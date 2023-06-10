import datetime
import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, \
    OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T10658(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_qfQuod_any_client_sell_FIXSELLTH2TEST.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/quickfix/client_qfQuod_any_client_sell_FIXSELLTH2TEST.xml"

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        element = ET.fromstring('<sellSideAlgo enabled="true">'
                                '<AlgoType internal="false">847</AlgoType>'
                                '<algos>'
                                '<algo scenario="1021"></algo>'
                                '<algo scenario="1023"></algo>'
                                '<algo scenario="1024"></algo>'
                                '</algos>'
                                '</sellSideAlgo>')
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.FIXSELLTH2TEST")
        time.sleep(35)
        # endregion

        # region step 1: create DMA  order with Algo
        # part 1: Create DMA order
        self.new_order_single.set_default_dma_limit()
        cl_ord_id = self.new_order_single.get_parameter('ClOrdID')
        time_day_and_hours = (datetime.datetime.now() + datetime.timedelta(hours=1))
        change_parameters = {
            'TargetStrategy': '1024',
            'StrategyParametersGrp': {'NoStrategyParameters': [{'StrategyParameterName': 'StartTime',
                                                                'StrategyParameterType': '28',
                                                                'StrategyParameterValue': time_day_and_hours.strftime(
                                                                    '%Y%m%d-%H:00:00Z')},
                                                               {'StrategyParameterName': 'EndTime',
                                                                'StrategyParameterType': '27',
                                                                'StrategyParameterValue': time_day_and_hours.strftime(
                                                                    '%H:00:00Z')}
                                                               ]}}
        self.new_order_single.change_parameters(change_parameters)
        self.fix_manager.send_message_fix_standard(self.new_order_single)
        time.sleep(5)
        order_id = self.db_manager.execute_query(f"SELECT ordid FROM ordr WHERE clordid = '{cl_ord_id}'")[
            0][0]
        self.execution_report.set_default_new(order_id)
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {order_id: order_id})
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            ord_reply,
            'Verifying that order created  (step 1)')
        # end_of_part

        # part 2: Verify 35=8 message on SellSide
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate', 'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'MaxPriceLevels', 'Parties',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'OrderAvgPx',
                                  'tag11245', 'ExecAllocGrp', 'SettlCurrFxRate', 'ConfirmType', 'SettlCurrFxRateCalc',
                                  'MatchStatus', 'ConfirmStatus', 'SettlCurrAmt', 'CpctyConfGrp', 'ConfirmTransType',
                                  'SettlCurrency', 'AllocSettlCurrAmt', 'TradeReportingIndicator', 'OrigClOrdID',
                                  'SettlType', 'Text']
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        execution_report_fix.set_default_new(self.new_order_single)
        change_parameters['StrategyParametersGrp']['NoStrategyParameters'][0][
            'StrategyParameterValue'] = time_day_and_hours.strftime("%Y%m%d-%H:00:00")
        change_parameters['StrategyParametersGrp']['NoStrategyParameters'][1][
            'StrategyParameterValue'] = time_day_and_hours.strftime("%Y%m%d-%H:00:00")
        change_parameters['StrategyParametersGrp']['NoStrategyParameters'][0][
            'StrategyParameterType'] = '19'
        change_parameters['StrategyParametersGrp']['NoStrategyParameters'][1][
            'StrategyParameterType'] = '19'
        execution_report_fix.change_parameters(change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(execution_report_fix,
                                                                  ignored_fields=list_of_ignored_fields)
        # end_of_part
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.FIXSELLTH2TEST")
        time.sleep(35)
        os.remove("temp.xml")
        self.ssh_client.close()
