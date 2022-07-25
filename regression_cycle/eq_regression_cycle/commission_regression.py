import os
from pathlib import Path

from custom.basic_custom_actions import timestamps


from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from test_cases.eq.Commissions.QAP_2998 import QAP_2998
from test_cases.eq.Commissions.QAP_3285 import QAP_3285
from test_cases.eq.Commissions.QAP_3307 import QAP_3307
from test_cases.eq.Commissions.QAP_3310 import QAP_3310
from test_cases.eq.Commissions.QAP_3312 import QAP_3312
from test_cases.eq.Commissions.QAP_3350 import QAP_3350
from test_cases.eq.Commissions.QAP_3380 import QAP_3380
from test_cases.eq.Commissions.QAP_3953 import QAP_3953
from test_cases.eq.Commissions.QAP_4231 import QAP_4231
from test_cases.eq.Commissions.QAP_4232 import QAP_4232
from test_cases.eq.Commissions.QAP_4255 import QAP_4255
from test_cases.eq.Commissions.QAP_4349 import QAP_4349
from test_cases.eq.Commissions.QAP_4535 import QAP_4535
from test_cases.eq.Commissions.QAP_5734 import QAP_5734
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None):
    report_id = bca.create_event('Commissions ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Commissions")
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
        QAP_2998(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3285(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3307(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3310(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3312(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3350(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_3351(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_3380(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3953(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4231(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4232(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4255(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4349(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_4373(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_4489(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_4535(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_4827(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_4859(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_4927(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_5009(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_5081(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_5344(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_5385(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_5734(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_5859(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_5881(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_5951(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Commission regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        Stubs.win_act.unregister(session_id)
        # base_main_window.close_fe()



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
