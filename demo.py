import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_mm_esp.QAP_7160 import QAP_7160
from test_cases.fx.fx_mm_rfq import QAP_4505, QAP_5848
from test_cases.fx.fx_mm_rfq.QAP_7168 import QAP_7168
from test_cases.fx.fx_mm_rfq.QAP_7287 import QAP_7287
from test_cases.fx.fx_taker_rfq.QAP_6 import QAP_6
from test_cases.fx.send_md import QAP_MD
from test_framework.configurations.component_configuration import ComponentConfiguration
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset

    # initializing FE session
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id(target_server_win="quod_11q")
    window_name = "Quod Financial - Quod site 314"
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    # endregion
    Stubs.frontend_is_open = True

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id, window_name)

        # rm = RuleManager()
        # rm.print_active_rules()

        # Testing(report_id, session_id, configuration.data_set).execute()
        # QAP_6(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set).execute()
        QAP_7160(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()


        end = time.time()
        print(f"Test duration is {end - start_time} seconds")

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
