from datetime import datetime, timedelta

from test_cases.fx.fx_wrapper.common_tools import generate_schedule
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiClientTierInstrSymbolMessages(RestApiMessages):

    def find_all_client_tier_instrument(self):
        self.clear_message_params()
        self.message_type = 'FindAllClientTierInstrSymbol'
        return self

    def modify_client_tier_instrument(self):
        self.message_type = 'ModifyClientTierInstrSymbol'
        return self

    def create_client_tier_instrument(self):
        self.message_type = 'CreateClientTierInstrSymbol'
        return self

    def disable_client_tier_instrument(self):
        self.message_type = 'DisableClientTierInstrSymbol'
        return self

    def set_defeault_params(self):
        self.parameters = {
            "instrSymbol": '',
            "quoteTTL": 120,
            "clientTierID": '',
            "alive": "true",
            'pricingMethod': '',
            "clientTierInstrSymbolQty": [
                {
                    "upperQty": 1000000,
                    "indiceUpperQty": 1,
                    "publishPrices": "true"
                },
                {
                    "upperQty": 2000000,
                    "indiceUpperQty": 2,
                    "publishPrices": "true"
                }
            ],
            "clientTierInstrSymbolTenor": [
                {
                    "tenor": "SPO",
                    "minSpread": None,
                    "maxSpread": '',
                    "marginPriceType": "PIP",
                    "lastUpdateTime": '',
                    "MDQuoteType": "TRD",
                    "activeQuote": "true",
                    "clientTierInstrSymbolTenorQty": [
                        {
                            "MDQuoteType": "TRD",
                            "activeQuote": "true",
                            "indiceUpperQty": 1,
                            'defaultBidMargin': 0,
                            'defaultOfferMargin': 0,
                        },
                        {
                            "MDQuoteType": "TRD",
                            "activeQuote": "true",
                            "indiceUpperQty": 2,
                            'defaultBidMargin': 0,
                            'defaultOfferMargin': 0,
                        }
                    ]
                }
            ],
            "clientTierInstrSymbolVenue": [
                {
                    "venueID": "HSBC"
                }
            ],
            "clientTierInstrSymbolActGrp": [
                {
                    "accountGroupID": ''
                }
            ],
            "clientTierInstrSymbolFwdVenue": [
                {
                    "venueID": "HSBC"
                },
                {
                    "venueID": "HSBCR"
                }
            ],
        }
        return self

    def add_sweepable_qty(self, sweepable_qty, default_bid_margin=None, default_offer_margin=None):
        qty_list = self.get_parameter('clientTierInstrSymbolQty')
        parent_indice_upper_qty = str(int(len(qty_list))+int(1))
        qty_list.append({
            "upperQty": str(sweepable_qty),
            "indiceUpperQty": str(int(len(qty_list))+int(1)),
            "publishPrices": "true"
        })
        tenors = self.get_parameter('clientTierInstrSymbolTenor')
        timestamp = str(datetime.now().timestamp())
        timestamp = timestamp.split(".", 1)
        timestamp = timestamp[0]
        for tenor in tenors:
            tenor["clientTierInstrSymbolTenorQty"].append({
                "upperQty": str(sweepable_qty),
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "indiceUpperQty": str(int(len(tenors))+int(1)),
                'defaultBidMargin': 0 if default_bid_margin is None else str(default_bid_margin),
                'defaultOfferMargin': 0 if default_offer_margin is None else str(default_offer_margin),
                'parentIndiceUpperQty': parent_indice_upper_qty,
                'editableQty': 'false',
                'publishPrices': 'true'
            })
            tenor.update({'lastUpdateTime': timestamp})
        self.update_parameters({'clientTierInstrSymbolQty': qty_list, 'clientTierInstrSymbolTenor': tenors})

    def set_sweepable_qty(self, sweepable_qty_list, default_bid_margin=None, default_offer_margin=None):
        timestamp = str(datetime.now().timestamp())
        timestamp = timestamp.split(".", 1)
        timestamp = timestamp[0]
        qty_list = []
        qty_list_tenor = []
        i = 1
        for qty in sweepable_qty_list:
            qty_list.append({
                "upperQty": str(qty),
                "indiceUpperQty": i,
                "publishPrices": "true"
            })
            qty_list_tenor.append({
                "upperQty": str(qty),
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "indiceUpperQty": i,
                'defaultBidMargin': 0 if default_bid_margin is None else str(default_bid_margin),
                'defaultOfferMargin': 0 if default_offer_margin is None else str(default_offer_margin),
                'parentIndiceUpperQty': i,
                'editableQty': 'false',
                'publishPrices': 'true'
            })
            i += 1
        tenors = self.get_parameter('clientTierInstrSymbolTenor')
        for tenor in tenors:
            tenor.update({"clientTierInstrSymbolTenorQty": qty_list_tenor, 'lastUpdateTime': timestamp})
        self.update_parameters({'clientTierInstrSymbolQty': qty_list, 'clientTierInstrSymbolTenor': tenors})
        return self

    def delete_sweepable_qty(self, qty_list_to_delete: list = None, indice_upper_qty_to_delete: list = None):
        # TODO: Add qty deletion
        # qty_list = self.get_parameter('clientTierInstrSymbolQty')
        # qty_id_list = set()
        # tenors = self.get_parameter('clientTierInstrSymbolTenor')
        # timestamp = str(datetime.now().timestamp())
        # timestamp = timestamp.split(".", 1)
        # timestamp = timestamp[0]
        # if qty_list_to_delete is not None:
        #     for qty_to_delete in qty_list_to_delete:
        #         id_to_delete = 0
        #         for qty in qty_list:
        #             if qty["upperQty"] == qty_to_delete:
        #                 qty_id_list.add(id_to_delete)
        #             id_to_delete += 1
        #     for id_to_delete in qty_id_list:
        #         qty_list.pop(id_to_delete)
        #
        # for tenor in tenors:
        #     tenor["clientTierInstrSymbolTenorQty"].append({
        #         "upperQty": str(sweepable_qty),
        #         "MDQuoteType": "TRD",
        #         "activeQuote": "true",
        #         "indiceUpperQty": str(int(len(tenors))+int(1)),
        #         'defaultBidMargin': 0 if default_bid_margin is None else str(default_bid_margin),
        #         'defaultOfferMargin': 0 if default_offer_margin is None else str(default_offer_margin),
        #         'parentIndiceUpperQty': parent_indice_upper_qty,
        #         'editableQty': 'false',
        #         'publishPrices': 'true'
        #     })
        #     tenor.update({'lastUpdateTime': timestamp})
        # self.update_parameters({'clientTierInstrSymbolQty': qty_list, 'clientTierInstrSymbolTenor': tenors})

        return self



