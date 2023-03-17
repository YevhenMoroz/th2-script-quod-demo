import time
from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_T2402(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.modify_client_tier = RestApiClientTierMessages()
        self.modify_instrument = RestApiClientTierInstrSymbolMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject = FixMessageQuoteRequestRejectFX()
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.client_id = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type = self.data_set.get_settle_type_by_name("today")
        self.settle_date = self.data_set.get_settle_date_by_name("today")
        self.msg_prams_client = None
        self.msg_prams_instr = None
        self.gbp_usd_fwd = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type
        }
        self.eur_usd_fwd = {
            "Symbol": self.eur_usd,
            "SecurityType": self.security_type
        }
        self.expected_error_id = "11900"
        self.bands_gbp_usd = ["1000000"]
        self.time_client_1 = (datetime.now() - timedelta(hours=4))
        self.time_client_2 = (datetime.now() + timedelta(hours=4))
        self.timestamp_client_1 = str(datetime.timestamp(self.time_client_1)).replace(".", "")[:13]
        self.timestamp_client_2 = str(datetime.timestamp(self.time_client_2)).replace(".", "")[:13]
        self.time_instr_1 = (datetime.now() - timedelta(hours=2))
        self.time_instr_2 = (datetime.now() - timedelta(hours=1))
        self.timestamp_instr_1 = str(datetime.timestamp(self.time_instr_1)).replace(".", "")[:13]
        self.timestamp_instr_2 = str(datetime.timestamp(self.time_instr_2)).replace(".", "")[:13]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.modify_client_tier.find_client_tier(self.client_id)
        self.msg_prams_client = self.rest_manager.send_get_request_filtered(self.modify_client_tier)
        self.msg_prams_client = self.rest_manager.parse_response_details(self.msg_prams_client,
                                                                         {"clientTierID": self.client_id})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams_client) \
            .add_parameters({"TODStartTime": self.timestamp_client_1, "TODEndTime": self.timestamp_client_2})
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.modify_instrument.find_client_tier_instrument(self.client_id, self.gbp_usd)
        self.msg_prams_instr = self.rest_manager.send_get_request_filtered(self.modify_instrument)
        self.msg_prams_instr = self.rest_manager. \
            parse_response_details(self.msg_prams_instr, {"clientTierID": self.client_id, "instrSymbol": self.gbp_usd})
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(
            self.msg_prams_instr).add_parameters(
            {"TODStartTime": self.timestamp_instr_1, "TODEndTime": self.timestamp_instr_2})
        self.rest_manager.send_post_request(self.modify_instrument)
        time.sleep(5)
        # endregion

        # region Step 2
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.client,
                                                           Currency="GBP", Instrument=self.gbp_usd_fwd,
                                                           SettlType=self.settle_type, SettlDate=self.settle_date)
        response = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 3
        self.quote_reject.set_quote_reject_params(self.quote_request)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(self.quote_reject)
        error_id = response[0].get_parameter("Text").split()[0]
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check error ID")
        self.verifier.compare_values("Error ID", self.expected_error_id, error_id)
        self.verifier.verify()
        # endregion

        # region Step 3
        self.modify_client_tier.remove_parameters(["TODStartTime", "TODEndTime"])
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.modify_instrument.remove_parameters(["TODStartTime", "TODEndTime"])
        self.rest_manager.send_post_request(self.modify_instrument)
        time.sleep(5)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.client,
                                                           Currency="GBP", Instrument=self.gbp_usd_fwd,
                                                           SettlType=self.settle_type, SettlDate=self.settle_date)
        response = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 3
        self.quote.set_params_for_quote(self.quote_request)
        self.quote.change_parameter("OfferForwardPoints", "*")
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 5
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.client,
                                                           Currency="EUR", Instrument=self.eur_usd_fwd)
        self.response = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 6
        self.quote.set_params_for_quote(self.quote_request)
        self.quote.change_parameter("OfferForwardPoints", "*")
        self.fix_verifier.check_fix_message(self.quote)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
