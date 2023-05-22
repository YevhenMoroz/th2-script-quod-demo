from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.FixRequestForPositionsFX import FixRequestForPositionsFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T11216(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixRequestForPositionsFX()
        self.position_report = FixMessageRequestForPositionsAckFX()
        self.trade_request_wk1 = TradeEntryRequestFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_mm_7")
        self.account = self.data_set.get_account_by_name("account_mm_7")
        self.listing_gbp_cad_wk1 = self.data_set.get_listing_id_by_name("gbp_cad_wk1")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.sec_type_java = self.data_set.get_fx_instr_type_ja("fx_fwd")
        self.instrument = {
            "SecurityType": self.sec_type_fwd,
            "Symbol": self.gbp_cad
        }
        self.settle_date_wk1 = self.data_set.get_settle_date_by_name("wk1_java_api")
        self.maintenance_request = FixPositionMaintenanceRequestFX()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        # self.trade_request_wk1.set_params_for_fwd()
        # self.trade_request_wk1.update_fields_in_component("TradeEntryRequestBlock",
        #                                                   {"AccountGroupID": self.client,
        #                                                    "SettlDate": self.settle_date_wk1,
        #                                                    "ListingID": self.listing_gbp_cad_wk1})
        # self.java_api_manager.send_message_and_receive_response(self.trade_request_wk1)
        #
        # # endregion
        #
        # # region Step 2
        # self.cancel_request.set_params(self.account)
        # self.java_api_manager.send_message(self.cancel_request)
        # self.sleep(5)
        #
        # # endregion

        # region Step 3
        self.request_for_position.set_default_params()
        response = self.java_api_manager.send_message_and_receive_response(self.request_for_position)
        for i in response:
            print(i.get_parameters())
        # print(response.get_parameters())
        self.sleep(1)
        # self.request_for_position.set_default_params()
        # self.request_for_position.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
        #                                              "Account": self.client})
        # self.java_api_manager.send_message_and_receive_response(self.request_for_position, self.test_id)
        # # endregion

        # # region Step 4
        # self.position_report.set_params_for_none(self.request_for_position)
        #
        # self.fix_verifier.check_fix_message(self.position_report)
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.sleep(2)
        self.request_for_position.unsubscribe()
        self.java_api_manager.send_message(self.request_for_position)
