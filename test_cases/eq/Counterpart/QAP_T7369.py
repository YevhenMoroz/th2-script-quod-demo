import logging
import time
from copy import deepcopy

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
import xml.etree.ElementTree as ET
from pkg_resources import resource_filename

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7369(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_2")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name("currency_3")
        self.change_params = {'Account': self.client,
                              "Currency": self.cur,
                              'ExDestination': self.mic,
                              'PreAllocGrp': {
                                  'NoAllocs': [{
                                      'AllocAccount': self.account,
                                      'AllocQty': "100"}]}}
        self.fix_message.change_parameters(self.change_params)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_bs = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.child_order_submit = OrderSubmitOMS(self.data_set)
        self.unmatch_transfer = UnMatchRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.result = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        class_name = QAP_T7369
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        quod.find("ors/BackToFront/FIXReportOrdrParties").text = "true"
        quod.find("ors/BackToFront/EnrichFIXExecReportParties").text = "true"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        # endregion
        # region create Care order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        parent_order_id = response[0].get_parameter("OrderID")
        client_ord_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region Split
        nos_rule = None
        trade_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.child_order_submit.set_default_child_dma(parent_order_id, client_ord_id)
            self.child_order_submit.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                                       'ListingList': {'ListingBlock': [
                                                                                           {
                                                                                               'ListingID': self.data_set.get_listing_id_by_name(
                                                                                                   "listing_2")}]},
                                                                                       'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                           "instrument_3")
                                                                                       })
            responses = self.java_api_manager.send_message_and_receive_response(self.child_order_submit)
            class_name.__print_message(f'Report after trade CHILD DMA ORDER', responses)
            self.__return_result(responses, PKSMessageType.PositionReport.value)
            exec_id = self.result.get_parameters()['PositionReportBlock']['PositionList']['PositionBlock'][0]['LastPositUpdateEventID']
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)

        list_of_ignored_fields = ['SettlCurrency', 'SecondaryOrderID', 'MiscFeesGrp', 'CommissionData', 'NoMiscFees',
                                  'PartyRoleQualifier','GatingRuleCondName', 'GatingRuleName']
        list_of_counterparts = [
                self.data_set.get_counterpart_id_fix('counterpart_id_gtwquod4'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa3'),
                self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2')
            ]
        parties = {
            'NoPartyIDs': list_of_counterparts
        }
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {"Parties": parties, "Currency": "GBp"})
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Currency": "GBp",
             "Account": self.account})
        exec_report2.remove_parameter("SettlCurrency")
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1, ignored_fields=list_of_ignored_fields)
        parties['NoPartyIDs'][-1] = self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user')
        self.fix_verifier.check_fix_message_fix_standard(exec_report2, ignored_fields=list_of_ignored_fields)
        # endregion

        # region unmatch and transfer
        self.unmatch_transfer.set_default(self.data_set, exec_id)
        self.unmatch_transfer.set_default_unmatch_and_transfer(self.data_set.get_account_by_name('client_pos_3_acc_3'))
        self.java_api_manager.send_message(self.unmatch_transfer)
        class_name.__print_message(f"{class_name} - After UNMATCH_AND_TRANSFER", responses)
        # endregion

        # region Set-up parameters for ExecutionReports
        noparties = {
            'NoParty': list_of_counterparts
        }

        all_param = {'NoAllocs': [{
            'AllocAccount': self.account,
            'AllocQty': "100",
            "AllocAcctIDSource": '*'}]}
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties, 'ReplyReceivedTime': "*", "Account": self.account, "Currency": "GBp",
             "LastMkt": self.mic})
        exec_report1.remove_parameter("SettlCurrency")
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"NoParty": noparties, "Account": self.client, "Currency": "GBp", 'QuodTradeQualifier': '*',
             "LastMkt": self.mic, "BookID": "*", "tag5120": "*", "ExecBroker": "*", "M_PreAllocGrp": all_param})
        exec_report2.remove_parameters(['TradeReportingIndicator', "SettlCurrency", "Parties"])
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1, ignored_fields=list_of_ignored_fields)
        self.fix_verifier_bs.check_fix_message_fix_standard(exec_report2, ignored_fields=list_of_ignored_fields)
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
                break

    @staticmethod
    def __print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(60)

