from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ListingQuotingModificationRequest(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=QSMessageType.ListingQuotingModificationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, listing_id, quoting_method="AUT", ref_spread_px_type=None, bid_spread=None,
                    offer_spead=None, spread_px_type=None, quoting_px_ref_type=None):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.QS.FE',
            'REPLY_SUBJECT': 'QUOD.QS.SPREAD',
            'ListingQuotingModificationRequestBlock': {
                "ListingID": listing_id,
                "QuotingMethod": quoting_method
            }
        }
        block = base_parameters['ListingQuotingModificationRequestBlock']
        if ref_spread_px_type: block["RefSpreadPriceType"] = ref_spread_px_type
        if bid_spread: block["BidSpread"] = bid_spread
        if offer_spead: block["OfferSpread"] = offer_spead
        if spread_px_type: block["SpreadPriceType"] = spread_px_type
        if quoting_px_ref_type: block["QuotingPriceReferenceType"] = quoting_px_ref_type
        super().change_parameters(base_parameters)
        return self
