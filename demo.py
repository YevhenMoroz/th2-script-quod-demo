import logging
import time
from datetime import datetime

from custom import basic_custom_actions as bca

from stubs import Stubs

from test_cases.fx.fx_mm_autohedging.QAP_T9220 import QAP_T9220
from test_cases.fx.fx_mm_positions.QAP_T10649 import QAP_T10649
from test_cases.fx.fx_mm_positions.QAP_T10840 import QAP_T10840
from test_cases.fx.fx_mm_positions.QAP_T11216 import QAP_T11216
from test_cases.fx.fx_mm_rfq.QAP_T8020 import QAP_T8020
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
    Stubs.frontend_is_open = True

    try:

        QAP_T8020(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # rule_manager = RuleManager(Simulators.connectivity)
        # # rule_manager.add_TRFQ("fix-bs-rfq-314-luna-standard")
        # rule_manager.remove_rules_by_alias("fix-fss-order-buy-side-312-mars")
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
