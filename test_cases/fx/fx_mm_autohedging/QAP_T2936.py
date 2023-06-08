from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T2936(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.trade_request = TradeEntryRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.client_ext = self.data_set.get_client_by_name("client_mm_8")
        self.account_ext = self.data_set.get_account_by_name("account_mm_8")
        self.client_int = self.data_set.get_client_by_name("client_int_5")
        self.account_int = self.data_set.get_account_by_name("account_int_5")
        self.qty = "1000000.53"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)

        # endregion
        # region Step 1-2
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.sleep(1)
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext,
                                                       "ExecQty": self.qty})
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ah_ordr_id = self.trade_request.get_ah_ord_id(response)

        # endregion
        # region Step 3
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameter("Account", self.client_int)
        self.ah_order.change_parameter("ClOrdID", ah_ordr_id)
        key_params = ["Misc0", "OrderQty"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order,key_parameters=key_params,
                                                      message_name="Check tha we create AH with decimals Qty")
