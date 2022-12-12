import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7176(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(trade_rule)
            # endregion

            # region book order
            self.all_instr.set_default_book(order_id)
            self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                      {"InstrID": self.data_set.get_instrument_id_by_name(
                                                          "instrument_2"), "Side": "Sell", "ClientCommissionList": {
                                                          "ClientCommissionBlock": [{"CommissionAmountType": "Broker",
                                                                                     "CommissionAmount": "1",
                                                                                     "CommissionBasis": "Absolute",
                                                                                     "CommissionCurrency": "EUR",
                                                                                     "CommissionRate": "1"}]}})
            self.java_api_manager.send_message_and_receive_response(self.all_instr)
            allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                    JavaApiFields.AllocationReportBlock.value]
            alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
            expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                               JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value}
            actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                               JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
            self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking')
            expected_comm = {"ClientCommissionCurrency": "EUR",
                             "ClientCommission": "1.0",
                             "ClientCommissionBasis": "ABS"
                             }
            self.java_api_manager.compare_values(expected_comm, allocation_report["ClientCommissionDataBlock"],
                                                 'Check booking commission')
            # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
