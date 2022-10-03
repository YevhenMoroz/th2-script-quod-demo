import os
from pathlib import Path

from custom.basic_custom_actions import timestamps


from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from test_cases.eq.Commissions.QAP_T7132 import QAP_T7132
from test_cases.eq.Commissions.QAP_T7149 import QAP_T7149
from test_cases.eq.Commissions.QAP_T7229 import QAP_T7229
from test_cases.eq.Commissions.QAP_T7281 import QAP_T7281
from test_cases.eq.Commissions.QAP_T7299 import QAP_T7299
from test_cases.eq.Commissions.QAP_T7308 import QAP_T7308
from test_cases.eq.Commissions.QAP_T7310 import QAP_T7310
from test_cases.eq.Commissions.QAP_T7358 import QAP_T7358
from test_cases.eq.Commissions.QAP_T7376 import QAP_T7376
from test_cases.eq.Commissions.QAP_T7534 import QAP_T7534
from test_cases.eq.Commissions.QAP_T7525 import QAP_T7525
from test_cases.eq.Commissions.QAP_T7514 import QAP_T7514
from test_cases.eq.Commissions.QAP_T7512 import QAP_T7512
from test_cases.eq.Commissions.QAP_T7511 import QAP_T7511
from test_cases.eq.Commissions.QAP_T7497 import QAP_T7497
from test_cases.eq.Commissions.QAP_T7489 import QAP_T7489
from test_cases.eq.Commissions.QAP_T7415 import QAP_T7415
from test_cases.eq.Commissions.QAP_T7391 import QAP_T7391
from test_cases.eq.Commissions.QAP_T7390 import QAP_T7390
from test_cases.eq.Commissions.QAP_T7389 import QAP_T7389
from test_cases.eq.Commissions.QAP_T7383 import QAP_T7383
from test_cases.eq.Commissions.QAP_T7357 import QAP_T7357
from test_cases.eq.Commissions.QAP_T7172 import QAP_T7172
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None, version=None):
    # Store case start time
    seconds, nanos = timestamps()
    configuration = ComponentConfiguration("Commissions")
    report_id = bca.create_event(f"Commissions Analysis" if version is None else f"Commissions Analysis | {version}", parent_id)
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle/layouts")
    layout_name = "all_columns_layout.xml"
    try:
        base_main_window.open_fe(test_id, fe_env=fe_env, is_open=False)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_T7534(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7525(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7514(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7512(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7511(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7497(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7496(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \1
        #     .execute()
        QAP_T7489(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7415(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7391(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7390(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7389(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7383(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7376(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7358(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7357(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7310(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7308(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7299(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7281(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7269(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7247(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7229(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7172(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7156(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \1
        #     .execute()
        QAP_T7149(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7132(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Commission regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
