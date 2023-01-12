import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX


class QAP_T2870(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
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
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_date_spot = self.data_set.get_settle_date_by_name('spot')
        self.settle_type_spot = self.data_set.get_settle_type_by_name('spot')
        self.bands_eur_usd = ["1000000", '5000000', '10000000']
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_1 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_2 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_3 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_4 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_5 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_6 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.instrument_order_7 = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_spot}]
        self.sts_filled = Status.Fill
        self.sts_rejected = Status.Reject
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
        # region 1-2
        self.manual_settings_request.set_default_params()
        self.manual_settings_request.set_executable_off()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(4)
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd, published=False)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)
        # endregion
        # region 3
        self.new_order_single.set_default().change_parameters(
            {"Instrument": self.instrument_order_1,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot})

        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_rejected,
                                                               response=response[-1])
        self.execution_report.change_parameter("Text", "not tradeable")
        self.fix_verifier.check_fix_message(self.execution_report)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion
        # region 4
        self.manual_settings_request.set_default_params()
        self.manual_settings_request.set_pricing_off()
        self.java_manager.send_message(self.manual_settings_request)
        time.sleep(4)

        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd, priced=False)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)
        # endregion
        # region 5
        self.new_order_single.set_default().change_parameters(
            {"Instrument": self.instrument_order_2,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot})

        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_rejected,
                                                               response=response[-1])
        self.execution_report.change_parameter("Text", "not active")
        self.fix_verifier.check_fix_message(self.execution_report)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region 6
        self.manual_settings_request.set_default_params()
        self.java_manager.send_message(self.manual_settings_request)
        self.quote_adjustment.set_defaults().update_fields_in_component(
            "QuoteAdjustmentRequestBlock",
            {"InstrSymbol": self.eur_usd,
             "ClientTierID": self.silver_id,
             "QuoteAdjustmentEntryList": self.quote_adj_entry})
        self.java_manager.send_message(self.quote_adjustment)
        time.sleep(4)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDQuoteType="0")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDQuoteType="0")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDQuoteType="0")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDQuoteType="0")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)

        # region 7
        self.new_order_single.set_default().change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument_order_3,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot})

        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_filled,
                                                               response=response[-1])
        self.execution_report.remove_parameters(["Text", "ExecRestatementReason"])
        self.fix_verifier.check_fix_message(self.execution_report)
        self.new_order_single_doubler.set_default()
        self.new_order_single_doubler.change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument_order_4,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot,
             "OrderQty": "2000000"})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single_doubler, self.test_id)
        self.execution_report_doubler.set_params_from_new_order_single(self.new_order_single_doubler, self.sts_rejected,
                                                                       response=response[-1])
        self.execution_report_doubler.change_parameter("Text", "not enough quantity in book")
        self.fix_verifier.check_fix_message(self.execution_report_doubler)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        # endregion

        # region 8
        self.manual_settings_request.set_default_params()
        self.java_manager.send_message(self.manual_settings_request)

        self.quote_adjustment.set_defaults().update_fields_in_component(
            "QuoteAdjustmentRequestBlock",
            {"InstrSymbol": self.eur_usd,
             "ClientTierID": self.silver_id})
        self.quote_adjustment.disable_pricing_by_index(2).disable_pricing_by_index(3)
        self.java_manager.send_message(self.quote_adjustment)
        time.sleep(4)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, QuoteCondition="B")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, QuoteCondition="B")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, QuoteCondition="B")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, QuoteCondition="B")
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)

        # region Step 9
        self.new_order_single.set_default().change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument_order_5,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot})

        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_filled,
                                                               response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report)
        self.new_order_single_doubler.set_default()
        self.new_order_single_doubler.change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument_order_6,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot,
             "OrderQty": "2000000"})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single_doubler, self.test_id)
        self.execution_report_doubler.set_params_from_new_order_single(self.new_order_single_doubler, self.sts_rejected,
                                                                       response=response[-1])
        self.execution_report_doubler.change_parameter("Text", "not enough quantity in book")
        self.fix_verifier.check_fix_message(self.execution_report_doubler)
        # endregion
        # region 10
        self.manual_settings_request.set_default_params()
        self.java_manager.send_message(self.manual_settings_request)
        # endregion
        self.quote_adjustment.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                        {"InstrSymbol": self.eur_usd,
                                                                         "ClientTierID": self.silver_id})
        self.java_manager.send_message(self.quote_adjustment)
        self.new_order_single.set_default()
        self.new_order_single.change_parameters(
            {"Account": self.silver,
             "Instrument": self.instrument_order_7,
             "SettlDate": self.settle_date_spot,
             "SettlType": self.settle_type_spot,
             "OrderQty": "2000000"})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report_doubler.set_params_from_new_order_single(self.new_order_single, self.sts_filled,
                                                                       response=response[-1])
        self.execution_report_doubler.remove_parameters(["Text", "ExecRestatementReason"])
        self.fix_verifier.check_fix_message(self.execution_report_doubler)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.quote_adjustment.set_defaults().update_fields_in_component(
            "QuoteAdjustmentRequestBlock",
            {"InstrSymbol": self.eur_usd,
             "ClientTierID": self.silver_id})
        self.java_manager.send_message(self.quote_adjustment)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.manual_settings_request.set_default_params()
        self.java_manager.send_message(self.manual_settings_request)
        self.quote_adjustment.set_defaults().update_fields_in_component(
            "QuoteAdjustmentRequestBlock",
            {"InstrSymbol": self.eur_usd,
             "ClientTierID": self.silver_id})
        self.java_manager.send_message(self.quote_adjustment)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.manual_settings_request.set_default_params()
        self.java_manager.send_message(self.manual_settings_request)
        self.sleep(2)
