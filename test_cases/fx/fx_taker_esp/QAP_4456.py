import logging
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from pathlib import Path

from custom.tenor_settlement_date import broken_w1w2
from test_framework.fix_wrappers import DataSet
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TimeInForce, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker

alias_gtw = "fix-sell-esp-t-314-stand"
symbol = 'EUR/USD'

# Gateway Side
gateway_side_sell = DataSet.GatewaySide.Sell
ob_col = OrderBookColumns
tif = TimeInForce
exe_sts = ExecSts
status = DataSet.Status.Fill


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    fix_manager_gtw = FixManager(alias_gtw, case_id)
    fix_verifier = FixVerifier(alias_gtw, case_id)
    try:

        # STEP 1
        new_order_sor = FixMessageNewOrderSingleTaker().set_default_SOR().change_parameters(
            {'TimeInForce': '1',"SettlType": "B", "OrdType": "2","HandlInst": "3", })
        fix_manager_gtw.send_message_and_receive_response(new_order_sor)
        execution_report_filled_1 = FixMessageExecutionReportAlgoFX(). \
            set_params_from_new_order_single(new_order_sor, gateway_side_sell, status)
        time.sleep(5)
        fix_verifier.check_fix_message(fix_message=execution_report_filled_1,
                                       direction=DirectionEnum.FromQuod)

    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
