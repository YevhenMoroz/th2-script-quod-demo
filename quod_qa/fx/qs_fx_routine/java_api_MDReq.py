from pathlib import Path
from stubs import Stubs
from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest
from custom import basic_custom_actions as bca
from quod_qa.common_tools import random_qty


from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class TestCase:
    def __init__(self):
        self.act_java_api = Stubs.act_java_api
        # self.connectivity = 'java-api-luna314'
        self.connectivity = '314_java_api'
        # checkpoint_id1 = None


    def send_nos(self):
        # checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        # self.checkpoint_id1 = checkpoint1.checkpoint
        nos_params = {
            # 'SEND_SUBJECT': 'QUOD.QSFE.FIX',
            # 'SEND_SUBJECT': 'QUOD.MDA.FIX',
            # 'SEND_SUBJECT': 'QUOD.MDA.REQUEST',
            # 'SEND_SUBJECT': 'QUOD.PRICING.2.FE',
            'SEND_SUBJECT': 'MDA.QUOD.PRICING.2.SUB',
            # 'SEND_SUBJECT': 'MDA.506403761.4.D.PRICING.2',
            # 'SEND_SUBJECT': 'QUOD.PRICING.1.FIX',
            'MarketDataRequestBlock': {
                # 'MarketDepth': '',
                # 'ExternalEntitlementKey': '',
                # 'SubscriptionRequestType': 'Units',
                # 'ClientAccountGroupID': 'Limit',
                # 'MDQuoteType': 'Day',
                # 'MDUpdateType': 'Open',
                # 'IPAddress': 'EUR',
                # 'MDReqList': 'Agency',
                'MDReqID': random_qty(1,2,len=10),
                # 'MDSource': '',
                # 'BookType': 1,
                # 'ClientClientTierID': 'No',
                'MDSymbolList': {
                    'MDSymbolBlock': [
                        {
                            'ListingID': '506403761',
                            'MDSymbol': '506403761.4',
                            'ClientTierID': '4',
                            'FeedType': 'D',
                            # 'MDEntrySizeList': '',
                            'SubscriptionRequestType': 'SUB',
                            # 'UseDefaultMargins': ''
                        }
                ]
                    },
            }
        }

        # print(ActJavaSubmitMessageRequest(
        #     message=bca.message_to_grpc('Market_MarketDataRequest', nos_params, 'java-api-luna314')))

        response= self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Market_MarketDataRequest', nos_params, self.connectivity)))

        # print(f'*********** response sendMessage = {response}************')
        # print(f'*********** response sendMessage = {response}************')


    # Main method
    def execute(self, report_id):
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        self.send_nos()
        def_order_exec_report = {
            'ActiveClientTier':'*',
            'AutomatedMargin':'*',
            'MarginPriceType':'*',
            'MDQuoteType':'*',
            'MDQuoteTypeStatus':'*',
            'MDReportID':'*',
            'MDTime':'*',
            'PositionBasedMargins':'*',
            'QuoteConditionStatus':'*',
            'MDReqID':'*',
            'MarketDataFullList': {
                'MarketDataFullBlock':
                    [
                        {
                            'VenueOrdID': '*',
                            'MDEntryPx': '*',
                            'OrdType': '*',
                            'MDQuoteType': '*',
                            'MDEntryID': '*',
                            'MDEntrySize': '*',
                            'QuoteEntryID': '*',
                            'MDEntryBaseSize': '*',
                            'MDEntryPosition': '*',
                            'MDEntryMargin': '*',
                            'MDEntryType': '*',
                            'MDEntryBaseMargin': '*',
                        },
                        {
                            'VenueOrdID': '*',
                            'MDEntryPx': '*',
                            'OrdType': '*',
                            'MDQuoteType': '*',
                            'MDEntryID': '*',
                            'MDEntrySize': '*',
                            'QuoteEntryID': '*',
                            'MDEntryBaseSize': '*',
                            'MDEntryPosition': '*',
                            'MDEntryMargin': '*',
                            'MDEntryType': '*',
                            'MDEntryBaseMargin': '*',
                        },
                        {
                            'VenueOrdID': '*',
                            'MDEntryPx': '*',
                            'OrdType': '*',
                            'MDQuoteType': '*',
                            'MDEntryID': '*',
                            'MDEntrySize': '*',
                            'QuoteEntryID': '*',
                            'MDEntryBaseSize': '*',
                            'MDEntryPosition': '*',
                            'MDEntryMargin': '*',
                            'MDEntryType': '*',
                            'MDEntryBaseMargin': '*',
                        },
                        {
                            'VenueOrdID': '*',
                            'MDEntryPx': '*',
                            'OrdType': '*',
                            'MDQuoteType': '*',
                            'MDEntryID': '*',
                            'MDEntrySize': '*',
                            'QuoteEntryID': '*',
                            'MDEntryBaseSize': '*',
                            'MDEntryPosition': '*',
                            'MDEntryMargin': '*',
                            'MDEntryType': '*',
                            'MDEntryBaseMargin': '*',
                        },
                        {
                            'VenueOrdID': '*',
                            'MDEntryPx': '*',
                            'OrdType': '*',
                            'MDQuoteType': '*',
                            'MDEntryID': '*',
                            'MDEntrySize': '*',
                            'QuoteEntryID': '*',
                            'MDEntryBaseSize': '*',
                            'MDEntryPosition': '*',
                            'MDEntryMargin': '*',
                            'MDEntryType': '*',
                            'MDEntryBaseMargin': '*',
                        },
                        {
                            'VenueOrdID': '*',
                            'MDEntryPx': '*',
                            'OrdType': '*',
                            'MDQuoteType': '*',
                            'MDEntryID': '*',
                            'MDEntrySize': '*',
                            'QuoteEntryID': '*',
                            'MDEntryBaseSize': '*',
                            'MDEntryPosition': '*',
                            'MDEntryMargin': '*',
                            'MDEntryType': '*',
                            'MDEntryBaseMargin': '*',
                        }
                    ]
            }
        }

        checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint1.checkpoint
        Stubs.verifier.submitCheckRule(
            request=bca.create_check_rule(
                '',
                bca.filter_to_grpc('Market_MarketDataSnapshotFullRefresh', def_order_exec_report,
                                   ['MDReqID', 'MDReportID']),
                checkpoint_id1, self.connectivity, case_id
            ),

        )
        print(def_order_exec_report)


if __name__ == '__main__':
    pass
