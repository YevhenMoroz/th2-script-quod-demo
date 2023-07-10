from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_value_in_db
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.fix_wrappers.forex.FixMessageOrderCancelRequestFX import FixMessageOrderCancelRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixNewOrderSingleFX import FixNewOrderSingleFX
from test_framework.java_api_wrappers.fx.FixOrderCancelRequestFX import FixOrderCancelRequestFX
from test_framework.java_api_wrappers.fx.FixOrderModificationRequestFX import FixOrderModificationRequestFX
from test_framework.java_api_wrappers.fx.OrderSubmitFX import OrderSubmitFX


class QAP_T2618(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.env = self.environment.get_list_fix_environment()[0]
        self.fix_env = self.env.buy_side_esp
        self.fix_manager_taker = FixManager(self.fix_env, self.test_id)
        self.new_order_single = OrderSubmitFX(data_set=self.data_set)
        self.order_modify = FixOrderModificationRequestFX(data_set=self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.verifier = Verifier(self.test_id)
        self.order_cancel = FixOrderCancelRequestFX(data_set=self.data_set)
        self.fix_order_cancel = FixMessageOrderCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_5")
        self.account = self.data_set.get_account_by_name("account_5")
        self.order_qty = "10000000"
        self.cl_ord_id = str()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.new_order_single.set_passive_algo()
        self.java_api_manager.send_message_and_receive_response(self.new_order_single)
        initial_qty = self.java_api_manager.get_last_message("Order_OrdReply").get_parameter("OrdReplyBlock")["OrdQty"]
        initial_qty = str(float(initial_qty))
        initial_status = self.java_api_manager.get_last_message("Order_OrdReply").get_parameter("OrdReplyBlock")[
            "TransStatus"]
        self.cl_ord_id = self.new_order_single.get_parameter("NewOrderSingleBlock")["ClOrdID"]
        self.order_modify.set_modify_order_limit(self.cl_ord_id, qty="50000000")
        self.java_api_manager.send_message_and_receive_response(self.order_modify)
        self.java_api_manager.get_last_message("Order_OrdReply")
        modified_qty = self.java_api_manager.get_last_message("Order_OrdReply").get_parameter("OrdReplyBlock")["OrdQty"]
        modified_qty = str(float(modified_qty))
        self.order_cancel.set_default_cancel(self.cl_ord_id)
        self.java_api_manager.send_message_and_receive_response(self.order_cancel)
        modified_status = self.java_api_manager.get_last_message("Order_OrdReply").get_parameter("OrdReplyBlock")[
            "TransStatus"]
        self.verifier.set_event_name("Check Order qty after modify and Order status after cancel")
        self.verifier.compare_values("Order qty before modification", "90000000.0", initial_qty)
        self.verifier.compare_values("Order qty after modification", "50000000.0", modified_qty)
        self.verifier.compare_values("Order status before cancel", "OPN", initial_status)
        self.verifier.compare_values("Order status after cancel", "CXL", modified_status)
        self.verifier.verify()
