from test_cases.fx.fx_taker_esp import QAP_T3097, QAP_T2987, QAP_T2743, \
    QAP_T2711, QAP_T2958, QAP_T2826,  QAP_T3112, QAP_T3106, QAP_T3094, \
    QAP_T2704, QAP_T2702, QAP_T2701, QAP_T2680, QAP_T2756, QAP_T2766, QAP_T2643, QAP_T2642, QAP_T2640, \
    QAP_T2685
from test_cases.fx.fx_mm_autohedging.QAP_T2440 import QAP_T2440
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_taker_esp.QAP_T2490 import QAP_T2490
from test_cases.fx.fx_taker_esp.QAP_T2491 import QAP_T2491
from test_cases.fx.fx_taker_esp.QAP_T2493 import QAP_T2493
from test_cases.fx.fx_taker_esp.QAP_T2532 import QAP_T2532
from test_cases.fx.fx_taker_esp.QAP_T2533 import QAP_T2533
from test_cases.fx.fx_taker_esp.QAP_T2624 import QAP_T2624
from test_cases.fx.fx_taker_esp.QAP_T2723 import QAP_T2723
from test_cases.fx.fx_taker_esp.QAP_T2724 import QAP_T2724
from test_cases.fx.fx_taker_esp.QAP_T2725 import QAP_T2725
from test_cases.fx.fx_taker_esp.QAP_T3090 import QAP_T3090
from test_cases.fx.fx_taker_esp.QAP_T3092 import QAP_T3092
from test_cases.fx.fx_taker_esp.QAP_T3093 import QAP_T3093
from test_cases.fx.fx_taker_esp.QAP_T3100 import QAP_T3100
from test_cases.fx.fx_taker_esp.QAP_T3104 import QAP_T3104
from test_cases.fx.fx_taker_esp.QAP_T3107 import QAP_T3107
from test_cases.fx.fx_wrapper.common_tools import stop_fxfh, start_fxfh
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def run_full_amount(report_id, session_id):
    """
    Need to run on 309 or 308
    """
    QAP_T2756.execute(report_id, session_id)


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"FX_Taker_ESP" if version is None else f"FX_Taker_ESP | {version}", parent_id)
    session_id = set_session_id(target_server_win="quod_11q")
    data_set = FxDataSet()
    configuration = ComponentConfiguration("ESP_Taker")
    window_name = "Quod Financial - Quod site 314"
    Stubs.frontend_is_open = True

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id, window_name)
        QAP_T2685.execute(report_id, session_id)
        QAP_T3112.execute(report_id, session_id)
        QAP_T3106.execute(report_id, session_id)
        QAP_T3107(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T3104(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T3100(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T3097.execute(report_id, session_id)
        QAP_T3094.execute(report_id, session_id)
        QAP_T3093(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()

        QAP_T3092(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T3091.execute(report_id, session_id)
        QAP_T3090(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T3087.execute(report_id, session_id)
        QAP_T3083.execute(report_id, session_id)
        QAP_T3001.execute(report_id, session_id)
        QAP_T2992.execute(report_id, session_id)
        QAP_T2987.execute(report_id, session_id)
        QAP_T2958.execute(report_id, session_id)
        QAP_T2832.execute(report_id, session_id)
        QAP_T2826.execute(report_id, session_id)
        QAP_T2766.execute(report_id, session_id)
        QAP_T2743.execute(report_id, session_id)
        QAP_T2725(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2724(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2723(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2711.execute(report_id, session_id)
        QAP_T2704.execute(report_id, session_id)
        QAP_T2702.execute(report_id, session_id)
        QAP_T2701.execute(report_id, session_id)
        QAP_T2680.execute(report_id, session_id)
        QAP_T2654.execute(report_id, session_id)
        QAP_T2624(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2607.execute(report_id, session_id)
        QAP_T2591.execute(report_id, session_id)
        QAP_T2540.execute(report_id, session_id)
        QAP_T2533(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2532(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2525.execute(report_id, session_id)
        QAP_T2524.execute(report_id, session_id)
        QAP_T2521.execute(report_id, session_id)
        QAP_T2493(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2491(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2490(report_id=report_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2489.execute(report_id, session_id, configuration.data_set)
        QAP_T2488.execute(report_id, session_id, configuration.data_set)
        QAP_T8648(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8667(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        stop_fxfh()
        QAP_T2643(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2642(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2640(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        start_fxfh()

        # run_full_amount(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
