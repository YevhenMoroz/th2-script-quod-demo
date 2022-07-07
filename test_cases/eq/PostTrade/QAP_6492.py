import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

# region TestData
qty = "100"
price = "20"


# endregion


class QAP_6492(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Initialization
        fix_env = self.environment.get_list_fix_environment()[0]
        fix_manager = FixManager(fix_env.sell_side, self.test_id)
        middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        # endregion
        # region Variables
        client_pt = self.data_set.get_client_by_name("client_pt_1")
        client_venue = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        mic = self.data_set.get_mic_by_name("mic_1")
        # endregion
        # region Create and execute order
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(fix_env.buy_side,
                                                                                             client_venue,
                                                                                             mic, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(fix_env.buy_side,
                                                                                       client_venue, mic,
                                                                                       float(price), int(qty), delay=0)
            nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit().change_parameters({"Account":
                                                                                                            client_pt})
            fix_manager.send_message_fix_standard(nos)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(nos_rule)
        # endregion
        # region Book
        middle_office.book_order()
        # endregion
        # region Allocate
        middle_office.approve_block()
        middle_office.set_modify_ticket_details(arr_allocation_param=[{AllocationsColumns.alt_account.value: "test",
                                                                       AllocationsColumns.security_acc.value: "",
                                                                       AllocationsColumns.alloc_qty.value: qty}])
        middle_office.allocate_block()
        # endregion
        # region Verify
        alt_acc = middle_office.extract_allocate_value(AllocationsColumns.alt_account.value)
        acc_id = middle_office.extract_allocate_value(AllocationsColumns.account_id.value)

        middle_office.compare_values({AllocationsColumns.account_id.value: ""}, acc_id,
                                     "check Security account")
        middle_office.compare_values({AllocationsColumns.alt_account.value: "test"}, alt_acc,
                                     "check Alt account")
        # endregion
