from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class QuoteManagementRequest(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=QSMessageType.QuoteManagementRequest.value)
        super().change_parameters(parameters)

    def set_default(self, listing_id, offer_px=None, bid_px=None, off_size=None, bid_size=None,
                    notional_amt=None, side=None, th_px=None, th_offer_px=None, th_bid_px=None):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.QS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.QS',
            'QuoteManagementRequestBlock': {
                'QuoteManagementList': {"QuoteManagementBlock": [{
                    "OfferPx": "10",
                    "BidPx": "10",
                    "CDOrdFreeNotes": "MMM",
                    "ListingID": listing_id,

                }]}
            }
        }
        block = base_parameters['QuoteManagementRequestBlock']['QuoteManagementList']["QuoteManagementBlock"][0]
        if offer_px: block["OfferPx"] = offer_px
        if bid_px: block["BidPx"] = bid_px
        if off_size: block["OfferSize"] = off_size
        if bid_size: block["BidSize"] = bid_size
        if notional_amt: block["NotionalAmt"] = notional_amt
        if th_px: block["TheoreticalPx"] = th_px
        if th_offer_px: block["TheoreticalOfferPx"] = th_offer_px
        if th_bid_px: block["TheoreticalBidPx"] = th_bid_px
        if side: block["Side"] = side
        super().change_parameters(base_parameters)
        return self
