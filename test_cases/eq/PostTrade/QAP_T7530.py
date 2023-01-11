import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7530(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '100'
        price = '10'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        sec_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        # endregion
        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception as ex:
            logger.exception(f'{ex} - your exception')

        finally:
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

        # endregion
        # region book and amend BO fields (step 2, step 3, step 4)
        self.all_instr.set_default_book(order_id)
        alloc_misc =  {
            "AllocInstructionMisc0": "BOF1A",
            "AllocInstructionMisc1": "BOF2A",
            "AllocInstructionMisc2": "BOF3A",
            "AllocInstructionMisc3": "BOF4A",
            "AllocInstructionMisc4": "BOF5A"
        }
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
                                                   "AllocInstructionMiscBlock": alloc_misc
                                                   })
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]

        print(allocation_report["AllocInstructionMiscBlock"])
        self.java_api_manager.compare_values(alloc_misc,
                                             allocation_report["AllocInstructionMiscBlock"],
                                             'Check booking')
        # endregion
        # region allocation block and check values at fix(step 5, step 6, step 7, step 8)
        self.approve.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve)

        self.confirm.set_default_allocation(alloc_id)
        conf_misc = {
            "ConfirmationMisc0": "BOF1C",
            "ConfirmationMisc1": "BOF2C",
            "ConfirmationMisc2": "BOF3C",
            "ConfirmationMisc3": "BOF4C",
            "ConfirmationMisc4": "BOF5C"
        }
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": sec_account,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2"),
                                                                      "ConfirmationMiscBlock": conf_misc
                                                                      })
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(conf_misc,
                                             confirm_report["ConfirmationMiscBlock"],
                                             f'Check ConfirmationMiscBlock of confirmation of {account}')

        # endregion
