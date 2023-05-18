import logging
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6950(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.currency = self.data_set.get_currency_by_name('currency_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_quickfixgtw_qfQuod_any_backoffice_sell.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_quickfixgtw_qfQuod_any_backoffice_sell.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_1')
        alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        # endregion

        # region precondition
        # part 1: Set Configuration
        tree = ET.parse(self.local_path)
        tree.getroot().find("connectivity/mapClientAccountGroupIDForTavira").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart FIXBACKOFFICE_TH2")
        time.sleep(50)
        # end of part

        # part 2 : Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit, response_time=10000)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value
        ]
        ord_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        # end of part

        # part 3 (trade dma order)
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": price,
                "AvgPrice": price,
                "LastPx": price,
                "OrdQty": qty,
                "LastTradedQty": qty,
                "CumQty": qty,
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        # end of part

        # part 4 book order
        self.allocation_instruction.set_default_book(ord_id)
        gross_trade_amt = float(price) * float(qty)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": qty,
                                                                "AvgPx": price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt),
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': price}]},
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report,
            f'Check expected and actually results for block (part of precondition)')
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update, f'Check expected and actually result for order (part of precondition)')
        # end of part

        # endregion

        # region step 1 : Approve block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
            allocation_report,
            f'Check expected and actually results for block (step 1)')
        # endregion

        # region step 2 : Allocate order
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock',
                                                             {"AllocQty": qty,
                                                              "Side": "B",
                                                              "AvgPx": price,
                                                              "AllocAccountID": alloc_account})
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value},
            allocation_report,
            f'Check expected and actually results for block (step 2)')
        self.java_api_manager.compare_values({
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value
        }, confirmation_report, f'Check expected and actually results for allocation (step 2)')
        # endregion

        # region step 4 : Check Fix_Confirmation
        list_of_ignored_fields = ['AllocQty', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier',
                                  'BookID', 'SettlDate', 'OrderAvgPx', 'Currency',
                                  'NetMoney', 'MatchStatus', 'ConfirmStatus', 'TradeDate',
                                  'NoParty', 'AllocInstructionMiscBlock1', 'tag5120',
                                  'ReportedPx', 'Instrument', 'GrossTradeAmt', 'AllocInstructionMiscBlock2']
        list_of_ignored_fields.extend(['CpctyConfGrp', 'ConfirmID', 'ConfirmType', 'AllocAccount', 'tag11245'])
        self.confirmation_report.change_parameters(
            {'NoOrders': [{'ClOrdID': cl_ord_id, 'OrderID': ord_id}],
             'ConfirmTransType': "0",
             'Account': client,
             'AllocID': alloc_id})
        self.fix_verifier.check_fix_message_fix_standard(self.confirmation_report,
                                                         ['ConfirmTransType', 'NoOrders', 'AllocID'],
                                                         ignored_fields=list_of_ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart FIXBACKOFFICE_TH2")
        time.sleep(30)
        self.ssh_client.close()
