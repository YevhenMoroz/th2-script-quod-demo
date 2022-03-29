import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TimeInForce, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

alias_fh = "fix-fh-314-luna"
alias_gtw = "fix-sell-esp-t-314-stand"
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
defaultmdsymbol_spo_barx = 'EUR/USD:SPO:REG:BARX'
defaultmdsymbol_spo_citi = 'EUR/USD:SPO:REG:CITI'
defaultmdsymbol_spo_hsbc = 'EUR/USD:SPO:REG:HSBC'
# Gateway Side

gateway_side_sell = DataSet.GatewaySide.Sell
# Status
status = DataSet.Status.Fill
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
no_md_entries_spo_hsbc = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18079,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.1814,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
no_strategy_parameters = [
    {'StrategyParameterName': 'AggressiveSingleOrderOnImmediateOrCancel', 'StrategyParameterType': '13',
     'StrategyParameterValue': 'Y'},
    {'StrategyParameterName': 'AllowedVenues', 'StrategyParameterType': '14',
     'StrategyParameterValue': 'CITI/BARX/HSBC'},
    {'StrategyParameterName': 'ForbiddenVenues', 'StrategyParameterType': '14',
     'StrategyParameterValue': 'BNP/DB/EBS-CITI/GS/JPM/MS'}]
ob_col = OrderBookColumns
tif = TimeInForce
exe_sts = ExecSts


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    fix_manager_gtw = FixManager(alias_gtw, case_id)
    fix_manager_fh = FixManager(alias_fh, case_id)
    fix_verifier = FixVerifier(alias_gtw, case_id)
    try:

        # Send market data to the BARX venue EUR/USD spot
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX().set_market_data() \
            .update_repeating_group('NoMDEntries', no_md_entries_spo_barx). \
            update_MDReqID(defaultmdsymbol_spo_barx, alias_fh, 'FX')
        fix_manager_fh.send_message(market_data_snap_shot, "Send MD BARX EUR/USD ")

        # Send market data to the CITI venue EUR/USD spot
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX().set_market_data() \
            .update_repeating_group('NoMDEntries', no_md_entries_spo_citi) \
            .update_MDReqID(defaultmdsymbol_spo_citi, alias_fh, 'FX')
        fix_manager_fh.send_message(market_data_snap_shot, "Send MD CITI EUR/USD ")

        # Send market data to the HSBC venue EUR/USD spot
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX().set_market_data() \
            .update_repeating_group('NoMDEntries', no_md_entries_spo_hsbc) \
            .update_MDReqID(defaultmdsymbol_spo_hsbc, alias_fh, 'FX')
        fix_manager_fh.send_message(market_data_snap_shot, "Send MD HSBC EUR/USD ")

        # STEP 1
        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters(
            {'TimeInForce': '3', 'OrderQty': '5000000'})
        new_order_sor.update_repeating_group('NoStrategyParameters', no_strategy_parameters)
        fix_manager_gtw.send_message_and_receive_response(new_order_sor)
        execution_report_filled_1 = FixMessageExecutionReportAlgoFX(). \
            set_params_from_new_order_single(new_order_sor, gateway_side_sell, status)
        fix_verifier.check_fix_message(fix_message=execution_report_filled_1,
                                       direction=DirectionEnum.FromQuod)

        FXOrderBook(case_id, session_id).set_filter(
            [ob_col.order_id.value, "AO", ob_col.qty.value, "5000000", ob_col.orig.value, "FIX", ob_col.lookup.value,
             "EUR/USD-SPO.SPO", ob_col.client_id.value, "TH2_Taker",
             ob_col.tif.value, tif.IOC.value]).check_order_fields_list(
            {ob_col.exec_sts.value: exe_sts.filled.value})
        FXOrderBook(case_id, session_id).set_filter(
            [ob_col.order_id.value, "AO", ob_col.qty.value, "5000000", ob_col.orig.value, "FIX", ob_col.lookup.value,
             "EUR/USD-SPO.SPO", ob_col.client_id.value, "TH2_Taker",
             ob_col.tif.value, tif.IOC.value]).check_second_lvl_fields_list(
            {ob_col.exec_sts.value: exe_sts.filled.value, ob_col.venue.value: "HSBC",
             ob_col.limit_price.value: "1.1814",
             ob_col.qty.value: "5,000,000"})
        # STEP 2
        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters(
            {'TimeInForce': '3', 'OrderQty': '5000000', 'Side': '2', 'Price': '1.18079'})
        new_order_sor.update_repeating_group('NoStrategyParameters', no_strategy_parameters)
        fix_manager_gtw.send_message_and_receive_response(new_order_sor)
        execution_report_filled_2 = FixMessageExecutionReportAlgoFX(). \
            set_params_from_new_order_single(new_order_sor, gateway_side_sell, status)
        fix_verifier.check_fix_message(fix_message=execution_report_filled_2,
                                       direction=DirectionEnum.FromQuod)

        FXOrderBook(case_id, session_id).set_filter(
            [ob_col.order_id.value, "AO", ob_col.qty.value, "5000000", ob_col.orig.value, "FIX", ob_col.lookup.value,
             "EUR/USD-SPO.SPO", ob_col.client_id.value, "TH2_Taker",
             ob_col.tif.value, tif.IOC.value]).check_order_fields_list(
            {ob_col.exec_sts.value: exe_sts.filled.value})
        FXOrderBook(case_id, session_id).set_filter(
            [ob_col.order_id.value, "AO", ob_col.qty.value, "5000000", ob_col.orig.value, "FIX", ob_col.lookup.value,
             "EUR/USD-SPO.SPO", ob_col.client_id.value, "TH2_Taker",
             ob_col.tif.value, tif.IOC.value]).check_second_lvl_fields_list(
            {ob_col.exec_sts.value: exe_sts.filled.value, ob_col.venue.value: "HSBC",
             ob_col.limit_price.value: "1.18079",
             ob_col.qty.value: "5,000,000"})

    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
