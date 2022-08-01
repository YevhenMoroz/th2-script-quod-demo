import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Counterpart.QAP_3503 import QAP_3503
from test_cases.eq.Counterpart.QAP_3509 import QAP_3509
from test_cases.eq.Counterpart.QAP_3510 import QAP_3510
from test_cases.eq.Counterpart.QAP_3743 import QAP_3743
from test_cases.eq.Counterpart.QAP_4111 import QAP_4111
from test_cases.eq.Counterpart.QAP_4421 import QAP_4421
# from test_cases.eq.Counterpart.QAP_4903 import QAP_4903
# from test_cases.eq.Counterpart.QAP_5860 import QAP_5860
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Counterparts ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Counterparts")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("eq_regression_cycle/layouts")
    layout_name = "all_columns_v172_layout.xml"

    try:
        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_3503(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3509(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3510(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_3536(report_id, session_id).execute() need to rewrite
        QAP_3743(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4111(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4421(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_4903(report_id, session_id).execute()
        # QAP_5860(report_id, session_id).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Counterparts regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        Stubs.win_act.unregister(session_id)
        # base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
