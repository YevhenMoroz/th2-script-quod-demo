import logging
import time
from datetime import datetime

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from send_rqf import Send_RFQ
from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_T2458
from test_cases.fx.fx_mm_esp.QAP_2075 import QAP_2075
from test_cases.fx.fx_mm_esp.QAP_T2497 import QAP_T2497


from test_cases.fx.fx_taker_esp import QAP_5600
from test_cases.fx.fx_taker_esp.QAP_6593 import QAP_6593
from test_cases.fx.fx_taker_esp.QAP_8090 import QAP_8090
from test_cases.fx.fx_taker_rfq.QAP_568 import QAP_568

from test_cases.fx.qs_fx_routine import DepositAndLoan
from test_cases.fx.qs_fx_routine.dep_and_loan import DepAndLoan
from test_cases.fx.send_md import QAP_MD
from test_framework.configurations.component_configuration import ComponentConfiguration
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

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

        QAP_MD(report_id, data_set=configuration.data_set).execute()
        # QAP_T2978(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T2458.execute(report_id)
        # QAP_T2497().execute(report_id)

        end = time.time()
        print(f"Test duration is {end - start_time} seconds")

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)
        pass


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
