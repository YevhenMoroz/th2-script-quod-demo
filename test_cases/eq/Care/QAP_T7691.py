import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, AlgoParametersExternal, \
    SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7691(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.child_book = OMSChildOrderBook(self.test_id, self.session_id)
        self.route = self.data_set.get_route("route_2")
        self.qty_type = self.data_set.get_qty_type('qty_type_1')
        self.ref_price = self.data_set.get_ref_price('ref_pr_2')
        self.ref_price_res = self.data_set.get_ref_price('ref_pr_9')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region direct poc
        self.client_inbox.client_inbox_direct_poc(qty_type=self.qty_type, reference_price=self.ref_price, percentage="50",
                                             qty_percentage="100", route=self.route)
        # endregion
        # region check fields
        self.order_book.check_second_lvl_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        self.child_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                            [OrderBookColumns.order_id.value], [1],
                                                            {OrderBookColumns.order_id.value: order_id})
        self.__check_child_book(self.ref_price_res, 1)
        self.__check_child_book('50', 2)
        # endregion

    def __check_child_book(self, expected_res: str, row: int):
        act_res = self.child_book.get_child_order_sub_lvl_value(row,
                                                                AlgoParametersExternal.parameter_value.value,
                                                                SecondLevelTabs.algo_parameters.value,
                                                                child_book_filter={
                                                                    OrderBookColumns.order_id.value:
                                                                        self.child_id[0]['ID']})
        self.child_book.compare_values({f"ParameterValue {row}": expected_res},
                                       {f"ParameterValue {row}": act_res},
                                       "Check Parameters of Algo order")
