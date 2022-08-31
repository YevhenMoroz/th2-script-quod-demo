from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_mm_positions import QAP_T2805, QAP_T2829, QAP_T2813, QAP_T2812, QAP_T2811, QAP_T2810, QAP_T2809, \
    QAP_T2933, QAP_T2932, QAP_T2804, QAP_T2803, QAP_T2808, QAP_T2761, QAP_T2630, import_position_layout, preconditions_for_pos, \
    QAP_T2935, QAP_T2934
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe, prepare_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"FX_MM_Position" if version is None else f"FX_MM_Position | {version}", parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    fe_dir = Stubs.custom_config['qf_trading_fe_folder']
    fe_user = Stubs.custom_config['qf_trading_fe_user']
    fe_password = Stubs.custom_config['qf_trading_fe_password']

    try:
        data_set = FxDataSet()
        configuration = ComponentConfiguration("Position")
        prepare_position()
        Stubs.frontend_is_open = False
        if not Stubs.frontend_is_open:
            prepare_fe(report_id, session_id, fe_dir, fe_user, fe_password)
        else:
            get_opened_fe(report_id, session_id)

        import_position_layout.execute(report_id, session_id)
        preconditions_for_pos.execute(report_id, session_id)

        QAP_T2935.execute(report_id, session_id)
        QAP_T2934.execute(report_id, session_id)
        QAP_T2933.execute(report_id, session_id)
        QAP_T2932.execute(report_id, session_id)
        QAP_T2829.execute(report_id, session_id)
        QAP_T2813.execute(report_id, session_id)
        QAP_T2812.execute(report_id, session_id)
        QAP_T2811.execute(report_id, session_id)
        QAP_T2810.execute(report_id, session_id)
        QAP_T2809.execute(report_id, session_id)
        QAP_T2808.execute(report_id, session_id)
        QAP_T2805.execute(report_id, session_id)
        QAP_T2804.execute(report_id, session_id)
        QAP_T2803.execute(report_id, session_id)
        QAP_T2761.execute(report_id, session_id)
        QAP_T2630.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)
        # close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
