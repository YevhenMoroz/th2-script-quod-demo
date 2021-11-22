import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from quod_qa.wrapper_test.DataSet import DirectionEnum
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from quod_qa.wrapper_test.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

alias_fh = "fix-fh-314-luna"
alias_gtw = "fix-sell-esp-t-314-stand"
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
defaultmdsymbol_spo_barx = 'EUR/USD:SPO:REG:BARX'
defaultmdsymbol_spo_citi = 'EUR/USD:SPO:REG:CITI'
no_md_entries_spo_barx = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18066,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18146,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
no_md_entries_spo_citi = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18075,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18141,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    fix_manager = FixManager(alias_gtw, case_id)
    fix_verifier = FixVerifier(alias_gtw, case_id)
    try:

        # Send market data to the BARX venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_barx, symbol, securitytype,
                                   connectivity=alias_fh).prepare_custom_md_spot(
            no_md_entries_spo_barx)).send_market_data_spot(even_name_custom='Send Market Data SPOT BARX')

        # Send market data to the CITI venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_citi, symbol, securitytype,
                                   connectivity=alias_fh).prepare_custom_md_spot(
            no_md_entries_spo_citi)). \
            send_market_data_spot(even_name_custom='Send Market Data SPOT CITI')

        # STEP 1
        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters({'TimeInForce': '3'})
        new_order_sor.add_fields_into_repeating_group('NoStrategyParameters', [
            {'StrategyParameterName': 'LonePassive', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'},
            {'StrategyParameterName': 'AllowedVenues', 'StrategyParameterType': '14',
             'StrategyParameterValue': 'CITI/BARX'}])
        fix_manager.send_message_and_receive_response(new_order_sor)

        execution_report_filled = FixMessageExecutionReportAlgoFX().update_to_filled_sor(
            new_order_sor).add_party_role()
        fix_verifier.check_fix_message(execution_report_filled, direction=DirectionEnum.FIRST.value)

        FXOrderBook(case_id, session_id).set_filter(
            ["Order ID", "AO", "Qty", "1000000", "Orig", "FIX", "Lookup", "EUR/USD-SPO.SPO", "Client ID", "TH2_Taker",
             "TIF", "ImmediateOrCancel"]).check_order_fields_list({"ExecSts": "Filled"})
        FXOrderBook(case_id, session_id).check_second_lvl_fields_list(
            {"ExecSts": "Filled", "Venue": "CITI", "Limit Price": "1.18141", "Qty": "1,000,000"})

        # STEP 2
        new_order_sor_2 = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters(
            {'TimeInForce': '3', 'OrderQty': '5000000'})
        new_order_sor_2.add_fields_into_repeating_group('NoStrategyParameters', [
            {'StrategyParameterName': 'LonePassive', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'},
            {'StrategyParameterName': 'AllowedVenues', 'StrategyParameterType': '14',
             'StrategyParameterValue': 'CITI/BARX'}])
        fix_manager.send_message_and_receive_response(new_order_sor_2)

        execution_report_filled_2 = FixMessageExecutionReportAlgoFX().update_to_filled_sor(
            new_order_sor_2).add_party_role()
        fix_verifier.check_fix_message(execution_report_filled_2, direction=DirectionEnum.FIRST.value)

        FXOrderBook(case_id, session_id).set_filter(
            ["Order ID", "AO", "Qty", "5000000", "Orig", "FIX", "Lookup", "EUR/USD-SPO.SPO", "Client ID", "TH2_Taker",
             "TIF", "ImmediateOrCancel"]).check_order_fields_list({"ExecSts": "Filled"})
        FXOrderBook(case_id, session_id).check_second_lvl_fields_list(
            {"ExecSts": "Filled", "Venue": "BARX", "Limit Price": "1.18146", "Qty": "5,000,000"})

    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
