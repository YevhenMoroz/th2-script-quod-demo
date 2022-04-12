import time
from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages
from test_framework.rest_api_wrappers.forex.RestApiClientTierMessages import RestApiClientTierMessages


class QAP_7287(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.modify_client_tier = RestApiClientTierMessages()
        self.modify_instrument = RestApiClientTierInstrSymbolMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject = FixMessageQuoteRequestRejectFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_today = self.data_set.get_settle_date_by_name("today")
        self.settle_type_today = self.data_set.get_settle_type_by_name("today")
        self.client_id = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.msg_prams_client = None
        self.msg_prams_instr = None
        self.qty = "1000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.current_time = datetime.now().strftime("%H:%M:%S.%f")
        self.time_client_1 = (datetime.now() - timedelta(hours=4))
        self.time_client_2 = (datetime.now() + timedelta(hours=4))
        self.timestamp_client_1 = str(datetime.timestamp(self.time_client_1)).replace(".", "")[:13]
        self.timestamp_client_2 = str(datetime.timestamp(self.time_client_2)).replace(".", "")[:13]
        self.time_instr_1 = (datetime.now() - timedelta(hours=2))
        self.time_instr_2 = (datetime.now() - timedelta(hours=1))
        self.timestamp_instr_1 = str(datetime.timestamp(self.time_instr_1)).replace(".", "")[:13]
        self.timestamp_instr_2 = str(datetime.timestamp(self.time_instr_2)).replace(".", "")[:13]
        self.text = f"11900 Validation failed: current time ({self.current_time}) > end time ({self.time_instr_2})"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.modify_client_tier.find_all_client_tier()
        self.msg_prams_client = self.rest_manager.send_get_request(self.modify_client_tier)
        self.msg_prams_client = self.rest_manager.parse_response_details(self.msg_prams_client,
                                                                         {"clientTierID": self.client_id})
        self.modify_client_tier.clear_message_params().modify_client_tier().set_params(self.msg_prams_client) \
            .change_params({"TODStartTime": self.timestamp_client_1, "TODEndTime": self.timestamp_client_2})
        self.rest_manager.send_post_request(self.modify_client_tier)
        # endregion
        # region Step 2
        self.modify_instrument.find_all_client_tier_instrument()
        self.msg_prams_instr = self.rest_manager.send_get_request(self.modify_instrument)
        self.msg_prams_instr = self.rest_manager. \
            parse_response_details(self.msg_prams_instr, {"clientTierID": self.client_id, "instrSymbol": self.symbol})
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(self.msg_prams_instr) \
            .change_params({"TODStartTime": self.timestamp_instr_1, "TODEndTime": self.timestamp_instr_2})
        self.rest_manager.send_post_request(self.modify_instrument)
        time.sleep(5)
        # endregion
        # region Step 3
        self.quote_request.set_rfq_params_fwd()

        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency="GBP", Instrument=self.instrument,
                                                           OrderQty=self.qty, SettlDate=self.settle_date_today,
                                                           SettlType=self.settle_type_today)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 4
        self.quote_reject.set_quote_reject_params(self.quote_request, text=self.text)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(fix_message=self.quote_reject, key_parameters=["QuoteReqID"])
        # endregion

    def run_post_conditions(self):
        self.modify_client_tier.remove_parameters(["TODStartTime", "TODEndTime"])
        self.rest_manager.send_post_request(self.modify_client_tier)
        self.modify_instrument.remove_parameters(["TODStartTime", "TODEndTime"])
        self.rest_manager.send_post_request(self.modify_instrument)

