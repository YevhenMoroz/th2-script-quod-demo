import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from my_methods import send_md, send_rfq, test_ob
from rule_management import RuleManager
from test_cases.fx.fx_mm_esp import QAP_1643, QAP_6145, QAP_2966
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389

from stubs import Stubs
from test_cases.fx.fx_mm_rfq import QAP_4505, for_test_77679, QAP_5848, QAP_5856, QAP_4085, QAP_2101, QAP_2092, \
    QAP_2296, QAP_2345, QAP_3234, QAP_3004, QAP_5992
from test_cases.fx.fx_mm_rfq.interpolation import QAP_3739, QAP_3806, QAP_3766, QAP_3762
from test_cases.fx.fx_mm_rfq.rejection import QAP_3764, QAP_3740, QAP_3720
from test_cases.fx.fx_taker_esp import QAP_5564, QAP_5589, QAP_5591, QAP_5598, QAP_5600, QAP_5006, QAP_4456, QAP_2373
from test_cases.fx.qs_fx_routine import QAP_5176
from test_cases.fx.ui_wrappers import wrapper_test
from win_gui_modules.utils import set_session_id, get_opened_fe, prepare_fe_2

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run

    report_id = bca.create_event("ostronov " + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial"
    session_id = set_session_id()
    start_time = datetime.now()
    print(f"Start time :{start_time}")

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)
        # rm= RuleManager()
        # rm.remove_rule_by_id(9)
        # rm.print_active_rules()


        # QAP_5006.execute(report_id, session_id)
        # QAP_2345.execute(report_id)
        # for_test_77679.execute(report_id, session_id)
        # send_rfq.execute(report_id)
        # QAP_3004.execute(report_id, session_id)
        QAP_5992.execute(report_id)
        # QAP_5006.execute(report_id, session_id)
        # QAP_3739.execute(report_id)
        # QAP_3720.execute(report_id)
        # QAP_3762.execute(report_id)

        print(f"Duration is {datetime.now()-start_time}")
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
