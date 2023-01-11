import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime

from Test_UI import Test_UI
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from send_rqf import Send_RFQ
from stubs import Stubs

from test_cases.fx.fx_mm_esp.QAP_T2719 import QAP_T2719

from test_cases.fx.fx_mm_esp.QAP_T9406 import QAP_T9406

from test_cases.fx.fx_taker_esp import QAP_T2487
from test_cases.fx.fx_wrapper.common_tools import restart_qs_rfq_fix_th2

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

    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    # endregion
    Stubs.frontend_is_open = True

    try:

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T2487.execute(report_id, session_id=None, data_set=configuration.data_set)

        # QAP_T8544(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9406(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # restart_qs_rfq_fix_th2()


        # rm = RuleManager()
        # rm.remove_rule_by_id(5)
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