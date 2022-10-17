import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime

from Test_UI import Test_UI
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from send_rqf import Send_RFQ
from stubs import Stubs

from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2448 import QAP_T2448

from test_cases.fx.send_md import QAP_MD

from test_framework.configurations.component_configuration import ComponentConfiguration
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(f'[alexs] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    # initializing dataset
    # initializing FE session
    session_id = set_session_id(target_server_win="ostronov")

    window_name = "Quod Financial - Quod site 309"
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    # endregion
    Stubs.frontend_is_open = True

    try:

        # QAP_MD(report_id, data_set=configuration.data_set).execute()

        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Test_UI(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T8544(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2448(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # rm = RuleManager()
        # # rm.add_QuodMDAnswerRule("fix-fh-314-luna")
        # rm.print_active_rules()


        end = time.time()
        print(f"Test duration is {end - start_time} seconds")

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        pass


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()