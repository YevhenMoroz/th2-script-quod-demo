import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime

from Test_UI import Test_UI
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from send_rqf import Send_RFQ
from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_2966, QAP_2012, QAP_2034, QAP_2035, QAP_2037, QAP_2038, QAP_2039, QAP_2050, \
    QAP_3661, QAP_3848, QAP_4016, QAP_4094
from test_cases.fx.fx_mm_esp.QAP_2079 import QAP_2079
from test_cases.fx.fx_mm_esp.QAP_3798 import QAP_3798
from test_cases.fx.fx_mm_rfq import QAP_1563, QAP_1755

from test_cases.fx.fx_mm_rfq.EarlyRedemption import EarlyRedemption
from test_cases.fx.fx_mm_rfq.QAP_1542 import QAP_1542
from test_cases.fx.fx_mm_rfq.QAP_1547 import QAP_1547
from test_cases.fx.fx_mm_rfq.QAP_1562 import QAP_1562
from test_cases.fx.fx_mm_rfq.QAP_4085 import QAP_4085
from test_cases.fx.fx_mm_rfq.QAP_5345 import QAP_5345
from test_cases.fx.fx_mm_rfq.QAP_6220 import QAP_6220
from test_cases.fx.fx_mm_rfq.QAP_8006 import QAP_8006
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3772 import QAP_3772
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3811 import QAP_3811
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_3721 import QAP_3721
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_3741 import QAP_3741
from test_cases.fx.fx_taker_esp import QAP_3414, QAP_5635, QAP_5600, QAP_5598, QAP_5591, QAP_5589, QAP_5564, QAP_5537, \
    QAP_2373
from test_cases.fx.fx_taker_esp.QAP_6593 import QAP_6593
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
        # rm.print_active_rules()
        # QAP_568(report_id, session_id, configuration.data_set).execute()
        # Test_UI(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # DepositAndLoan.execute(report_id)

        QAP_MD(report_id, data_set=configuration.data_set).execute()
        # EarlyRedemption(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_5600.execute(report_id, session_id, configuration.data_set)
        # QAP_4094.execute(report_id)

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
