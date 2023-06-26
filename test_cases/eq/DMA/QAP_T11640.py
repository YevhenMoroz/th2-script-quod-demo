import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiManageSecurityBlock import RestApiManageSecurityBlock

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T11640(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.rest_api_security_block = RestApiManageSecurityBlock(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: set up needed configuration for listing
        list_of_price = [4, 10]
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_11_collar_eurex')
        listing_id = self.data_set.get_listing_id_by_name('listing_11_collar_eurex')
        params_for_listing = {"listingID": listing_id, "algoIncluded": 'true', "instrID": instrument_id,
                              "instrCurrency": "GBp", "preferredVenueID": "EUREX",
                              "tickSizeProfileID": 3, "currency": "GBp", "symbol": "EUR_COLLAR",
                              "instrSymbol": "ISI3_COLLAR",
                              "securityID": "ISI3_COLLAR", "securityIDSource": "ISI",
                              "lookupSymbol": "EUR[EUREX]_COLLAR", "ISINSecurityAltID": "IS0000000001_COLLAR",
                              "exchSymbSecurityAltID": "IS0000000001_COLLAR",
                              "securityExchange": "XEUR", "USDDirectQuotation2": 'false',
                              "USDDirectQuotation1": 'false',
                              "EURDirectQuotation2": 'false', "EURDirectQuotation1": 'false',
                              "crossThroughUSD": 'false', "crossThroughEUR": 'false', "crossThroughUSDToEUR": 'false',
                              "crossThroughEURToUSD": 'false', "instrType": "EQU",
                              "orderBookVisibility": "V", "impliedInSupport": 'false', "venueID": "EUREX",
                              "asyncIndicator": 'false',
                              "preferredSecurityExchange": "XEUR",
                              "stampFeeExemption": 'false', "levyFeeExemption": 'false',
                              "perTransacFeeExemption": 'false', "collarDown": list_of_price[0],
                              "collarUp": list_of_price[1],
                              "alive": 'true'}
        self.rest_api_security_block.update_parameters(params_for_listing)
        self.rest_api_manager.send_post_request(self.rest_api_security_block)
        # endregion

        # region Create DMA orders : Step 1-2
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.InstrID.value: instrument_id,
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_id}]}})
        list_of_prices_for_order = ['3.0', '11.0']
        for price in list_of_prices_for_order:
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                JavaApiFields.ClOrdID.value:bca.client_orderid(9),
                JavaApiFields.Price.value: price})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_submit_reply = self.java_api_manager.get_last_message(
                ORSMessageType.OrderSubmitReply.value).get_parameters()
            self.java_api_manager.compare_values(
                {JavaApiFields.ErrorMsg.value: 'Order price is not within RD collar range.'},
                order_submit_reply[JavaApiFields.MessageReply.value][
                    JavaApiFields.MessageReplyBlock.value][0],
                f'Verifying error message (step {list_of_prices_for_order.index(price) + 1})')
            self.java_api_manager.compare_values(
                {JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value,
                 JavaApiFields.Price.value: price},
                order_submit_reply[JavaApiFields.NewOrderReplyBlock.value][
                    JavaApiFields.Ord.value],
                f'Verifying that order is rejected (step {list_of_prices_for_order.index(price) + 1})')
        # endregion



