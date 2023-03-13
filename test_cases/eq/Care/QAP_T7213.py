import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7213(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = FixNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_quickfixgtw_qfQuod_any_backoffice_sell.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_quickfixgtw_qfQuod_any_backoffice_sell.xml"
        self.local_path_2 = resource_filename("test_resources.be_configs.oms_be_configs",
                                              "client_ors.xml")
        self.remote_path_2 = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.route_act_grp_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1'
        price = '1'
        client = self.data_set.get_client_by_name('client_1')
        # endregion

        # region precondition
        # part 1: Set Configuration
        tree = ET.parse(self.local_path)
        tree.getroot().find("connectivity/mapClientAccountGroupIDForTavira").text = 'true'
        tree.write("temp.xml")
        tree2 = ET.parse(self.local_path_2)
        tree2.getroot().find("ors/FIXNotif/mapping/ClientAccountGroupID/OrdReply").text = 'RouteActGrpName'
        tree2.getroot().find("ors/FIXNotif/mapping/ClientAccountGroupID/ExecutionReport").text = 'RouteActGrpName'
        tree2.write("temp2.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.put_file(self.remote_path_2, "temp2.xml")
        self.ssh_client.send_command("qrestart QUOD.FIXBACKOFFICE_TH2 QUOD.ORS")
        time.sleep(90)
        # end of part

        # part 2 : Create CO order
        self.order_submit.set_default_care_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "ClientAccountGroupID": client,
             "Price": price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # end of part
        # endregion

        # region step 1-2: Manual Execute CO order
        self.trade_entry.set_default_trade(ord_id, price, qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        # endregion

        # region step 3 : Check that 35=8 messages has properly value for 1 tag
        # part 1: Check Fix_OrdReply message
        ignored_fields = ['ExecID', 'GatingRuleCondName', 'OrderQtyData',
                          'LastQty', 'GatingRuleName', 'OrderID',
                          'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier',
                          'BookID', 'SettlCurrency', 'SettlDate', 'Currency',
                          'TimeInForce', 'PositionEffect', 'TradeDate', 'HandlInst',
                          'LeavesQty', 'NoParty', 'CumQty', 'LastPx', 'OrdType',
                          'tag5120', 'LastMkt', 'OrderCapacity', 'QtyType',
                          'ExecBroker', 'Price', 'VenueType', 'ExDestination',
                          'Instrument', 'GrossTradeAmt']
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        execution_report_fix.change_parameters(
            {"ExecType": "0", "OrdStatus": "0", 'ClOrdID': cl_ord_id,
             'Account': self.route_act_grp_name}
        )
        self.fix_verifier.check_fix_message_fix_standard(execution_report_fix, ignored_fields=ignored_fields)
        # end_of_part

        # part 2: Check Fix_ExecutionReport message
        execution_report_fix.change_parameters(
            {"ExecType": "F", "OrdStatus": "2"}
        )
        self.fix_verifier.check_fix_message_fix_standard(execution_report_fix, ignored_fields=ignored_fields)
        # end_of_part

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.put_file(self.remote_path_2, self.local_path_2)
        self.ssh_client.send_command("qrestart QUOD.FIXBACKOFFICE_TH2 QUOD.ORS")
        os.remove('temp.xml')
        os.remove('temp2.xml')
        time.sleep(90)
        self.ssh_client.close()
