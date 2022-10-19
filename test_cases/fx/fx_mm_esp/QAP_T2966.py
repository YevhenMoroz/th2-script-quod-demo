import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX


class QAP_T2966(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.manual_settings_request = QuoteManualSettingsRequestFX(data_set=self.data_set)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.new_order_single_doubler = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.execution_report_doubler = FixMessageExecutionReportFX()
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date_1w = self.data_set.get_settle_date_by_name('wk1')
        self.settle_type_1w = self.data_set.get_settle_type_by_name('wk1')
        self.settle_type_1w_java = self.data_set.get_settle_type_ja_by_name('wk1')
        self.tenor_1w_java = self.data_set.get_tenor_java_api_by_name("tenor_1w")
        self.bands_eur_usd = ["1000000", '5000000', '10000000']
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.instrument_order_1 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.instrument_order_2 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_1w}]
        self.sts_filled = Status.Fill
        self.sts_rejected = Status.Reject

        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.silver_id = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.quote_adj_entry = {
            "QuoteAdjustmentEntryBlock":
                [{"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "TRD",
                  "IndiceUpperQty": "1"},

                 {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "2"},

                 {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "3"}]}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_1w_java})
        self.manual_settings_request.set_executable_off()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(15)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd, published=False)
        self.sleep(4)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion

        # region Step 3
        self.new_order_single.set_default().change_parameters(
            {"Instrument": self.instrument_order_1,
             "SettlDate": self.settle_date_1w,
             "SettlType": self.settle_type_1w})

        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_rejected,
                                                               response=response[-1])
        self.execution_report.change_parameter("Text", "not tradeable")
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_1w_java})
        self.java_manager.send_message(self.manual_settings_request)

        self.quote_adjustment.set_defaults().update_fields_in_component(
            "QuoteAdjustmentRequestBlock",
            {"InstrSymbol": self.eur_usd,
             "ClientTierID": self.silver_id,
             "QuoteAdjustmentEntryList": self.quote_adj_entry,
             "Tenor": self.tenor_1w_java})
        self.java_manager.send_message(self.quote_adjustment)
        time.sleep(15)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDQuoteType="0")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDQuoteType="0")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDQuoteType="0")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDQuoteType="0")
        self.sleep(4)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        # region Step 3
        self.new_order_single.set_default().change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument,
             "SettlDate": self.settle_date_1w,
             "SettlType": self.settle_type_1w})

        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_filled,
                                                               response=response[-1])
        self.execution_report.remove_parameters(["Text", "ExecRestatementReason"])
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

        # region Step 4
        self.new_order_single_doubler.set_default()
        self.new_order_single_doubler.change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument_order_2,
             "SettlDate": self.settle_date_1w,
             "SettlType": self.settle_type_1w,
             "OrderQty": "2000000"})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single_doubler, self.test_id)
        self.execution_report_doubler.set_params_from_new_order_single(self.new_order_single_doubler, self.sts_rejected,
                                                                       response=response[-1])
        self.execution_report_doubler.change_parameter("Text", "not enough quantity in book")
        self.fix_verifier.check_fix_message(self.execution_report_doubler)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Step 5
        self.quote_adjustment.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                        {"InstrSymbol": self.eur_usd,
                                                                         "ClientTierID": self.silver_id,
                                                                         "Tenor": self.tenor_1w_java})
        self.java_manager.send_message(self.quote_adjustment)
        # endregion
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # region Step 5
        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_1w_java})
        self.java_manager.send_message(self.manual_settings_request)
        # endregion
