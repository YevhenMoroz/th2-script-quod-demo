from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportDropCopyFX import FixMessageExecutionReportDropCopyFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMaintenanceRequestFX import FixPositionMaintenanceRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T9220(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.trade_request = TradeEntryRequestFX()
        self.maintenance_request_int = FixPositionMaintenanceRequestFX()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.client_ext = self.data_set.get_client_by_name("client_mm_6")
        self.account_ext = self.data_set.get_account_by_name("account_mm_6")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_usd")
        self.usd_php = self.data_set.get_symbol_by_name("symbol_ndf_1")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_spo = self.data_set.get_settle_date_by_name("spo_ndf_java_api")
        self.listing_usd_php = self.data_set.get_listing_id_by_name("usd_php_spo")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.usd_php
        }

        self.exec_qty = "10000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start
        self.maintenance_request_int.set_default_params()
        self.maintenance_request_int.change_account(self.account_int)
        self.maintenance_request_int.change_client(self.client_int)
        self.maintenance_request_int.change_instrument(self.usd_php)
        self.maintenance_request_int.change_settle_date(self.settle_date_spo)
        self.java_api_manager.send_message(self.maintenance_request_int)
        self.sleep(5)

        # endregion

        # region Step 3
        self.trade_request.set_default_params()
        self.trade_request.remove_fields_from_component("TradeEntryRequestBlock", ["SettlDate"])
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"AccountGroupID": self.client_ext,
                                                                                 "ListingID": self.listing_usd_php,
                                                                                 "ExecQty": self.exec_qty,
                                                                                 "Currency": self.currency})
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion
        # region Step 4
        self.ah_exec_report.set_params_from_trade_new(self.trade_request)
        self.ah_exec_report.change_parameter("TargetStrategy", "1005")
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report, message_name="Check that AH send TWAP")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.java_api_manager.send_message(self.maintenance_request_int)
        self.sleep(5)
