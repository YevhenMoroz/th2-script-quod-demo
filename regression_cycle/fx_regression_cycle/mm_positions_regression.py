from quod_qa.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_positions import QAP_2505, QAP_2378, QAP_2491, QAP_2492, QAP_2494, QAP_2496, QAP_2497, \
    QAP_1897, QAP_1898, QAP_2506, QAP_2508, QAP_2500, QAP_2779, QAP_3484, import_position_layout, preconditions_for_pos
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe, prepare_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('FX MM Positions regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    fe_dir = Stubs.custom_config['qf_trading_fe_folder']
    fe_user = Stubs.custom_config['qf_trading_fe_user']
    fe_password = Stubs.custom_config['qf_trading_fe_password']

    try:
        prepare_position()
        Stubs.frontend_is_open = False
        if not Stubs.frontend_is_open:
            prepare_fe(report_id, session_id, fe_dir, fe_user, fe_password)
        else:
            get_opened_fe(report_id, session_id)

        import_position_layout.execute(report_id, session_id)
        preconditions_for_pos.execute(report_id, session_id)

        QAP_1897.execute(report_id, session_id)
        QAP_1898.execute(report_id, session_id)
        QAP_2378.execute(report_id, session_id)
        QAP_2491.execute(report_id, session_id)
        QAP_2492.execute(report_id, session_id)
        QAP_2494.execute(report_id, session_id)
        QAP_2496.execute(report_id, session_id)
        QAP_2497.execute(report_id, session_id)
        QAP_2500.execute(report_id, session_id)
        QAP_2505.execute(report_id, session_id)
        QAP_2506.execute(report_id, session_id)
        QAP_2508.execute(report_id, session_id)
        QAP_2779.execute(report_id, session_id)
        QAP_3484.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)
        # close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
