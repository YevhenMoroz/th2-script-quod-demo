import time

from custom import basic_custom_actions as bca
from quod_qa.fx.fx_wrapper.CaseParams import CaseParams
from stubs import Stubs


class MarketDataRequst:
    md_params=None
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    subscribe = None
    mdreqid=None
    case_params = None
    md_subscribe_response=None
    md_reject_response=None
    message_verification=None




    def __init__(self, case_params=CaseParams, market_depth='0', md_update_type='0'):
        self.market_depth=market_depth
        self.md_update_type=md_update_type
        self.case_params=case_params
        self.mdreqid=case_params.mdreqid
        self.set_md_subscribe_response()
        self.set_md_params()


    def set_md_params(self):
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
        return self

    #Send MarketDataRequest subscribe method
    def send_md_request(self):
        self.md_params['SubscriptionRequestType'] = '1'
        self.subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                self.case_params.connectivity,
                self.case_params.case_id,
                bca.message_to_grpc('MarketDataRequest', self.md_params, self.case_params.connectivity)
            ))
        return self

    def set_md_subscribe_response(self):
        # Defaulf band with qty=1M
        self.md_subscribe_response = {
            'MDReqID': self.mdreqid,
            'Instrument': {
                'Symbol': self.case_params.symbol
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

    def set_md_reject_response(self,text):
        self.md_reject_response = {
            'MDReqID': self.mdreqid,
            'MDReqRejReason': '0',
            'Text': text
        }
        return self





    # Extract filed by name
    def extruct_filed(self, field, band_number=1):
        price = 0
        if field.lower()=='price':
            price = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryPx'].simple_value
            return price
        elif field.lower()=='mdentryid':
            mdEntryId = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryID'].simple_value
            return mdEntryId

    def prepare_md_response(self,*args, published=True ,which_bands_not_pb=None, priced=True,which_bands_not_pr=None):
        self.parse_settl_type()
        if self.case_params.securitytype == 'FXFWD':
            self.prepare_md_for_verification_fwrd(*args, published, which_bands_not_pb, priced, which_bands_not_pr)
        if self.case_params.securitytype == 'FXSPOT':
            self.prepare_md_for_verification_spo(*args, published, which_bands_not_pb, priced, which_bands_not_pr)
        return self

    # Check respons was received
    def verify_md_pending(self):
        time.sleep(3)
        msg = self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', self.md_subscribe_response, ['MDReqID']),
                self.subscribe.checkpoint_id,
                self.case_params.connectivity,
                self.case_params.case_id
            )
        )
        self.message_verification=msg
        return self

    # Check respons was received
    def verify_md_pending_forward(self, *args, published=True, priced=True):
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
        return self

    def verify_md_reject(self,text,reason=''):
        self.set_md_reject_response(text)
        time.sleep(5)
        if reason=='date':
            self.md_reject_response.pop('MDReqRejReason')
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Market Data Request Reject',
                bca.filter_to_grpc('MarketDataRequestReject', self.md_reject_response, ['MDReqID']),
                self.subscribe.checkpoint_id,
                self.case_params.connectivity,
                self.case_params.case_id
            )
        )

    def prepare_md_for_verification_spo(self,qty_count, published, which_bands_not_pb, priced, which_bands_not_pr):
        if len(qty_count) > 0:
            a = len(qty_count)
            band = 0
            row_pub = 0
            row_prc = 0
            check_pub=0
            check_price=0
            self.md_subscribe_response['NoMDEntries'].clear()
            md_entry_position=1
            for qty in qty_count:
                b=qty
                md_entry_type = 0
                while md_entry_type < 2:
                    # self.md_subscribe_response['NoMDEntries'].append(one_band)
                    self.md_subscribe_response['NoMDEntries'].append({
                        'SettlType': 0,
                        'MDEntryPx': '*',
                        'MDEntryTime': '*',
                        'MDEntryID': '*',
                        'MDEntrySize': qty,
                        'QuoteEntryID': '*',
                        'MDOriginType': 1,
                        'SettlDate': self.case_params.settldate.split(' ')[0],
                        'MDQuoteType': 1,
                        'MDEntryPositionNo': md_entry_position,
                        'MDEntryDate': '*',
                        'MDEntryType': md_entry_type
                    })

                    if published == False:
                        if which_bands_not_pb == None:
                            self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '0'
                        else:
                            if qty!=which_bands_not_pb[row_pub]:
                                self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '1'
                            if qty==which_bands_not_pb[row_pub]:
                                self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '0'
                                check_pub += 1

                    if priced == False:
                        if which_bands_not_pr == None:
                            self.md_subscribe_response['NoMDEntries'][band]['QuoteCondition'] = 'B'
                        elif qty==which_bands_not_pr[row_prc]:
                                self.md_subscribe_response['NoMDEntries'][band]['QuoteCondition'] = 'B'
                                check_price += 1

                    md_entry_type +=1
                    band +=1
                md_entry_position +=1
                if check_pub!=0:
                    row_pub +=1
                if check_price != 0:
                    row_prc += 1

    def prepare_md_for_verification_fwrd(self,qty_count, published, which_bands_not_pb, priced, which_bands_not_pr):
        if len(qty_count) > 0:
            a = len(qty_count)
            band = 0
            row_pub = 0
            row_prc = 0
            check_pub=0
            check_price=0
            self.md_subscribe_response['NoMDEntries'].clear()
            md_entry_position=1
            for qty in qty_count:
                md_entry_type = 0
                while md_entry_type < 2:
                    # self.md_subscribe_response['NoMDEntries'].append(one_band)
                    self.md_subscribe_response['NoMDEntries'].append({
                        'SettlType': self.case_params.settltype,
                        'MDEntryPx': '*',
                        'MDEntryTime': '*',
                        'MDEntryID': '*',
                        'MDEntryForwardPoints':'*',
                        'MDEntrySize': qty,
                        'MDEntrySpotRate':'*',
                        'QuoteEntryID': '*',
                        'MDOriginType': 1,
                        'SettlDate': self.case_params.settldate.split(' ')[0],
                        'MDQuoteType': 1,
                        'MDEntryPositionNo': md_entry_position,
                        'MDEntryDate': '*',
                        'MDEntryType': md_entry_type
                    })

                    if published == False:
                        if which_bands_not_pb == None:
                            self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '0'
                        else:
                            if qty!=which_bands_not_pb[row_pub]:
                                self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '1'
                            if qty==which_bands_not_pb[row_pub]:
                                self.md_subscribe_response['NoMDEntries'][band]['MDQuoteType'] = '0'
                                check_pub += 1

                    if priced == False:
                        if which_bands_not_pr == None:
                            self.md_subscribe_response['NoMDEntries'][band]['QuoteCondition'] = 'B'
                        elif qty==which_bands_not_pr[row_prc]:
                                self.md_subscribe_response['NoMDEntries'][band]['QuoteCondition'] = 'B'
                                check_price += 1

                    md_entry_type +=1
                    band +=1
                md_entry_position +=1
                if check_pub!=0:
                    row_pub +=1
                if check_price != 0:
                    row_prc += 1

    # Send MarketDataRequest unsubscribe method
    def send_md_unsubscribe(self):
        self.md_params['SubscriptionRequestType'] = '2'
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.case_params.connectivity,
                self.case_params.case_id,
                bca.message_to_grpc('MarketDataRequest', self.md_params, self.case_params.connectivity)
            ))


    def parse_settl_type(self):
        if self.case_params.settltype == 'MO1':
            self.case_params.settltype = 'M1'








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