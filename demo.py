import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Care.QAP_T7685 import QAP_T7685
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(f'[alexs] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    # initializing dataset
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing FE session
    # session_id = set_session_id(target_server_win="ostronov")

    window_name = "Quod Financial - Quod site 309"
    session_id = set_session_id(pc_name)
    base_main_window = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    configuration = ComponentConfiguration("YOUR_COMPONENT")  # <--- provide your component from XML (DMA, iceberg, etc)
    fe_env = configuration.environment.get_list_fe_environment()[0]
    fe_folder = fe_env.folder
    fe_user = fe_env.user_1
    fe_pass = fe_env.password_1
    # endregion
    Stubs.frontend_is_open = True

    try:

        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        QAP_T7685(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment) \
            .execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
