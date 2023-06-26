import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
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


class QAP_T11154(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.rest_api_security_block = RestApiManageSecurityBlock(self.data_set)
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: set up needed configuration for listing
        list_of_price = [4, 12]
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
        for price in list_of_price:
            try:
                new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                    self.fix_env.buy_side, self.venue_client_name, self.venue, float(price))
                self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                    JavaApiFields.ClOrdID.value: bca.client_orderid(9),
                    JavaApiFields.Price.value: price})
                self.java_api_manager.send_message_and_receive_response(self.order_submit)
            except Exception as e:
                logger.error(f'Exception: {e}', exc_info=True)
            finally:
                time.sleep(2)
                self.rule_manager.remove_rule(new_order_single)
            order_reply = self.java_api_manager.get_last_message(
                ORSMessageType.OrderReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                 JavaApiFields.Price.value: str(float(price))},
                order_reply,
                f'Verifying that order created and has properly price (step {list_of_price.index(price) + 1})')
        # endregion
