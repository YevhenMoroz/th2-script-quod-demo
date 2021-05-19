
from CaseParams import CaseParams
from custom import basic_custom_actions as bca
from stubs import Stubs


class MarketDataRequst:
    md_params=None
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    subscribe = None

    # Defaulf band with qty=1M
    md_subscribe_response = {
        'MDReqID': md_params['MDReqID'],
        'Instrument': {
            'Symbol': ''
        },
        'LastUpdateTime': '*',
        'NoMDEntries': [
            {
                'SettlType': 0,
                'MDEntryPx': '*',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '1000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': '',
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryPx': '*',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '1000000',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': '',
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 1
            }

        ]
    }

    def __init__(self, market_depth='0', md_update_type='0',case_params=CaseParams):
        self.market_depth=market_depth
        self.md_update_type=md_update_type
        self.case_params=case_params

        self.md_params={
            'SenderSubID': self.case_params.account,
            'MDReqID': self.case_params.mdreqid,
            'MarketDepth': self.market_depth,
            'MDUpdateType': self.md_update_type,
            'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
            'NoRelatedSymbols': [
                {
                    'Instrument': {
                        'Symbol': self.case_params.symbol,
                        'SecurityType': self.case_params.securitytype,
                        'Product': self.case_params.product
                    },
                    'SettlDate': self.case_params.settldate,
                    'SettlType': self.case_params.settltype
                }
            ]
        }

    # Send MarketDataRequest subscribe method
    def send_md_request(self):
        self.md_params['SubscriptionRequestType'] = '1'
        self.subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                self.case_params.connectivity,
                self.case_params.case_id,
                bca.message_to_grpc('MarketDataRequest', self.md_params, self.case_params.connectivity)
            ))


    # Extract filed by name
    def extruct_filed(self, field, band_number=0):
        if field=='price':
            self.subscribe.response_messages_list[band_number].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[1] \
                .message_value.fields['MDEntryPx'].simple_value


    # Check respons was received
    def verify_md_pending(self, *args, published=True, priced=True):
        self.prepare_md_for_verification(*args, published=True, priced=True)
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', self.md_subscribe_response, ['MDReqID']),
                self.subscribe.checkpoint_id,
                self.case_params.connectivity,
                self.case_params.case_id
            )
        )


    def prepare_md_for_verification(self,*args, published=True, priced=True):
        if len(args) > 0:
            band = 0
            self.md_subscribe_response['NoMDEntries'].clear()
            md_entry_position=1
            for qty in args:
                md_entry_type = 0
                while md_entry_type < 2:
                    # self.md_subscribe_response['NoMDEntries'].append(one_band)
                    self.md_subscribe_response['NoMDEntries'].append({
                        'SettlType': 0,
                        'MDEntryPx': '*',
                        'MDEntryTime': '*',
                        'MDEntryID': '*',
                        'MDEntrySize': '1000000',
                        'QuoteEntryID': '*',
                        'MDOriginType': 1,
                        'SettlDate': '',
                        'MDQuoteType': 1,
                        'MDEntryPositionNo': 1,
                        'MDEntryDate': '*',
                        'MDEntryType': 0
                    })
                    self.md_subscribe_response['NoMDEntries'][band]['MDEntrySize'] = qty
                    self.md_subscribe_response['NoMDEntries'][band]['MDEntryType'] = md_entry_type
                    self.md_subscribe_response['NoMDEntries'][band]['MDEntryPositionNo'] = md_entry_position
                    self.md_subscribe_response['NoMDEntries'][band]['SettlDate'] = '2021/05/08'
                    md_entry_type +=1
                    band +=1
                md_entry_position +=1


    # Send MarketDataRequest unsubscribe method
    def send_md_unsubscribe(self):
        self.md_params['SubscriptionRequestType'] = '2'
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.case_params.connectivity,
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', self.md_params, self.case_params.connectivity)
            ))











    # one_band={
    #     {
    #         'SettlType': 0,
    #         'MDEntryPx': '*',
    #         'MDEntryTime': '*',
    #         'MDEntryID': '*',
    #         'MDEntrySize': '1000000',
    #         'QuoteEntryID': '*',
    #         'MDOriginType': 1,
    #         'SettlDate': '',
    #         'MDQuoteType': 1,
    #         'MDEntryPositionNo': 1,
    #         'MDEntryDate': '*',
    #         'MDEntryType': 0
    #     }
    # }
    # Send MarketDataRequest subscribe method
    # def send_md_request(self,case_id):
    #     self.md_params['SubscriptionRequestType'] = '1'
    #     subscribe = self.fix_act.placeMarketDataRequestFIX(
    #         bca.convert_to_request(
    #             'Send MDR (subscribe)',
    #             self.case_params.connectivity,
    #             case_id,
    #             bca.message_to_grpc('MarketDataRequest', self.md_params, self.case_params.connectivity)
    #         ))
    #     price =  subscribe \
    #         .response_messages_list[0].fields['NoMDEntries'] \
    #         .message_value.fields['NoMDEntries'].list_value.values[1] \
    #         .message_value.fields['MDEntryPx'].simple_value
    #
    #     self.md_subscribe_response['MDReqID']=self.md_params['MDReqID']
    #     self.md_subscribe_response['MDReqID']['Symbol']=self.case_params.symbol
    #     self.md_subscribe_response['NoMDEntries']['Symbol']=self.case_params.symbol
    #
    #     self.verifier.submitCheckRule(
    #         bca.create_check_rule(
    #             'Receive MarketDataSnapshotFullRefresh (pending)',
    #             bca.filter_to_grpc('MarketDataSnapshotFullRefresh', self.md_subscribe_response, ['MDReqID']),
    #             subscribe.checkpoint_id,
    #             self.case_params['Connectivity'],
    #             self.case_id
    #         )
    #     )
    #
    #     #return price for Sending Order in future
    #     return price