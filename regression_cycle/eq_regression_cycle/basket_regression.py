import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Basket.QAP_5024 import QAP_5024
from test_cases.eq.Basket.QAP_5031 import QAP_5031
from test_cases.eq.Basket.QAP_T6956 import QAP_T6956
from test_cases.eq.Basket.QAP_T6957 import QAP_T6957
# from test_cases.eq.Basket.QAP_T7017 import QAP_T7017
# from test_cases.eq.Basket.QAP_T6957 import QAP_T6957
# from test_cases.eq.Basket.QAP_T6956 import QAP_T6956
from test_cases.eq.Basket.QAP_T7017 import QAP_T7017
from test_cases.eq.Basket.QAP_T7077 import QAP_T7077
from test_cases.eq.Basket.QAP_T7078 import QAP_T7078
from test_cases.eq.Basket.QAP_T7109 import QAP_T7109
from test_cases.eq.Basket.QAP_T7199 import QAP_T7199
from test_cases.eq.Basket.QAP_T7201 import QAP_T7201
from test_cases.eq.Basket.QAP_T7332 import QAP_T7332
from test_cases.eq.Basket.QAP_T7338 import QAP_T7338
from test_cases.eq.Basket.QAP_T7339 import QAP_T7339
from test_cases.eq.Basket.QAP_T7340 import QAP_T7340
# from test_cases.eq.Basket.QAP_T7361 import QAP_T7361
from test_cases.eq.Basket.QAP_T7341 import QAP_T7341
from test_cases.eq.Basket.QAP_T7361 import QAP_T7361
from test_cases.eq.Basket.QAP_T7378 import QAP_T7378
from test_cases.eq.Basket.QAP_T7393 import QAP_T7393
from test_cases.eq.Basket.QAP_T7397 import QAP_T7397
from test_cases.eq.Basket.QAP_T7400 import QAP_T7400
from test_cases.eq.Basket.QAP_T7401 import QAP_T7401
from test_cases.eq.Basket.QAP_T7402 import QAP_T7402
from test_cases.eq.Basket.QAP_T7404 import QAP_T7404
from test_cases.eq.Basket.QAP_T7405 import QAP_T7405
from test_cases.eq.Basket.QAP_T7406 import QAP_T7406
from test_cases.eq.Basket.QAP_T7408 import QAP_T7408
from test_cases.eq.Basket.QAP_T7429 import QAP_T7429
from test_cases.eq.Basket.QAP_T7431 import QAP_T7431
# from test_cases.eq.Basket.QAP_T7433 import QAP_T7433
from test_cases.eq.Basket.QAP_T7433 import QAP_T7433
from test_cases.eq.Basket.QAP_T7439 import QAP_T7439
from test_cases.eq.Basket.QAP_T7441 import QAP_T7441
from test_cases.eq.Basket.QAP_T7447 import QAP_T7447
from test_cases.eq.Basket.QAP_T7448 import QAP_T7448
from test_cases.eq.Basket.QAP_T7449 import QAP_T7449
from test_cases.eq.Basket.QAP_T7450 import QAP_T7450
from test_cases.eq.Basket.QAP_T7453 import QAP_T7453
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"Basket Analysis" if version is None else f"Basket Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("BasketTrading")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle/layouts")
    layout_name = "basket_templates_v172_layout.xml"
    try:
        base_main_window.open_fe(test_id, fe_env=fe_env, is_open=False)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_T7453(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7450(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7449(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7448(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7447(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7441(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7439(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7433(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7431(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7429(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7408(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7406(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7405(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7404(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7402(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7401(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7400(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7397(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7393(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7378(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7361(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7341(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7340(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7339(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7338(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7332(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_5024(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_5031(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7201(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7199(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7109(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7078(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7077(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7017(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6957(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6956(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Basket regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
