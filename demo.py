import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime

from Test_UI import Test_UI
from custom import basic_custom_actions as bca
from regression_cycle.fx_regression_cycle import fx_mm_rfq_regression, rfq_taker_regression
from rule_management import RuleManager
from send_rqf import Send_RFQ
from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_1559
from test_cases.fx.fx_mm_esp.QAP_1518 import QAP_1518
from test_cases.fx.fx_mm_esp.QAP_1597 import QAP_1597
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389
from test_cases.fx.fx_mm_rfq.QAP_3610 import QAP_3610
from test_cases.fx.fx_mm_rfq.QAP_6192 import QAP_6192
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3734 import QAP_3734
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3761 import QAP_3761
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3762 import QAP_3762
from test_cases.fx.fx_mm_rfq.interpolation.QAP_5992 import QAP_5992

from test_cases.fx.fx_mm_rfq.interpolation.QAP_6147 import QAP_6147
from test_cases.fx.fx_mm_rfq.rejection.QAP_3764 import QAP_3764
from test_cases.fx.fx_taker_esp import QAP_5600
from test_cases.fx.fx_taker_esp.QAP_6593 import QAP_6593
from test_cases.fx.fx_taker_esp.QAP_8090 import QAP_8090

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
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[alexs] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    # initializing dataset
    # initializing FE session
    session_id = set_session_id(target_server_win="ostronov")

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
        # rm.remove_rule_by_id(8)
        # rm.print_active_rules()
        # QAP_568(report_id, session_id, configuration.data_set).execute()
        # Test_UI(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # DepositAndLoan.execute(report_id)

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # EarlyRedemption(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_5389().execute(report_id)
        # QAP_1559.execute(report_id)

        # QAP_5992(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3764(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # rfq_taker_regression.test_run(parent_id=report_id)
        # fx_mm_rfq_regression.test_run(parent_id=report_id)

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
