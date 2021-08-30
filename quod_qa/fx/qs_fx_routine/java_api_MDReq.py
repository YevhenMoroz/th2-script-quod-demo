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
        self.connectivity = 'java-api-luna314'



    def send_nos(self):
        nos_params = {
            'SEND_SUBJECT': 'QUOD314.QSFE.FE',
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
                            'ListingID': '100000413',
                            'MDSymbol': '100000413.4',
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

        print(f'*********** response sendMessage = {response}************')
        print(f'*********** response sendMessage = {response}************')


    # Main method
    def execute(self, report_id):
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        self.send_nos()
        def_order_exec_report = {
            'MarketDataFullList':{
                'MarketDataFullBlock':[
                    {
                        'MDEntryType': 'Bid',
                        'MDEntryPosition': '1',
                        'MDOriginType': 'Book'
                    }
                ]
            }
        }
        checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint1.checkpoint
        Stubs.verifier.submitCheckRule(
            request=bca.create_check_rule(
                '',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', def_order_exec_report,
                                   ['MDEntryPosition', 'MDOriginType']),
                checkpoint_id1, self.connectivity, case_id
            ),
            timeout=1000
        )


if __name__ == '__main__':
    pass
