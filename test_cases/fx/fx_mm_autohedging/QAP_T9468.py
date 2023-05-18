from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX


class QAP_T9468(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.trade_request = TradeEntryRequestFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.mo_order = FixMessageNewOrderSingleTakerDC()
        self.client_ext = self.data_set.get_client_by_name("client_mm_8")
        self.client_int = self.data_set.get_client_by_name("client_int_5")
        self.execMisc1 = "execMisc1"
        self.execMisc2 = "execMisc2"
        self.execMisc3 = "execMisc3"
        self.execMisc4 = "execMisc4"
        self.execMisc5 = "execMisc5"
        self.execMisc6 = "execMisc6"
        self.execMisc7 = "execMisc7"
        self.execMisc8 = "execMisc8"
        self.execMisc9 = "execMisc9"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 3
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.sleep(1)
        self.trade_request.set_default_params()
        self.trade_request.set_exec_misc1(self.execMisc1)
        self.trade_request.set_exec_misc2(self.execMisc2)
        self.trade_request.set_exec_misc3(self.execMisc3)
        self.trade_request.set_exec_misc4(self.execMisc4)
        self.trade_request.set_exec_misc5(self.execMisc5)
        self.trade_request.set_exec_misc6(self.execMisc6)
        self.trade_request.set_exec_misc7(self.execMisc7)
        self.trade_request.set_exec_misc8(self.execMisc8)
        self.trade_request.set_exec_misc9(self.execMisc9)
        self.sleep(1)
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {"ClientAccountGroupID": self.client_ext})
        self.java_api_manager.send_message_and_receive_response(self.trade_request)

        # endregion
        # region Step 5
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameter("Account", self.client_int)
        self.ah_order.add_tag({"Misc1": self.execMisc1})
        self.ah_order.add_tag({"Misc2": self.execMisc2})
        self.ah_order.add_tag({"Misc3": self.execMisc3})
        self.ah_order.add_tag({"Misc4": self.execMisc4})
        self.ah_order.add_tag({"Misc5": self.execMisc5})
        self.ah_order.add_tag({"Misc6": self.execMisc6})
        self.ah_order.add_tag({"Misc7": self.execMisc7})
        self.ah_order.add_tag({"Misc8": self.execMisc8})
        self.ah_order.add_tag({"Misc9": self.execMisc9})
        self.mo_order.set_default_mo_from_trade(self.trade_request)
        self.mo_order.change_parameter("Account", self.client_int)
        self.mo_order.add_tag({"Misc1": self.execMisc1})
        self.mo_order.add_tag({"Misc2": self.execMisc2})
        self.mo_order.add_tag({"Misc3": self.execMisc3})
        self.mo_order.add_tag({"Misc4": self.execMisc4})
        self.mo_order.add_tag({"Misc5": self.execMisc5})
        self.mo_order.add_tag({"Misc6": self.execMisc6})
        self.mo_order.add_tag({"Misc7": self.execMisc7})
        self.mo_order.add_tag({"Misc8": self.execMisc8})
        self.mo_order.add_tag({"Misc9": self.execMisc9})
        prefilter = {
            "header": {
                "MsgType": ("D", "EQUAL"),
            }
        }
        key_params = ["Misc0"]
        self.fix_drop_copy_verifier.check_fix_message_sequence([self.ah_order, self.mo_order],
                                                               key_parameters_list=[key_params, key_params],
                                                               pre_filter=prefilter,
                                                               message_name="Check that Misc feilds transfered to AH and his child")
        # endregion
