from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageOrderCancelRequestFX import FixMessageOrderCancelRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixOrderCancelRequestFX import FixOrderCancelRequestFX
from test_framework.java_api_wrappers.fx.FixOrderModificationRequestFX import FixOrderModificationRequestFX
from test_framework.java_api_wrappers.fx.OrderModificationRequestFX import OrderModificationRequestFX
from test_framework.java_api_wrappers.fx.OrderSubmitFX import OrderSubmitFX
from test_framework.java_api_wrappers.fx.OrderValidateFX import OrderValidateFX


class QAP_T3094(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.env = self.environment.get_list_fix_environment()[0]
        self.fix_env = self.env.buy_side_esp
        self.fix_manager_taker = FixManager(self.fix_env, self.test_id)
        self.new_order_single = OrderSubmitFX(data_set=self.data_set)
        self.fix_order_modify = FixOrderModificationRequestFX(data_set=self.data_set)
        self.order_modify = OrderModificationRequestFX(data_set=self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.verifier = Verifier(self.test_id)
        self.order_cancel = FixOrderCancelRequestFX(data_set=self.data_set)
        self.fix_order_cancel = FixMessageOrderCancelRequestFX()
        self.client = self.data_set.get_client_by_name("client_5")
        self.account = self.data_set.get_account_by_name("account_5")
        self.order_qty = "10000000"
        self.cl_ord_id = str()
        self.listing_citi = {'ListingBlock': [
            {"ListingID": "100000249"}]}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.new_order_single.set_default_dma_limit()
        self.new_order_single.update_fields_in_component("NewOrderSingleBlock",
                                                         {"Price": "1.17164",
                                                          "ListingList": self.listing_citi,
                                                          "TimeInForce": "IOC", "AccountGroupID": "ASPECT_CITI"})
        self.java_api_manager.send_message_and_receive_response(self.new_order_single)
        ord_notification = self.java_api_manager.get_last_message("Order_OrdReply")
        self.ord_id = ord_notification.get_parameter("OrdReplyBlock")["OrdID"]
        initial_tif = ord_notification.get_parameter("OrdReplyBlock")["TimeInForce"]
        self.cl_ord_id = ord_notification.get_parameter("OrdReplyBlock")["ClOrdID"]
        # self.order_modify.set_modify_order_limit(self.ord_id, qty="1000000", price="1.18164")
        # self.order_modify.update_fields_in_component("OrderModificationRequestBlock", {"TimeInForce": "GTC"})
        # self.java_api_manager.send_message_and_receive_response(self.order_modify)
        # ord_notification = self.java_api_manager.get_last_message("Order_OrdReply")
        # modified_tif = ord_notification.get_parameter("OrdReplyBlock")["TimeInForce"]
        self.fix_order_modify.set_modify_order_limit(self.cl_ord_id, qty="1000000", price="1.18164")
        self.fix_order_modify.update_fields_in_component("OrderModificationRequestBlock", {"TimeInForce": "GTC"})
        self.java_api_manager.send_message_and_receive_response(self.fix_order_modify)
        ord_notification = self.java_api_manager.get_last_message("Order_OrdReply")
        modified_tif = ord_notification.get_parameter("OrdReplyBlock")["TimeInForce"]
        self.verifier.set_event_name("Check Order qty and Order status after Order Release")
        self.verifier.compare_values("Order tif before modification", "IOC", initial_tif)
        self.verifier.compare_values("Order tif after modification", "DAY", modified_tif)
        self.verifier.verify()
