import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from my_methods import send_md, send_rfq, test_ob
from rule_management import RuleManager

from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_2750, QAP_6148
from test_cases.fx.fx_mm_esp.QAP_1589 import QAP_1589
from test_cases.fx.fx_mm_rfq import QAP_3494

from test_framework.core.example_of_ideal_test_case_ui import QAP_Example
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
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
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id()
    start_time = datetime.now()
    print(f"Start time :{start_time}")
    data_set = FxDataSet()

    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        # rm= RuleManager()
        # rm.remove_rule_by_id(15)
        # rm.add_fx_md_to("fix-fh-314-luna")
        # rm.print_active_rules()
        # send_md.execute(report_id, 1.18123, 1.18223)

        QAP_1589(report_id, session_id, data_set).execute()

        # QAP_3805.execute(report_id)

        print(f"Duration is {datetime.now() - start_time}")
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
