import logging
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.oms_data_set.oms_const_enum import (
    OMSFee,
    OMSCommission,
    OmsVenues,
    OMSFeeType,
    OMSVenueID,
)
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import (
    OrderBookColumns,
    ExecSts,
    SecondLevelTabs,
    TradeBookColumns,
    FeeTypeForMiscFeeTab,
    Basis,
    AllocationsColumns,
    MiddleOfficeColumns,
)
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7166(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "100"
        self.price = "10"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name(
            "client_com_1_venue_2"
        )  # CLIENT_COMM_1_EUREX
        self.venue = self.data_set.get_mic_by_name("mic_2")  # EUREX
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.alloc_account = self.data_set.get_account_by_name("client_com_1_acc_1")  # CLIENT_COMM_1_SA1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, session_id)
        self.child_order_book = OMSChildOrderBook(self.test_id, self.session_id)

        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(
            self.ssh_client_env.host,
            self.ssh_client_env.port,
            self.ssh_client_env.user,
            self.ssh_client_env.password,
            self.ssh_client_env.su_user,
            self.ssh_client_env.su_password,
        )
        self.local_path = os.path.abspath("test_framework\ssh_wrappers\oms_cfg_files\client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Setup Backend config
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<automaticCalculatedReportEnabled>true</automaticCalculatedReportEnabled>")
        root = tree.getroot()
        root.append(element)
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(120)
        # endregion

        # region Send commission and fees
        # Commissions
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(
            client=self.client, comm_profile=self.perc_amt, commission=OMSCommission.commission1
        )
        self.commission_sender.change_message_params(
            {"venueID": OmsVenues.venue_2.value, "commissionAmountType": "BRK"}
        )
        self.commission_sender.send_post_request()

        # Fees
        self.commission_sender.set_modify_fees_message(
            comm_profile=self.perc_amt, fee=OMSFee.fee1, fee_type=OMSFeeType.stamp.value
        )
        self.commission_sender.change_message_params({"venueID": OMSVenueID.eurex.value})
        self.commission_sender.send_post_request()
        # endregion

        # region Create CO order via FIX
        self.fix_message.set_default_care_limit(instr="instrument_3")
        self.fix_message.change_parameters(
            {
                "Side": "1",
                "OrderQtyData": {"OrderQty": self.qty},
                "Account": self.client,
                "ExDestination": self.venue,
                "Currency": self.data_set.get_currency_by_name("currency_3"),  # GBp
                "Price": self.price,
            }
        )
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # get Client Order ID and Order ID
        cl_ord_id: str = response[0].get_parameters()["ClOrdID"]
        order_id: str = response[0].get_parameters()["OrderID"]
        # endregion

        # region Accept order
        self.client_inbox.accept_order(filter={OrderBookColumns.order_id.value: order_id})
        # endregion

        # region Check ExecutionReport
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.change_parameters({"Currency": "GBp"})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region step 1-2 - Split CO order and execute DMA order
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price), int(self.qty), 0
            )
            self.order_ticket.split_order([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Checking CO execution
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value, OrderBookColumns.exec_sts.value: ExecSts.filled.value}
        )
        # endregion

        # region step 3 - Checking Fees for EV Execution
        exec_id: dict = self.order_book.extract_2lvl_fields(
            SecondLevelTabs.executions.value,
            [OrderBookColumns.exec_id.value],
            [1],
            {OrderBookColumns.cl_ord_id.value: cl_ord_id},
        )[0]
        list_of_column_fees: list = [
            TradeBookColumns.fee_type.value,
            TradeBookColumns.basis.value,
            TradeBookColumns.rate.value,
            TradeBookColumns.amount.value,
        ]
        expected_values_for_misc_fees_tab: dict = {
            "FeeType1": FeeTypeForMiscFeeTab.stamp.value,
            "Basis1": Basis.percentage.value,
            "Rate1": "5",
            "Amount1": "0.5",
        }
        actual_values_for_fees_ev: dict = self.trade_book.extract_sub_lvl_fields(
            list_of_column_fees,
            TradeBookColumns.misc_tab.value,
            1,
            {TradeBookColumns.exec_id.value: exec_id.get("ExecID")},
        )
        self.trade_book.compare_values(
            expected_values_for_misc_fees_tab,
            actual_values_for_fees_ev,
            "Checking values in Misc Fees for EV Execution",
        )
        # endregion

        # region step 3 - Checking Commissions for EV Execution
        list_of_column_comm: list = [
            TradeBookColumns.basis.value,
            TradeBookColumns.rate.value,
            TradeBookColumns.amount.value,
            TradeBookColumns.amount_type.value,
        ]
        expected_values_for_cl_comm_tab: dict = {
            "Basis1": Basis.percent.value,
            "Rate1": "5",
            "Amount1": "0.5",
            "AmountType1": "Broker",
        }
        actual_values_for_comm_ev: dict = self.trade_book.extract_sub_lvl_fields(
            list_of_column_comm,
            SecondLevelTabs.commissions.value,
            1,
            {TradeBookColumns.exec_id.value: exec_id.get("ExecID")},
        )
        self.trade_book.compare_values(
            expected_values_for_cl_comm_tab, actual_values_for_comm_ev, "Checking Client Commissions for EV Execution"
        )
        # endregion

        # region step 3 - Checking Fees for EX Execution of Child order
        exec_id_child: dict = self.order_book.extract_sub_lvl_fields(
            [OrderBookColumns.exec_id.value],
            [SecondLevelTabs.child_tab.value, SecondLevelTabs.executions.value],
            {OrderBookColumns.cl_ord_id.value: cl_ord_id},
        )
        actual_values_for_fees_ex: dict = self.trade_book.extract_sub_lvl_fields(
            list_of_column_fees,
            TradeBookColumns.misc_tab.value,
            1,
            {TradeBookColumns.exec_id.value: exec_id_child.get("ExecID")},
        )
        self.trade_book.compare_values(
            expected_values_for_misc_fees_tab,
            actual_values_for_fees_ex,
            "Checking values in Misc Fees for EX Execution",
        )
        # endregion

        # region step 4 - Checking that DayCumQty=Qty of the parent order
        day_cum_qty: dict = self.order_book.extract_2lvl_fields(
            SecondLevelTabs.child_tab.value,
            [OrderBookColumns.day_cum_qty.value],
            [1],
            {OrderBookColumns.cl_ord_id.value: cl_ord_id},
        )[0]
        self.order_book.compare_values(
            {OrderBookColumns.day_cum_qty.value: self.qty},
            day_cum_qty,
            "Checking that DayCumQty=Qty of the parent order",
        )
        # endregion

        # region step 5 - Complete Parent CO order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region step 6 - Checking Commissions and Fees Electronic Calculated execution (EV CO order)
        exec_id_calculated: dict = self.order_book.extract_2lvl_fields(
            SecondLevelTabs.executions.value,
            [OrderBookColumns.exec_id.value],
            [2],
            {OrderBookColumns.cl_ord_id.value: cl_ord_id},
        )[0]
        actual_values_for_fees_calc: dict = self.trade_book.extract_sub_lvl_fields(
            list_of_column_fees,
            TradeBookColumns.misc_tab.value,
            1,
            {TradeBookColumns.exec_id.value: exec_id_calculated.get("ExecID")},
        )
        self.trade_book.compare_values(
            expected_values_for_misc_fees_tab,
            actual_values_for_fees_calc,
            "Checking values in Misc Fees for Electronic Calculated Execution",
        )
        actual_values_for_comm_calc: dict = self.trade_book.extract_sub_lvl_fields(
            list_of_column_comm,
            SecondLevelTabs.commissions.value,
            1,
            {TradeBookColumns.exec_id.value: exec_id_calculated.get("ExecID")},
        )
        expected_values_for_cl_comm_tab: dict = {
            "Basis1": Basis.absolute.value,
            "Rate1": "0.5",
            "Amount1": "0.5",
            "AmountType1": "Broker",
        }
        self.trade_book.compare_values(
            expected_values_for_cl_comm_tab,
            actual_values_for_comm_calc,
            "Checking values in Client Commissions for Electronic Calculated Execution",
        )
        # endregion

        # region step 7 - Check that the tabs of Commissions and Fees have values from EV (Calculated) execution
        # Extracting Commissions and Fees tab from Booking ticket
        extract_panels_from_booking = self.order_book.extracting_values_from_booking_ticket(
            [PanelForExtraction.COMMISSION, PanelForExtraction.FEES],
            filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id},
        )
        splitted_values = self.middle_office.split_fees(extract_panels_from_booking)  # Dictionary is not ordered
        if "FeeType" in splitted_values[0]:
            splitted_comm = splitted_values[1]
            splitted_fees = splitted_values[0]
        else:
            splitted_comm = splitted_values[0]
            splitted_fees = splitted_values[1]
        # Comparing values for Commissions tab
        actual_values_for_comm = {k: v.replace(",", "") for k, v in splitted_comm.items()}
        self.middle_office.compare_values(
            {
                TradeBookColumns.basis.value: Basis.percent.value,
                TradeBookColumns.rate.value: "5",
                TradeBookColumns.amount.value: "0.5",
                "Currency": "GBP",
                "AmountType": "BRK",
            },
            actual_values_for_comm,
            "Comparing values for Commissions tab",
        )
        # Comparing values for Fees tab
        actual_values_for_fees = {k: v.replace(",", "") for k, v in splitted_fees.items()}
        self.middle_office.compare_values(
            {
                TradeBookColumns.fee_type.value: FeeTypeForMiscFeeTab.stamp.value,
                TradeBookColumns.basis.value: Basis.percentage.value,
                TradeBookColumns.rate.value: "5",
                TradeBookColumns.amount.value: "0.5",
                "Currency": "GBP",
            },
            actual_values_for_fees,
            "Comparing values for Fees tab",
        )
        # endregion

        # region step 8-9 - Book and Approve order
        self.middle_office.book_order([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.middle_office.approve_block()
        # endregion

        # region step 10 - Allocate block
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}
        ]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()

        # Checking values after Allocate in Middle Office
        values_after_allocate = self.middle_office.extract_list_of_block_fields(
            [
                MiddleOfficeColumns.sts.value,
                MiddleOfficeColumns.match_status.value,
                MiddleOfficeColumns.summary_status.value,
                MiddleOfficeColumns.total_fees.value,
                MiddleOfficeColumns.client_comm.value,
            ],
            [MiddleOfficeColumns.order_id.value, order_id],
        )
        self.middle_office.compare_values(
            {
                MiddleOfficeColumns.sts.value: "Accepted",
                MiddleOfficeColumns.match_status.value: "Matched",
                MiddleOfficeColumns.summary_status.value: "MatchedAgreed",
                MiddleOfficeColumns.total_fees.value: "0.5",
                MiddleOfficeColumns.client_comm.value: "0.5",
            },
            values_after_allocate,
            "Checking values after Allocate in Middle Office",
        )
        # endregion

        # region Checking values in Allocations
        extracted_fields_from_alloc = self.middle_office.extract_list_of_allocate_fields(
            [
                AllocationsColumns.sts.value,
                AllocationsColumns.match_status.value,
                AllocationsColumns.total_fees.value,
                AllocationsColumns.client_comm.value,
            ]
        )
        self.middle_office.compare_values(
            {
                AllocationsColumns.sts.value: "Affirmed",
                AllocationsColumns.match_status.value: "Matched",
                AllocationsColumns.total_fees.value: "0.5",
                AllocationsColumns.client_comm.value: "0.5",
            },
            extracted_fields_from_alloc,
            "Checking values in Allocations",
        )
        # endregion

        # region Checking values in Misc Fees for Allocation
        self.middle_office.set_extract_sub_lvl_fields(list_of_column_fees, SecondLevelTabs.fees.value, 1)
        actual_values_for_misc_fees_in_alloc = self.middle_office.extract_allocation_sub_lvl(
            {MiddleOfficeColumns.order_id.value: order_id}, {AllocationsColumns.sts.value: "Affirmed"}
        )
        expected_values_for_misc_fees_tab: dict = {
            "FeeType1": OMSFeeType.stamp.value,
            "Basis1": "P",
            "Rate1": "5",
            "Amount1": "0.5",
        }
        self.middle_office.compare_values(
            expected_values_for_misc_fees_tab,
            actual_values_for_misc_fees_in_alloc,
            "Checking values in Misc Fees for Allocation",
        )
        # endregion

        # region Checking values in Client Commissions for Allocation
        self.middle_office.set_extract_sub_lvl_fields(list_of_column_comm, SecondLevelTabs.commissions.value, 1)
        actual_values_for_client_comm_in_alloc = self.middle_office.extract_allocation_sub_lvl(
            {MiddleOfficeColumns.order_id.value: order_id}, {AllocationsColumns.sts.value: "Affirmed"}
        )
        expected_values_for_cl_comm_tab: dict = {"Basis1": "PCT", "Rate1": "5", "Amount1": "0.5", "AmountType1": "BRK"}
        self.middle_office.compare_values(
            expected_values_for_cl_comm_tab,
            actual_values_for_client_comm_in_alloc,
            "Checking values in Client Commissions for Allocation",
        )
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        os.remove("temp.xml")

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
