import logging
import time
from pathlib import Path
from stubs import Stubs
from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

from datetime import datetime

from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.common_tools import random_qty

alias_fh = "fix-fh-314-luna"
defaultmdsymbol_spo_hsbc = 'GBP/USD:SPO:REG:HSBC'
no_md_entries_spo_hsbc = [
    {
        "MDEntryType": "0",
        "QuoteEntryID": "1_GBP/USD_20211122292ACF004FF385E1_Bid2",
        "MDEntryPx": 1.18075,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "1_GBP/USD_20211122292ACF004FF385E1_Ask2",
        "MDEntryPx": 1.18141,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
symbol = 'GBP/USD'
securitytype = 'FXSPOT'


class QAP_5389:
    def __init__(self):
        self.act_java_api = Stubs.act_java_api
        self.connectivity = '314_java_api'

    def send_mdr_sub(self):
        md_params = {
            'SEND_SUBJECT': 'MDA.QUOD.PRICING.2.SUB',
            'REPLY_SUBJECT': 'MDA.506404433.2000011.D.PRICING.2',
            'MarketDataRequestBlock': {
                'MDReqID': random_qty(1, 2, len=10),
                'MDSymbolList': {
                    'MDSymbolBlock': [
                        {
                            'ListingID': '506404433',
                            'MDSymbol': '506404433.2000011',
                            'ClientTierID': '2000011',
                            'FeedType': 'D',
                            'SubscriptionRequestType': 'SUB'
                        }
                    ]
                },
            }
        }

        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Market_MarketDataRequest', md_params, self.connectivity)))

    # Main method
    def execute(self, report_id):
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        try:
            checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
            # Send market data to the HSBC venue GBP/USD spot
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_hsbc, symbol, securitytype,
                                       connectivity=alias_fh).prepare_custom_md_spot(
                no_md_entries_spo_hsbc)).send_market_data_spot(even_name_custom='Send Market Data SPOT HSBC')
            checkpoint_id1 = checkpoint1.checkpoint
            time.sleep(5)
            self.send_mdr_sub()

            def_order_exec_report = {
                'ActiveClientTier': '*',
                'AutomatedMargin': '*',
                'MarginPriceType': '*',
                'MDQuoteType': '*',
                'OrigQuoteEntryID': '*',
                'MDQuoteTypeStatus': '*',
                'MDReportID': '*',
                'MDTime': '*',
                'PositionBasedMargins': '*',
                'QuoteConditionStatus': '*',
                'OrigVenueID': '*',
                'OrigMDTime': '*',
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
                            }
                        ]
                }
            }

            time.sleep(2)

            Stubs.verifier.submitCheckRule(
                request=bca.create_check_rule(
                    'Market_MarketDataSnapshotFullRefresh',
                    bca.wrap_filter(def_order_exec_report, 'Market_MarketDataSnapshotFullRefresh'),
                    checkpoint_id1, self.connectivity, case_id
                ),

            )
            print(def_order_exec_report)
        except Exception:
            logging.error("Error execution", exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)


