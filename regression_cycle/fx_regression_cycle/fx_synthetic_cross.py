from test_cases.fx.fx_mm_esp.QAP_T2719 import QAP_T2719
from test_cases.fx.fx_mm_esp.QAP_T2782 import QAP_T2782
from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_mm_positions import QAP_T2805, QAP_T2829, QAP_T2813, QAP_T2812, QAP_T2811, QAP_T2810, QAP_T2809, \
    QAP_T2933, QAP_T2932, QAP_T2804, QAP_T2803, QAP_T2808, QAP_T2761, QAP_T2630, import_position_layout, \
    preconditions_for_pos, \
    QAP_T2935, QAP_T2934
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe, prepare_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version="5.1.165.178"):
    report_id = bca.create_event(f"FX_Synthetic" if version is None else f"FX_Synthetic | {version}", parent_id)
    session_id = set_session_id(target_server_win="ostronov")
    main_window_name = "Quod Financial - Quod site 314"
    configuration = ComponentConfiguration("FX_Synthetic_cross")

    try:
        # prepare_position()
        # Stubs.frontend_is_open = False
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id, main_window_name)
        #
        # import_position_layout.execute(report_id, session_id)
        # preconditions_for_pos.execute(report_id, session_id)

        QAP_T2782(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2719(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)
        # close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
