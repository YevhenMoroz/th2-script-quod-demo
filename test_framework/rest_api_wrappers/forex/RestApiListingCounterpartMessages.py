from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiListingCounterpartMessages(RestApiMessages):

    def set_default_params(self, listing_id=None):
        if not listing_id:
            self.clear_message()
            self.parameters = {
                "listingID": "100000939"
            }
        return self

    def manage_listing_counterpart(self, listing_counterpart_record):
        """listing_counterpart_record example:
        listing_counterpart_record = [
                {
                    "counterpartID": 1000000,
                    "partyRole": "PBT,
                },
                {
                    "counterpartID": 1000000,
                    "partyRole": "CLI,
                }
            ]"""
        self.parameters.update({"listingCounterpartRecord": listing_counterpart_record})
        self.message_type = ResAPIMessageType.ManageListingCounterpart.value
        return self
