import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Counterpart.QAP_T6996 import QAP_T6996
from test_cases.eq.Counterpart.QAP_T7135 import QAP_T7135
from test_cases.eq.Counterpart.QAP_T7155 import QAP_T7155
from test_cases.eq.Counterpart.QAP_T7302 import QAP_T7302
from test_cases.eq.Counterpart.QAP_T7369 import QAP_T7369
from test_cases.eq.Counterpart.QAP_T7394 import QAP_T7394
from test_cases.eq.Counterpart.QAP_T7444 import QAP_T7444
from test_cases.eq.Counterpart.QAP_T7471 import QAP_T7471
from test_cases.eq.Counterpart.QAP_T7472 import QAP_T7472
from test_cases.eq.Counterpart.QAP_T7473 import QAP_T7473
from test_cases.eq.Counterpart.QAP_T7474 import QAP_T7474
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version='5.1.167.180'):
    report_id = bca.create_event(f"Counterpart Analysis" if version is None else f"Counterpart Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Counterparts")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle/layouts")
    layout_name = "all_columns_layout.xml"

    try:
        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        # base_main_window.import_layout(layout_path, layout_name)
        QAP_T7471(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7135(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7369(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7302(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7155(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7444(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7474(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7473(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7472(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6996(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7394(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Counterparts regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
