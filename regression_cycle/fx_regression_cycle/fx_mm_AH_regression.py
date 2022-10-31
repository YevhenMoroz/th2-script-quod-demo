from test_cases.fx.fx_mm_autohedging import QAP_T2495, QAP_2322, QAP_T2681, \
    QAP_T2682, QAP_T2854, QAP_T2697, QAP_T2569, QAP_T2542, QAP_T2847, QAP_T2713, QAP_T2474, QAP_T2472, QAP_T2473, \
    QAP_T2469, \
    QAP_T2840, QAP_T2679
from test_cases.fx.fx_mm_autohedging import QAP_T2862, QAP_T2855, \
    QAP_T2548, QAP_T2712, QAP_T2821, QAP_T2657, QAP_T2703, QAP_T2936, QAP_T2839, import_AH_layout, AH_Precondition
from test_cases.fx.fx_mm_autohedging import QAP_T2857, QAP_T2872, QAP_T2860, QAP_T2859, QAP_T2858, QAP_T2850, QAP_T2849, \
    QAP_T2848, \
    QAP_T2554
from test_cases.fx.fx_mm_autohedging.QAP_T2440 import QAP_T2440
from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe, prepare_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"FX_MM_Autohedger" if version is None else f"FX_MM_Autohedger | {version}", parent_id)
    session_id = set_session_id(target_server_win="ostronov")
    window_name = "Quod Financial - Quod site 314"
    fe_dir = Stubs.custom_config['qf_trading_fe_folder']
    fe_user = Stubs.custom_config['qf_trading_fe_user']
    fe_password = Stubs.custom_config['qf_trading_fe_password']
    data_set = FxDataSet()
    configuration = ComponentConfiguration("AutoHedger")
    try:
        # prepare_position()
        # Stubs.frontend_is_open = True
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id, fe_dir, fe_user, fe_password)
        # else:
        #     get_opened_fe(report_id, session_id, window_name)

        # import_AH_layout.execute(report_id, session_id)
        # AH_Precondition.execute(report_id)
        QAP_T2936.execute(report_id, session_id)
        QAP_T2872.execute(report_id, session_id)
        QAP_T2862.execute(report_id, session_id)
        QAP_T2860.execute(report_id, session_id)
        QAP_T2855.execute(report_id, session_id)
        QAP_2322.execute(report_id, session_id)
        QAP_T2548.execute(report_id, session_id)
        QAP_T2712.execute(report_id, session_id)
        QAP_T2657.execute(report_id, session_id)
        QAP_T2703.execute(report_id, session_id)
        QAP_T2839.execute(report_id, session_id)
        QAP_T2495.execute(report_id, session_id)
        QAP_T2821.execute(report_id, session_id)
        QAP_T2681.execute(report_id, session_id)
        QAP_T2682.execute(report_id, session_id)
        QAP_T2697.execute(report_id, session_id)
        QAP_T2569.execute(report_id, session_id)
        QAP_T2542.execute(report_id, session_id)
        QAP_T2840.execute(report_id, session_id)
        QAP_T2679.execute(report_id, session_id)
        # Rest API
        QAP_T2554.execute(report_id, session_id)
        QAP_T2848.execute(report_id, session_id)
        QAP_T2849.execute(report_id, session_id)
        QAP_T2850.execute(report_id, session_id)
        QAP_T2857.execute(report_id, session_id)
        QAP_T2858.execute(report_id, session_id)
        QAP_T2859.execute(report_id, session_id)
        QAP_T2854.execute(report_id, session_id)
        QAP_T2847.execute(report_id, session_id)
        QAP_T2713.execute(report_id, session_id)
        QAP_T2474.execute(report_id, session_id)
        QAP_T2473.execute(report_id, session_id)
        QAP_T2472.execute(report_id, session_id)
        QAP_T2469.execute(report_id, session_id)
        QAP_T2440(report_id, data_set=configuration.data_set)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
