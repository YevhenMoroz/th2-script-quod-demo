import logging
from custom import basic_custom_actions as bca
from pathlib import Path

from custom.tenor_settlement_date import broken_w1w2
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX

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
