import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from custom.tenor_settlement_date import broken_w1w2
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.win_gui_wrappers.forex.fx_child_book import FXChildBook
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

alias_gtw = "fix-sell-esp-t-314-stand"


def execute(report_id, session_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        new_order_sor_broken = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters(
            {'TimeInForce': '1', 'SettlType': 'B', 'SettlDate': broken_w1w2()}). \
            update_fields_in_component('Instrument', {'SecurityType': 'FXFWD'}). \
            remove_parameter('TargetStrategy')
        FixManager(alias_gtw, case_id).send_message(fix_message=new_order_sor_broken)



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
