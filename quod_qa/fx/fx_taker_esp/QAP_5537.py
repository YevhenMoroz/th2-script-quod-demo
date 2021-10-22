import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.win_gui_wrappers.forex.fx_child_book import FXChildBook
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fix_act = Stubs.fix_act

symbol = 'EUR/USD'
securitytype = 'FXSPOT'
defaultmdsymbol_spo_DB = 'EUR/USD:SPO:REG:DB'
defaultmdsymbol_spo_EBS = 'EUR/USD:SPO:REG:EBS-CITI'
no_md_entries_spo_db = [
    {
        "MDEntryType": "0",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Bid1",
        "MDEntryPx": 1.18075,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Offer1",
        "MDEntryPx": 1.18141,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Bid2",
        "MDEntryPx": 1.18071,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Offer2",
        "MDEntryPx": 1.18145,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
no_md_entries_spo_ebs = [
    {
        "MDEntryType": "0",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Bid1",
        "MDEntryPx": 1.18066,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Offer1",
        "MDEntryPx": 1.18146,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Bid2",
        "MDEntryPx": 1.18061,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Offer2",
        "MDEntryPx": 1.18149,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]


# instrument = dict(
#             Symbol='EUR/USD',                                    #55
#             SecurityType='FXSPOT',                               #167
#         )
#         base_parameters = {
#             "ClOrdID": bca.client_orderid(9),                    #11
#             "Account": "TH2_Taker",                              #1
#             "HandlInst": "2",                                    #21
#             "Side": "1",                                         #54
#             "OrderQty": "2000000",                               #38
#             "TimeInForce": "0",                                  #59
#             "OrdType": "2",                                      #40
#             "TransactTime": datetime.utcnow().isoformat(),       #60
#             "Price": "1.18999",                                  #44
#             "Currency": "EUR",                                   #15
#             "Instrument": instrument,
#             "TargetStrategy": "1008",                            #847
#             "SettlDate": spo(),                                  #64
#             "SettlType": '0',                                    #63
#             "NoStrategyParameters":[                             #957
#                 {
#                     'StrategyParameterName': 'AllowedVenues',    #958
#                     'StrategyParameterType': '14',               #959
#                     'StrategyParameterValue': 'EBS-CITI/DB'      #960
#                 }
#             ]

def execute(report_id, session_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        case_base_request = get_base_request(session_id, case_id)
        alias = "fix-fh-q-314-luna"

        # Send market data to the EBS-CITI venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_EBS, symbol, securitytype,
                                   connectivity=alias).prepare_custom_md_spot(
            no_md_entries_spo_ebs)). \
            send_market_data_spot(even_name_custom='Send Market Data SPOT EBS-CITI')
        # Send market data to the DB venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_DB, symbol, securitytype,
                                   connectivity=alias).prepare_custom_md_spot(
            no_md_entries_spo_db)). \
            send_market_data_spot(even_name_custom='Send Market Data SPOT DB')

        new_order_single = FixMessageNewOrderSingleAlgoFX().set_default_SOR()
        # new_order_single.change_parameter

        print('New Order Single parameters: ', new_order_single)
        fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ', 'fix-sell-esp-t-314-stand', case_id,
                bca.message_to_grpc('NewOrderSingle', new_order_single,
                                    'fix-sell-esp-t-314-stand')
            ))

        FXOrderBook(case_id, case_base_request).set_filter(
            ["Order ID", "AO", "Qty", "2000000", "Orig", "FIX", "Lookup", "EUR/USD-SPO.SPO", "Client ID", "TH2_Taker",
             "TIF","Day"]).check_order_fields_list({"ExecSts": "Filled"})

        FXChildBook(case_id, case_base_request).set_filter(
            ["Order ID", "MO", "Venue", "DB", "Orig", "Internal", "Lookup", "EUR/USD-SPO.SPO", "Client ID",
             "TH2_Taker"]).check_order_fields_list(
            {"ExecSts": "Filled", "Qty": "1,000,000", "Limit Price": "1.18141", "OrdType": "PreviouslyQuoted",
             "TIF": "ImmediateOrCancel"}, event_name="Check Child Order DB")

        FXChildBook(case_id, case_base_request).set_filter(
            ["Order ID", "MO", "Venue", "EBS-CITI", "Orig", "Internal", "Lookup", "EUR/USD-SPO.SPO", "Client ID",
             "TH2_Taker"]).check_order_fields_list(
            {"ExecSts": "Filled", "Qty": "1,000,000", "Limit Price": "1.18146", "OrdType": "PreviouslyQuoted",
             "TIF": "ImmediateOrCancel"}, event_name="Check Child Order EBS-CITI")







    except Exception as e:
        logging.error('Error execution', exc_info=True)

    finally:
        pass
