import os
from pathlib import Path

from custom.basic_custom_actions import timestamps

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from test_cases.eq.Gateway.QAP_T7015 import QAP_T7015
from test_cases.eq.Gateway.QAP_T7106 import QAP_T7106
from test_cases.eq.Gateway.QAP_T7167 import QAP_T7167
from test_cases.eq.Gateway.QAP_T7169 import QAP_T7169
from test_cases.eq.Gateway.QAP_T7170 import QAP_T7170
from test_cases.eq.Gateway.QAP_T7171 import QAP_T7171
from test_cases.eq.Gateway.QAP_T7173 import QAP_T7173
from test_cases.eq.Gateway.QAP_T7223 import QAP_T7223
from test_cases.eq.Gateway.QAP_T7323 import QAP_T7323
from test_cases.eq.Gateway.QAP_T7324 import QAP_T7324
from test_cases.eq.Gateway.QAP_T7499 import QAP_T7499
from test_cases.eq.Gateway.QAP_T7500 import QAP_T7500
from test_cases.eq.Gateway.QAP_T7501 import QAP_T7501
from test_cases.eq.Gateway.QAP_T7502 import QAP_T7502
from test_cases.eq.Gateway.QAP_T7503 import QAP_T7503
from test_cases.eq.Gateway.QAP_T7504 import QAP_T7504
from test_cases.eq.Gateway.QAP_T7506 import QAP_T7506
from test_cases.eq.Gateway.QAP_T7507 import QAP_T7507
from test_cases.eq.Gateway.QAP_T7514 import QAP_T7514
from test_cases.eq.Gateway.QAP_T7515 import QAP_T7515
from test_cases.eq.Gateway.QAP_T7516 import QAP_T7516
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version='5.1.166.179'):
    report_id = bca.create_event(f"Gateway Analysis" if version is None else f"Gateway Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Gateway")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle\layouts")
    layout_name = "all_columns_layout.xml"
    try:
        # base_main_window.open_fe(test_id, fe_env=fe_env)
        # base_main_window.import_layout(layout_path, layout_name)
        QAP_T7223(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7515(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7516(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7169(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7323(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7170(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7324(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7502(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7506(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7503(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7500(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7504(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7167(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7171(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7514(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7173(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7106(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7507(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7501(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7015(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7499(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()






    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Gateway regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        # base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
