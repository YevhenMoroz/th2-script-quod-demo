import logging
import time
from datetime import datetime

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_mm_positions.QAP_T8544 import  QAP_T8544
from test_cases.fx.fx_taker_esp.QAP_T7940 import QAP_T7940
from test_cases.fx.send_md import QAP_MD

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(f'[alexs] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    # initializing dataset
    # initializing FE session
    # session_id = set_session_id(target_server_win="ostronov")

    window_name = "Quod Financial - Quod site 309"
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
        # rm.add_TRADE_ESP_test("fix-bs-esp-314-luna-standard")
        # rm.print_active_rules()
        # QAP_568(report_id, session_id, configuration.data_set).execute()
        # Test_UI(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # DepositAndLoan.execute(report_id)

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # QAP_2075(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2481(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T8544(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T7940(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_5591.execute(report_id, session_id)
        # QAP_3414.execute(report_id)

        # QAP_T2497().execute(report_id)

        end = time.time()
        print(f"Test duration is {end - start_time} seconds")

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        # Stubs.win_act.unregister(session_id)
        pass


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
