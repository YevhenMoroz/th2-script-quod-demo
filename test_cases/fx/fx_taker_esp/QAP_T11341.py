from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_value_in_db
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.ExecutePricedOrderRequestFX import ExecutePricedOrderRequestFX
from test_framework.java_api_wrappers.fx.OrderSubmitFX import OrderSubmitFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiOrderCompressionMessages import RestApiOrderCompressionMessages
from test_framework.rest_api_wrappers.forex.RestApiOrderPricingMessages import RestApiOrderPricingMessages


class QAP_T11341(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitFX(self.data_set)
        self.order_pricing = RestApiOrderPricingMessages()
        self.execute_priced_order_request = ExecutePricedOrderRequestFX(data_set=self.data_set)
        self.order_compression = RestApiOrderCompressionMessages()
        self.client_buy_poc = self.data_set.get_client_by_name("client_6")
        self.random_qty_1 = randint(3000000, 4000000)
        self.random_qty_2 = randint(1000000, 2000000)
        self.random_qty_3 = randint(1000000, 2000000)
        self.random_qty_4 = randint(1000000, 2000000)
        self.random_qty_5 = randint(1000000, 2000000)
        self.mo_qty = str(self.random_qty_1 - self.random_qty_2)
        self.mo_qty = str(self.random_qty_1 - self.random_qty_2)
        self.seconds_wait = 60
        self.time = datetime.now() - timedelta(hours=2) + timedelta(seconds=self.seconds_wait)
        self.iso_time = self.time.isoformat().rsplit("T")[1].rsplit(".")[0]
        self.verifier = Verifier()
        self.order_compression_message = {"accountGroupID": self.client_buy_poc, "clientGroupID": "1",
                                          "enableCompression": "true", "executionDelay": "1",
                                          "orderCompressionID": "600040",
                                          "orderCompressionName": self.client_buy_poc,
                                          "orderCompressionTimeTable": [{"compressionTime": self.iso_time}]}
        self.order_pricing_message = {"accountGroupID": self.client_buy_poc, "alive": "true", "clientGroupID": "1",
                                      "orderPricingID": "400013", "orderPricingName": self.client_buy_poc,
                                      "pricingAgreement": "BEN", "rateMethodology": "MID",
                                      "rateSourceClientTierID": "4"}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step preparation
        self.order_pricing.set_params(self.order_pricing_message).modify_order_pricing()
        self.rest_manager.send_post_request(self.order_pricing)
        self.order_compression.set_params(self.order_compression_message).modify_order_compression()
        self.rest_manager.send_post_request(self.order_compression)
        self.sleep(0.5)
        # endregion
        # region Step 1
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_1
        self.java_api_manager.send_message(self.submit_request)
        # endregion
        # region Step 2
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_2
        self.submit_request.get_parameter("NewOrderSingleBlock")["Side"] = "Sell"
        self.java_api_manager.send_message(self.submit_request)
        # endregion
        # region Step 3
        self.sleep(self.seconds_wait + 2)
        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.mo_qty}")
        price = check_value_in_db(extracting_value="price",
                                  query=f"SELECT price FROM ordr "
                                        f"WHERE ordqty = {self.mo_qty}")
        self.execute_priced_order_request.set_default_params(order_id)
        self.java_api_manager.send_message(self.execute_priced_order_request)
        self.sleep(0.5)
        status = check_value_in_db(extracting_value="transstatus",
                                   query=f"SELECT transstatus FROM transac "
                                         f"WHERE ordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Compressed Order")
        self.verifier.compare_values("price", "1.180000000", str(price))
        self.verifier.compare_values("status", "TER", status)
        self.verifier.verify()
        # endregion
        # region Step 4
        self.time = datetime.now() - timedelta(hours=2) + timedelta(seconds=self.seconds_wait)
        self.iso_time = self.time.isoformat().rsplit("T")[1].rsplit(".")[0]
        self.order_compression_message.update({"enableCompression": "false",
                                               "orderCompressionTimeTable": [{"compressionTime": self.iso_time}]})
        self.order_compression.set_params(self.order_compression_message).modify_order_compression()
        self.rest_manager.send_post_request(self.order_compression)
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_3
        self.java_api_manager.send_message(self.submit_request)
        self.sleep(self.seconds_wait + 2)
        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.random_qty_3} AND origin = 'INT'")
        self.execute_priced_order_request.set_default_params(order_id)
        self.java_api_manager.send_message(self.execute_priced_order_request)
        self.sleep(0.5)
        status = check_value_in_db(extracting_value="transstatus",
                                   query=f"SELECT transstatus FROM transac "
                                         f"WHERE ordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Compressed Order")
        self.verifier.compare_values("price", "1.180000000", str(price))
        price = check_value_in_db(extracting_value="price",
                                  query=f"SELECT price FROM ordr "
                                        f"WHERE ordqty = {self.random_qty_3} AND origin = 'INT'")
        self.verifier.compare_values("status", "TER", status)
        self.verifier.verify()
        # endregion
        # region Step 5
        self.time = datetime.now() - timedelta(hours=2) + timedelta(seconds=self.seconds_wait)
        self.iso_time = self.time.isoformat().rsplit("T")[1].rsplit(".")[0]
        self.order_compression_message.update({"enableCompression": "false",
                                               "orderCompressionTimeTable": [{"compressionTime": self.iso_time}]})
        self.order_compression.set_params(self.order_compression_message).modify_order_compression()
        self.rest_manager.send_post_request(self.order_compression)
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_3
        self.java_api_manager.send_message(self.submit_request)
        self.time = datetime.now() - timedelta(hours=2) + timedelta(seconds=self.seconds_wait)
        self.iso_time = self.time.isoformat().rsplit("T")[1].rsplit(".")[0]
        self.order_compression_message.update({"enableCompression": "false",
                                               "orderCompressionTimeTable": [{"compressionTime": self.iso_time}]})
        self.order_compression.set_params(self.order_compression_message).modify_order_compression()
        self.rest_manager.send_post_request(self.order_compression)
        # endregion
        # region Step 6
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_4
        self.java_api_manager.send_message(self.submit_request)
        self.sleep(self.seconds_wait + 2)
        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.random_qty_3} AND origin = 'INT'")
        self.execute_priced_order_request.set_default_params(order_id)
        self.java_api_manager.send_message(self.execute_priced_order_request)
        self.sleep(0.5)
        status = check_value_in_db(extracting_value="transstatus",
                                   query=f"SELECT transstatus FROM transac "
                                         f"WHERE ordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Compressed Order")
        self.verifier.compare_values("price", "1.180000000", str(price))
        price = check_value_in_db(extracting_value="price",
                                  query=f"SELECT price FROM ordr "
                                        f"WHERE ordqty = {self.random_qty_3} AND origin = 'INT'")
        self.verifier.compare_values("status", "TER", status)
        self.verifier.verify()
        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.random_qty_4} AND origin = 'INT'")
        self.execute_priced_order_request.set_default_params(order_id)
        self.java_api_manager.send_message(self.execute_priced_order_request)
        self.sleep(0.5)
        status = check_value_in_db(extracting_value="transstatus",
                                   query=f"SELECT transstatus FROM transac "
                                         f"WHERE ordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Compressed Order")
        self.verifier.compare_values("price", "1.180000000", str(price))
        price = check_value_in_db(extracting_value="price",
                                  query=f"SELECT price FROM ordr "
                                        f"WHERE ordqty = {self.random_qty_4} AND origin = 'INT'")
        self.verifier.compare_values("status", "TER", status)
        self.verifier.verify()
        # endregion
        # region Step 7-8
        self.time = datetime.now() - timedelta(hours=2) + timedelta(seconds=self.seconds_wait)
        self.iso_time = self.time.isoformat().rsplit("T")[1].rsplit(".")[0]
        self.order_compression_message.update({"enableCompression": "true",
                                               "orderCompressionTimeTable": [{"compressionTime": self.iso_time}]})
        self.order_compression.set_params(self.order_compression_message).modify_order_compression()
        self.rest_manager.send_post_request(self.order_compression)
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_3
        self.java_api_manager.send_message(self.submit_request)
        self.time = datetime.now() - timedelta(hours=2) + timedelta(seconds=self.seconds_wait)
        self.iso_time = self.time.isoformat().rsplit("T")[1].rsplit(".")[0]
        self.order_compression_message.update({"enableCompression": "true",
                                               "orderCompressionTimeTable": [{"compressionTime": self.iso_time}]})
        self.order_compression.set_params(self.order_compression_message).modify_order_compression()
        self.rest_manager.send_post_request(self.order_compression)
        # endregion
        # region Step 9
        self.submit_request.set_default_care().get_parameter("NewOrderSingleBlock")["OrdQty"] = self.random_qty_4
        self.java_api_manager.send_message(self.submit_request)
        self.sleep(self.seconds_wait + 2)
        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.random_qty_3} AND origin = 'INT'")
        self.execute_priced_order_request.set_default_params(order_id)
        self.java_api_manager.send_message(self.execute_priced_order_request)
        self.sleep(0.5)
        status = check_value_in_db(extracting_value="transstatus",
                                   query=f"SELECT transstatus FROM transac "
                                         f"WHERE ordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Compressed Order")
        self.verifier.compare_values("price", "1.180000000", str(price))
        price = check_value_in_db(extracting_value="price",
                                  query=f"SELECT price FROM ordr "
                                        f"WHERE ordqty = {self.random_qty_3} AND origin = 'INT'")
        self.verifier.compare_values("status", "TER", status)
        self.verifier.verify()

        order_id = check_value_in_db(extracting_value="ordid",
                                     query=f"SELECT ordid FROM ordr "
                                           f"WHERE ordqty = {self.random_qty_4} AND origin = 'INT'")
        self.execute_priced_order_request.set_default_params(order_id)
        self.java_api_manager.send_message(self.execute_priced_order_request)
        self.sleep(0.5)
        status = check_value_in_db(extracting_value="transstatus",
                                   query=f"SELECT transstatus FROM transac "
                                         f"WHERE ordid = '{order_id}'")
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check Compressed Order")
        self.verifier.compare_values("price", "1.180000000", str(price))
        price = check_value_in_db(extracting_value="price",
                                  query=f"SELECT price FROM ordr "
                                        f"WHERE ordqty = {self.random_qty_4} AND origin = 'INT'")
        self.verifier.compare_values("status", "TER", status)
        self.verifier.verify()
        # endregion