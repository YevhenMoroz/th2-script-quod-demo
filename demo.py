import logging
import time
from datetime import datetime

from custom import basic_custom_actions as bca
from rule_management import RuleManager

from stubs import Stubs
from test_cases.fx.fx_mm_autohedging.QAP_T2440 import QAP_T2440
from test_cases.fx.fx_mm_autohedging.QAP_T2468 import QAP_T2468
from test_cases.fx.fx_mm_positions.QAP_T2809 import QAP_T2809

from test_cases.fx.fx_mm_positions.QAP_T2813 import QAP_T2813
from test_cases.fx.fx_mm_positions.QAP_T8424 import QAP_T8424
from test_cases.fx.fx_mm_rfq.QAP_T8020 import QAP_T8020
from test_cases.fx.fx_taker_esp import QAP_T2496
from test_cases.fx.send_md import QAP_MD

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(f'[alexs] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    # endregion

    try:
        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # QAP_T2496.execute(report_id, session_id=None, data_set=configuration.data_set)

        QAP_T2440(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # rule_manager = RuleManager()
        # rule_manager.remove_rule_by_id(2)
        # rule_manager.print_active_rules()

        end = time.time()
        print(f"Test duration is {end - start_time} seconds")

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
