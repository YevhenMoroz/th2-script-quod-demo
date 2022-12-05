import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.GatingRules.QAP_T4295 import QAP_T4295
from test_cases.eq.GatingRules.QAP_T4296 import QAP_T4296
from test_cases.eq.GatingRules.QAP_T4305 import QAP_T4305
from test_cases.eq.GatingRules.QAP_T4316 import QAP_T4316
from test_cases.eq.GatingRules.QAP_T4317 import QAP_T4317
from test_cases.eq.GatingRules.QAP_T4318 import QAP_T4318
from test_cases.eq.GatingRules.QAP_T4325 import QAP_T4325
from test_cases.eq.GatingRules.QAP_T4326 import QAP_T4326
from test_cases.eq.GatingRules.QAP_T4327 import QAP_T4327
from test_cases.eq.GatingRules.QAP_T4328 import QAP_T4328
from test_cases.eq.GatingRules.QAP_T4329 import QAP_T4329
from test_cases.eq.GatingRules.QAP_T4347 import QAP_T4347
from test_cases.eq.GatingRules.QAP_T4684 import QAP_T4684

from test_cases.eq.GatingRules.QAP_T4928 import QAP_T4928
from test_cases.eq.GatingRules.QAP_T4929 import QAP_T4929
from test_cases.eq.GatingRules.QAP_T4930 import QAP_T4930
from test_cases.eq.GatingRules.QAP_T4931 import QAP_T4931
from test_cases.eq.GatingRules.QAP_T4951 import QAP_T4951
from test_cases.eq.GatingRules.QAP_T4952 import QAP_T4952
from test_cases.eq.GatingRules.QAP_T4954 import QAP_T4954
from test_cases.eq.GatingRules.QAP_T4955 import QAP_T4955
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"GatingRules" if version is None else f"GatingRules | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Gating_rules")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)

    try:
        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)

        QAP_T4296(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4329(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4684(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4325(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4326(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4327(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4347(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4929(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4928(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4930(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4931(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T4953(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T4317(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4318(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4328(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4305(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4952(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4955(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4954(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4951(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4316(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T8756(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T4295(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Acceptance list was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        Stubs.win_act.unregister(session_id)
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
