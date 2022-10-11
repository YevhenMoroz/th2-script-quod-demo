import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns, \
    BasketSecondLvlTabName, OrderBagColumn
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7338(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderListOMS(self.data_set)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.bag_order_book = OMSBagOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        name_of_bag = 'QAP_T7338'
        nol = FixMessageNewOrderListOMS(self.data_set)
        nol.base_parameters['ListOrdGrp']['NoOrders'][1]['Side'] = '1'
        nol.set_default_order_list()
        self.fix_manager.send_message_fix_standard(nol)
        nol_id = nol.get_parameter("ListID")
        # endregion

        # region accept co orders
        qty = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["OrderQtyData"]["OrderQty"]
        qty_verifying = str(int(int(qty) * 2))
        cl_ord_id1 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["ClOrdID"]
        cl_ord_id2 = nol.get_parameter("ListOrdGrp")['NoOrders'][1]["ClOrdID"]
        price = nol.get_parameter("ListOrdGrp")['NoOrders'][1]["Price"]
        self.client_inbox.accept_order(filter={"ClOrdId": cl_ord_id1})
        self.client_inbox.accept_order(filter={"ClOrdId": cl_ord_id2})
        # endregion

        # region verifying of basket value
        client_order_ids = self.basket_book.get_basket_sub_lvl_value(2,

                                                                     OrderBookColumns.cl_ord_id.value,
                                                                     BasketSecondLvlTabName.orders.value,
                                                                     {
                                                                         BasketBookColumns.client_basket_id.value:
                                                                             nol_id}
                                                                     )
        self.basket_book.compare_values({'1': cl_ord_id1, '2': cl_ord_id2}, client_order_ids, 'Comparing orders')
        # endregion


        # region verifying of created bag
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price=price)
        self.bag_order_book.create_bag()
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.order_bag_qty.value,
                                                             OrderBagColumn.ord_bag_name.value,
                                                             OrderBagColumn.unmatched_qty.value,
                                                             OrderBagColumn.leaves_qty.value,
                                                             ],
                                                            [
                                                                qty_verifying,
                                                                name_of_bag,
                                                                qty_verifying,
                                                                qty_verifying
                                                            ], False, 'creation',
                                                            )
        # endregion

    def __extracting_and_comparing_value_for_bag_order(self, bag_column_extraction: list, expected_values: list,
                                                       return_order_bag_id: bool, action: str):
        fields = self.bag_order_book.extract_order_bag_book_details('1', bag_column_extraction)
        expected_values_bag = dict()
        order_bag_id = None
        if return_order_bag_id:
            order_bag_id = fields.pop(OrderBagColumn.id.value)
            bag_column_extraction.remove(OrderBagColumn.id.value)
        for count in range(len(bag_column_extraction)):
            expected_values_bag.update({bag_column_extraction[count]: expected_values[count]})
        self.bag_order_book.compare_values(expected_values_bag,
                                           fields, f'Compare values from bag_book after {action}')
        if return_order_bag_id:
            return order_bag_id
    # endregion
