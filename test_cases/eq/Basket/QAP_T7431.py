import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, OrderBookColumns, BasketBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7431(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.oms_basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.price = '10'
        self.fix_message = FixMessageNewOrderListOMS(self.data_set, parameters={
            'BidType': "1",
            'TotNoOrders': '3',
            'ListID': basic_custom_actions.client_orderid(10),
            'ListOrdGrp': {'NoOrders': [{
                "Account": data_set.get_client_by_name("client_pt_1"),
                "HandlInst": "3",
                "Side": "1",
                'OrderQtyData': {'OrderQty': "100"},
                "TimeInForce": "0",
                "OrdType": "2",
                'ListSeqNo': "1",
                'ClOrdID': basic_custom_actions.client_orderid(9),
                'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_pt_1_acc_1"),
                                              'AllocQty': "100"}]},
                "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
                'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
                "TransactTime": datetime.utcnow().isoformat(),
                "Price": "1000",
                "Currency": data_set.get_currency_by_name("currency_1")
            }, {
                "Account": data_set.get_client_by_name("client_pt_1"),
                "HandlInst": "3",
                "Side": "1",
                'OrderQtyData': {'OrderQty': "100"},
                "TimeInForce": "0",
                "OrdType": "2",
                'ListSeqNo': "2",
                'ClOrdID': basic_custom_actions.client_orderid(9),
                'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_pt_1_acc_1"),
                                              'AllocQty': "100"}]},
                "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
                'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
                "TransactTime": datetime.utcnow().isoformat(),
                "Price": "1000",
                "Currency": data_set.get_currency_by_name("currency_1")
            },
                {
                    "Account": data_set.get_client_by_name("client_pt_1"),
                    "HandlInst": "3",
                    "Side": "1",
                    'OrderQtyData': {'OrderQty': "100"},
                    "TimeInForce": "0",
                    "OrdType": "2",
                    'ListSeqNo': "1",
                    'ClOrdID': basic_custom_actions.client_orderid(9),
                    'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_pt_1_acc_1"),
                                                  'AllocQty': "100"}]},
                    "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
                    'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
                    "TransactTime": datetime.utcnow().isoformat(),
                    "Price": "1000",
                    "Currency": data_set.get_currency_by_name("currency_1")
                }
            ]}
        })
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.fix_manager.send_message_fix_standard(self.fix_message)
        qty = self.fix_message.get_parameters()['ListOrdGrp']['NoOrders'][2]['OrderQtyData']['OrderQty']
        rule_manager = RuleManager(Simulators.equity)
        rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env.buy_side, self.client_for_rule,
                                                                  self.exec_destination, price=1000)
        for i in range(3):
            self.client_inbox.accept_order(self.lookup, qty, self.price)
        cl_ord_id_first = self.fix_message.get_parameters()['ListOrdGrp']['NoOrders'][0]['ClOrdID']
        cl_ord_id_second = self.fix_message.get_parameters()['ListOrdGrp']['NoOrders'][1]['ClOrdID']
        cl_ord_id_third = self.fix_message.get_parameters()['ListOrdGrp']['NoOrders'][2]['ClOrdID']
        client_basket_id = self.fix_message.get_parameters()['ListID']
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_third])
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value, row_number=1)
        # region wave basket first time
        self.oms_basket_book.wave_basket('70', route=self.data_set.get_route('route_2'), removed_orders=[order_id],
                                         basket_filter={BasketBookColumns.client_basket_id.value: client_basket_id})
        # endregion

        # region verify child order after first basket
        first_dma_order = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.sts.value,
                                                               OrderBookColumns.qty.value], [1],
                                                              {OrderBookColumns.cl_ord_id.value: cl_ord_id_first})
        second_dma_order = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                               [OrderBookColumns.sts.value,
                                                                OrderBookColumns.qty.value], [1],
                                                               {OrderBookColumns.cl_ord_id.value: cl_ord_id_second})

        self.oms_basket_book.compare_values(
            {OrderBookColumns.qty.value: str(int(0.7 * int(qty)))},
            first_dma_order[0], 'Compare second child order after first wave for first order')
        self.oms_basket_book.compare_values(
            {OrderBookColumns.qty.value: str(int(0.7 * int(qty)))},
            second_dma_order[0],
            'Compare second child order after first wave for second order')
        # endregion

        # region wave basket second time
        self.oms_basket_book.wave_basket('100', route=self.data_set.get_route('route_1'), removed_orders=[order_id],
                                         basket_filter={BasketBookColumns.client_basket_id.value: client_basket_id})
        # endregion

        # region verify child order after second basket

        first_dma_order = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.sts.value,
                                                               OrderBookColumns.qty.value],
                                                              rows=[1], filter_dict={
                OrderBookColumns.cl_ord_id.value: cl_ord_id_second})
        second_dma_order = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                               [OrderBookColumns.sts.value,
                                                                OrderBookColumns.qty.value],
                                                               rows=[1], filter_dict={
                OrderBookColumns.cl_ord_id.value: cl_ord_id_second})

        self.oms_basket_book.compare_values(
            {OrderBookColumns.qty.value: str(int(0.3 * int(qty)))},
            first_dma_order[0], 'Compare second child order after second wave for first order')
        self.oms_basket_book.compare_values(
            {OrderBookColumns.qty.value: str(int(0.3 * int(qty)))},
            second_dma_order[0], 'Compare second child order after second wave for second order')
        # endregion
