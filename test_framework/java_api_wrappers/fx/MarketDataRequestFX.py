from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import MDAMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class MarketDataRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=MDAMessageType.MarketDataRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params_sub(self):
        client_tier_id = self.get_data_set().get_client_tier_id_by_name("client_tier_id_1")
        # client_tier_id = "4"
        listing_id = self.get_data_set().get_listing_id_by_name("gbp_usd_spo")
        md_request_params = {
            "SEND_SUBJECT": "MDA.QUOD.PRICING.8.SUB",
            "REPLY_SUBJECT": f"MDA.{listing_id}.{client_tier_id}.D.PRICING.8",
            "MarketDataRequestBlock": {
                "MDReqID": bca.client_orderid(10),
                "MDSymbolList": {
                    "MDSymbolBlock": [
                        {
                            "ListingID": listing_id,
                            "MDSymbol": f"{listing_id}.{client_tier_id}",
                            "ClientTierID": client_tier_id,
                            "FeedType": "D",
                            "SubscriptionRequestType": "SUB",
                        }
                    ]
                }
            }
        }
        super().change_parameters(md_request_params)
        return self

    def unsubscribe(self):
        md_block = self.get_parameter("MarketDataRequestBlock")
        md_sym_block = md_block["MDSymbolList"]["MDSymbolBlock"][0]
        md_sym_block["SubscriptionRequestType"] = "UNS"
