from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T10760(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.position_report = FixMessagePositionReportFX()
        self.trade_request = TradeEntryRequestFX()
        self.trade_request_wk1 = TradeEntryRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.listing_gbp_cad = self.data_set.get_listing_id_by_name("gbp_cad_spo")
        self.listing_gbp_cad_wk1 = self.data_set.get_listing_id_by_name("gbp_cad_wk1")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.spot = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "SecurityType": self.spot,
            "Symbol": self.gbp_cad
        }
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1_java_api")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send Trade to have position
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"AccountGroupID": self.client,
                                                                                 "ListingID": self.listing_gbp_cad})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_id = self.trade_request.get_exec_id(response)
        self.sleep(3)
        # endregion
        # region Step 2
        self.request_for_position.set_default()
        self.request_for_position.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                     "Account": self.client})
        self.fix_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        # endregion
        # region Step 3
        # TODO add Check RequestForPositionsAck
        # endregion
        # region Step 4
        self.trade_request_wk1.set_default_params()
        self.trade_request_wk1.update_fields_in_component("TradeEntryRequestBlock",
                                                          {"AccountGroupID": self.client,
                                                           "SettlDate": self.settle_date_wk1,
                                                           "ListingID": self.listing_gbp_cad_wk1})
        self.java_api_manager.send_message_and_receive_response(self.trade_request_wk1)
        # endregion
        # region Step 5
        self.position_report.set_params_from_reqeust(self.request_for_position)
        self.position_report.change_parameter("LastPositUpdateEventID", exec_id)
        prefilter = {
            "header": {
                "MsgType": ("AP", "EQUAL"),
                "TargetCompID": "PKSTH2",
                "SenderCompID": "QUODFX_UAT"
            }
        }
        key_params = ["PosReqID"]
        self.fix_verifier.check_fix_message_sequence([self.position_report], key_parameters_list=[key_params],
                                                     pre_filter=prefilter,
                                                     message_name="Check that we receive only One report")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position)
