import logging
import time
from datetime import datetime
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_3303(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '10'
        self.exchange_rate = '2'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
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
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Filter Order Book and Check values
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after trading')
        # endregion

        # region Extracting values from Booking ticket
        extract_panels = self.order_book.extracting_values_from_booking_ticket(
            [PanelForExtraction.MAIN_PANEL], filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id})
        values_from_panels = {}
        for d in self.middle_office.split_tab_misk(extract_panels):
            values_from_panels.update(d)
        # endregion

        # region Calculating SettlAmount before Re-compute
        global settl_amount_before_recompute
        if len(values_from_panels['TotalComm']) == 0 and len(values_from_panels['TotalFees']) == 0:
            settl_amount_before_recompute = '{:,}'.format((int(self.qty) * int(self.price)) * float(self.exchange_rate))
        elif len(values_from_panels['TotalComm']) == 0:
            if values_from_panels['TotalFees'] == '0':
                settl_amount_before_recompute = '{:,}'.format(
                    (int(self.qty) * int(self.price) + int(values_from_panels.get('TotalFees'))) * int(
                        self.exchange_rate))
            else:
                settl_amount_before_recompute = '{:,}'.format(
                    (int(self.qty) * int(self.price) + float(values_from_panels.get('TotalFees'))) * int(
                        self.exchange_rate))
        elif len(values_from_panels['TotalFees']) == 0:
            if values_from_panels['TotalComm'] == '0':
                settl_amount_before_recompute = '{:,}'.format(
                    (int(self.qty) * int(self.price) + int(values_from_panels.get('TotalComm'))) * int(
                        self.exchange_rate))
            else:
                settl_amount_before_recompute = '{:,}'.format(
                    (int(self.qty) * int(self.price) + float(values_from_panels.get('TotalComm'))) * int(
                        self.exchange_rate))
        else:
            settl_amount_before_recompute = '{:,}'.format((int(self.qty) * int(self.price) + float(
                values_from_panels.get('TotalComm')) + float(values_from_panels.get('TotalFees'))) * int(
                self.exchange_rate))
        # endregion

        # region Book order and checking values in the Order book
        self.middle_office.set_modify_ticket_details(settl_currency='USD', exchange_rate=self.exchange_rate,
                                                     toggle_recompute=True)
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Extracting Settlement panel in Booking ticket after Book
        settlement_panel_after_book = self.middle_office.extracting_values_from_amend_ticket(
            [PanelForExtraction.SETTLEMENT])
        expected_settlement_panel_after_book = {}
        for d in self.middle_office.split_tab_misk(settlement_panel_after_book):
            expected_settlement_panel_after_book.update(d)
        # endregion

        # region Checking SettlAmount after applying Re-compute
        settl_amount_after_recompute = expected_settlement_panel_after_book.get('SettlAmount')
        self.middle_office.compare_values({'SettlAmount': settl_amount_before_recompute},
                                          {'SettlAmount': settl_amount_after_recompute},
                                          'Comparing SettlAmount after Re-compute')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
