import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.win_gui_wrappers.forex.fx_child_book import FXChildBook
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

from win_gui_modules.utils import get_base_request

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
alias_fh = "fix-fh-q-314-luna"
alias_gtw = "fix-sell-esp-t-314-stand"


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:

        # Send market data to the EBS-CITI venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_EBS, symbol, securitytype,
                                   connectivity=alias_fh).prepare_custom_md_spot(
            no_md_entries_spo_ebs)). \
            send_market_data_spot(even_name_custom='Send Market Data SPOT EBS-CITI')
        # Send market data to the DB venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_DB, symbol, securitytype,
                                   connectivity=alias_fh).prepare_custom_md_spot(
            no_md_entries_spo_db)). \
            send_market_data_spot(even_name_custom='Send Market Data SPOT DB')

        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters(
            {'OrderQty': '2000000'}).add_fields_into_repeating_group('NoStrategyParameters', [
            {'StrategyParameterName': 'AllowedVenues', 'StrategyParameterType': '14',
             'StrategyParameterValue': 'EBS-CITI/DB'}])
        FixManager(alias_gtw, case_id).send_message(fix_message=new_order_sor)

        FXOrderBook(case_id, session_id).set_filter(
            ["Order ID", "AO", "Qty", "2000000", "Orig", "FIX", "Lookup", "EUR/USD-SPO.SPO", "Client ID", "TH2_Taker",
             "TIF", "Day"]).check_order_fields_list({"ExecSts": "Filled"})

        FXChildBook(case_id, session_id).set_filter(
            ["Order ID", "MO", "Venue", "DB", "Orig", "Internal", "Lookup", "EUR/USD-SPO.SPO", "Client ID",
             "TH2_Taker"]).check_order_fields_list(
            {"ExecSts": "Filled", "Qty": "1,000,000", "Limit Price": "1.18141", "OrdType": "PreviouslyQuoted",
             "TIF": "ImmediateOrCancel"}, event_name="Check Child Order DB")

        FXChildBook(case_id, session_id).set_filter(
            ["Order ID", "MO", "Venue", "EBS-CITI", "Orig", "Internal", "Lookup", "EUR/USD-SPO.SPO", "Client ID",
             "TH2_Taker"]).check_order_fields_list(
            {"ExecSts": "Filled", "Qty": "1,000,000", "Limit Price": "1.18146", "OrdType": "PreviouslyQuoted",
             "TIF": "ImmediateOrCancel"}, event_name="Check Child Order EBS-CITI")

    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        pass
