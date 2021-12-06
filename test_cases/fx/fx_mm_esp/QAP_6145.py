import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.win_gui_wrappers.data_set import OrderBookColumns, TimeInForce, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

alias_gtw = "fix-sell-esp-m-314luna-stand"

no_related_symbol = [
    {
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT',
            'Product': '4',
        },
        'SettlType': '',
    }
]
client = "Silver1"
bands = ["1000000", "5000000", "10000000"]


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    fix_manager_gtw = FixManager(alias_gtw, case_id)
    fix_verifier = FixVerifier(alias_gtw, case_id)
    try:
        market_data_request = FixMessageMarketDataRequestFX().set_md_req_parameters(). \
            change_parameters({'SenderSubID': client}). \
            update_repeating_group('NoRelatedSymbols', no_related_symbol)

        fix_manager_gtw.send_message_and_receive_response(market_data_request, case_id)
        md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        md_snapshot.set_params_for_md_response(market_data_request, bands)

        time.sleep(4)
        fix_verifier.check_fix_message(fix_message=md_snapshot, direction=DirectionEnum.FromQuod,
                                       key_parameters=["MDReqID"])


    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        market_data_request.change_parameters({"SubscriptionRequestType": "2"})
        fix_manager_gtw.send_message(market_data_request)
