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
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsVenues, OMSCommission
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import (
    OrderBookColumns,
    ExecSts,
    PostTradeStatuses,
)
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7163(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "200"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name(
            "client_com_1_venue_2"
        )  # CLIENT_COMM_1_EUREX
        self.venue = self.data_set.get_mic_by_name("mic_2")  # EUREX
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send commission and fees
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(
            client=self.client, comm_profile=self.perc_amt, commission=OMSCommission.commission1
        )
        self.commission_sender.change_message_params(
            {"venueID": OmsVenues.venue_2.value, "commissionAmountType": "BRK"}
        )
        self.commission_sender.send_post_request()
        # endregion

        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price), int(self.qty), 0
            )
            self.fix_message.set_default_dma_limit(instr="instrument_3")
            self.fix_message.change_parameters(
                {
                    "Side": "1",
                    "OrderQtyData": {"OrderQty": self.qty},
                    "Account": self.client,
                    "ExDestination": self.venue,
                    "Currency": self.data_set.get_currency_by_name("currency_3"),
                }
            )
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id: str = response[0].get_parameters()["ClOrdID"]

        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Checking statuses in OrderBook
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {
                OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                OrderBookColumns.done_for_day.value: "Yes",
            },
            "Comparing statuses after trading",
        )
        # endregion

        # region Extracting values from Booking ticket
        extract_comm_panel_from_booking = self.order_book.extracting_values_from_booking_ticket(
            [PanelForExtraction.COMMISSION], filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id}
        )
        splitted_fees: dict = self.middle_office.split_fees(extract_comm_panel_from_booking)[0]
        values_from_commission_panel: dict = {k: v.replace(",", "") for k, v in splitted_fees.items()}
        # endregion

        # region Comparing values from the Commission panel
        expected_values_from_commission_panel: dict = {
            "Basis": "Percent",
            "Rate": "5",
            "Amount": "2",
            "Currency": "GBP",
            "AmountType": "BRK",
        }
        self.middle_office.compare_values(
            expected_values_from_commission_panel,
            values_from_commission_panel,
            "Comparing values from the Commission panel",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
