import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from my_methods import send_md
from rule_management import RuleManager
from test_cases.fx.fx_mm_esp import QAP_1643
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389

from stubs import Stubs
from test_cases.fx.fx_mm_rfq import QAP_4505, for_test_77679
from win_gui_modules.utils import set_session_id, get_opened_fe, prepare_fe_2

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run

    report_id = bca.create_event("ostronov" + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id()
    start_time = datetime.now()
    print(f"Start time :{start_time}")

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)


        # rm= RuleManager()
        # rm.remove_rule_by_id(3)
        # # rm.add_fx_md_to("fix-fh-314-luna")
        # rm.print_active_rules()
        # # rm.remove_rule_by_id(48)
        # rm.print_active_rules()
        # send_md.execute(report_id, 1.19, 1.21)
        QAP_4505.execute(report_id)
        # for_test_77679.execute(report_id, session_id)
        # QAP_1643.execute(report_id, session_id)
        # QAP_5389().execute(report_id)

        # SendMD.execute(report_id)
        # send_rfq.execute(report_id)

        # QAP_5369_not_ready.execute(report_id)
        print(f"Duration is {datetime.now()-start_time}")
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
