from datetime import datetime, timedelta

from test_cases.fx.fx_wrapper.common_tools import generate_schedule
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiClientTierInstrSymbolMessages(RestApiMessages):

    def find_all_client_tier_instrument(self):
        self.clear_message_params()
        self.message_type = 'FindAllClientTierInstrSymbol'
        return self

    def find_client_tier_instrument(self, client_tier_id: str, instrument: str):
        self.clear_message_params()
        self.message_type = 'FindClientTierInstrSymbol'
        self.parameters = {
            'URI':
                {
                    'queryID': client_tier_id,
                    'curr1': instrument.split('/')[0],
                    'curr2': instrument.split('/')[1],
                }
        }
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

    def sort_bands_by_indice_upper_quantity(self):
        for_sort = dict()
        bands = list()
        for band in self.parameters["clientTierInstrSymbolQty"]:
            index = band.get("indiceUpperQty")
            for_sort.update({index: band})
        for i in range(len(for_sort)):
            a = for_sort.get(str(i))
            bands.append(for_sort.get(str(i)))
        self.parameters["clientTierInstrSymbolQty"] = bands
        return self

    def add_sweepable_qty(self, sweepable_qty, default_bid_margin=None, default_offer_margin=None):
        qty_list = self.get_parameter('clientTierInstrSymbolQty')
        parent_indice_upper_qty = str(int(len(qty_list)) + int(1))
        qty_list.append({
            "upperQty": str(sweepable_qty),
            "indiceUpperQty": parent_indice_upper_qty,
            "publishPrices": "true"
        })
        tenors = self.get_parameter('clientTierInstrSymbolTenor')
        timestamp = str(datetime.now().timestamp())
        timestamp = timestamp.split(".", 1)
        timestamp = timestamp[0]
        for tenor in tenors:
            indiceUpperQty = len(tenor["clientTierInstrSymbolTenorQty"]) + 1
            tenor["clientTierInstrSymbolTenorQty"].append({
                "upperQty": str(sweepable_qty),
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "indiceUpperQty": indiceUpperQty,
                'defaultBidMargin': 0 if default_bid_margin is None else str(default_bid_margin),
                'defaultOfferMargin': 0 if default_offer_margin is None else str(default_offer_margin),
                'parentIndiceUpperQty': parent_indice_upper_qty,
                'editableQty': 'false',
                'publishPrices': 'true'
            })
            tenor.update({'lastUpdateTime': timestamp})
        self.update_parameters({'clientTierInstrSymbolQty': qty_list, 'clientTierInstrSymbolTenor': tenors})
        return self

    def set_sweepable_qty(self, sweepable_qty_list: list, default_bid_margin=None, default_offer_margin=None):
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

    def delete_sweepable_qty(self, indice_upper_qty_to_delete: list = None):
        qty_list = self.get_parameter('clientTierInstrSymbolQty')
        tenors = self.get_parameter('clientTierInstrSymbolTenor')
        timestamp = str(datetime.now().timestamp())
        timestamp = timestamp.split(".", 1)
        timestamp = timestamp[0]
        for indice_upper_qty in indice_upper_qty_to_delete:
            qty_list.pop(indice_upper_qty)
        i = 1
        for qty in qty_list:
            qty['indiceUpperQty'] = str(i)
            i += 1
        for tenor in tenors:
            id_to_delete = []
            id = 1
            for tenor_qty in tenor['clientTierInstrSymbolTenorQty']:
                if tenor_qty['parentIndiceUpperQty'] not in range(len(qty_list) + 1):
                    id_to_delete.append(id)
                id += 1
            if len(id_to_delete) > 0:
                for id in id_to_delete:
                    tenor['clientTierInstrSymbolTenorQty'].pop(id)
            tenor.update({'lastUpdateTime': timestamp})
        self.update_parameters({'clientTierInstrSymbolQty': qty_list, 'clientTierInstrSymbolTenor': tenors})
        return self

    def remove_all_qty(self):
        self.remove_parameter('clientTierInstrSymbolQty')
        self.remove_field_from_component('clientTierInstrSymbolTenor', "clientTierInstrSymbolTenorQty")
        return self

    def set_published_false(self, bands_to_update: list = None):
        sweepable = self.get_parameter('clientTierInstrSymbolQty')
        tenors = self.get_parameter('clientTierInstrSymbolTenor')
        if bands_to_update is not None:
            for band in sweepable:
                if band["upperQty"] in bands_to_update:
                    band.update({"publishPrices": "false"})
            for tenor in tenors:
                for band in tenor['clientTierInstrSymbolTenorQty']:
                    if band["upperQty"] in bands_to_update:
                        band.update({"publishPrices": "false"})
        else:
            for band in sweepable:
                band.update({"publishPrices": "false"})
            for tenor in tenors:
                for band in tenor['clientTierInstrSymbolTenorQty']:
                    band.update({"publishPrices": "false"})
        self.update_parameters({'clientTierInstrSymbolQty': sweepable, 'clientTierInstrSymbolTenor': tenors})
        return self

    def add_tenor_qty(self, qty, default_bid_margin=None, default_offer_margin=None):
        tenors = self.get_parameter('clientTierInstrSymbolTenor')
        timestamp = str(datetime.now().timestamp())
        timestamp = timestamp.split(".", 1)
        timestamp = timestamp[0]
        for tenor in tenors:
            indiceUpperQty = len(tenor["clientTierInstrSymbolTenorQty"]) + 1
            tenor["clientTierInstrSymbolTenorQty"].append({
                "upperQty": str(qty),
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "indiceUpperQty": indiceUpperQty,
                'defaultBidMargin': 0 if default_bid_margin is None else str(default_bid_margin),
                'defaultOfferMargin': 0 if default_offer_margin is None else str(default_offer_margin),
                'editableQty': 'true',
                'publishPrices': 'true'
            })
            tenor.update({'lastUpdateTime': timestamp})
        self.update_parameters({'clientTierInstrSymbolTenor': tenors})
        return self


