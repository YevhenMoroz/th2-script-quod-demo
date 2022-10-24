import logging
import os
import time
from pathlib import Path
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiSettlementModelMessages import RestApiSettlementModelMessages
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6996(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_conn = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_conn, case_id=self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.api_message = RestApiSettlementModelMessages(self.data_set)
        self.local_path = os.path.abspath("../../test_framework\ssh_wrappers\oms_cfg_files\client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        client = self.data_set.get_client_by_name('client_counterpart_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        self.fix_message.change_parameter("HandlInst", '3')

        # region set up configuration on ORS(precondition)
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        quod.find("ors/FrontToBack/setSettlementModel").text = "true"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        # endregion

        # region precondition and step 1
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        vanue_id = self.data_set.get_venue_id('paris')
        self.api_message.set_modify_message_amend(client, venue_id=vanue_id)
        self.rest_api_manager.send_post_request(self.api_message)
        counterpart_settl_location = self.data_set.get_counterpart_id_fix('counterpart_id_settlement_location')
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id_care = response[0].get_parameter("OrderID")
        fix_execution_report.set_default_new(self.fix_message)
        fix_execution_report.remove_parameter("Parties").add_tag({'QuodTradeQualifier': '*'})
        fix_execution_report.add_tag({'BookID': '*'}).add_tag({'tag5120': '*'}).add_tag({'ExecBroker': '*'})
        no_party = {"NoParty": {'NoParty': [
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyRoleQualifier': '*',
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            {'PartyRole': "*",
             'PartyID': "*",
             'PartyIDSource': "*"},
            counterpart_settl_location]}}
        fix_execution_report.add_tag(no_party)
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report)
        self.trade_entry_message.set_default_trade(order_id_care, exec_price=price, exec_qty=qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value)
        actually_result = result.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.TransExecStatus.value]
        self.order_book.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {OrderBookColumns.exec_sts.value: actually_result},
            f'Comparing {OrderBookColumns.exec_sts.value}')
        # endregion

        # region step 2
        fix_execution_report.set_default_filled(self.fix_message)
        fix_execution_report.remove_parameter("Parties").add_tag({'QuodTradeQualifier': '*'}). \
            remove_parameter('SettlCurrency').remove_parameter('LastExecutionPolicy'). \
            remove_parameter('TradeReportingIndicator').add_tag({'VenueType': '0'}).remove_parameter('SecondaryExecID') \
            .remove_parameter('SecondaryOrderID').add_tag({'LastMkt': '*'}).change_parameter('VenueType', 'O')
        fix_execution_report.add_tag({'BookID': '*'}).add_tag({'tag5120': '*'}).add_tag({'ExecBroker': '*'})

        fix_execution_report.add_tag(no_party)
        list_of_ignored_fields = ['CommissionData', 'NoMiscFees', 'SecurityDesc', 'PartyRoleQualifier']
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignored_fields)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.api_message.set_modify_message_clear()
        self.rest_api_manager.send_post_request(self.api_message)
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)
        os.remove("temp.xml")
