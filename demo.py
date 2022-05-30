import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime

import rule_management
from MyFiles.SendMD import SendMD
from MyFiles.SendMD_QAP_6337 import SendMD_QAP_6337
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_2326, QAP_3147, QAP_3146, QAP_2470, QAP_3017, QAP_3039, QAP_3067, \
    QAP_3233, QAP_3354, QAP_3819, QAP_4122
from test_cases.fx.fx_mm_esp import QAP_2966, QAP_6148
from test_cases.fx.fx_mm_esp.QAP_3537 import QAP_3537
from test_cases.fx.fx_mm_esp.QAP_6149 import QAP_6149
from test_cases.fx.fx_mm_esp.QAP_6153 import QAP_6153
from test_cases.fx.fx_mm_esp.QAP_6691 import QAP_6691
from test_cases.fx.fx_mm_esp.QAP_6697 import QAP_6697
from test_cases.fx.fx_mm_esp.QAP_7279 import QAP_7279
from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from test_cases.fx.fx_mm_rfq import QAP_3003, QAP_3250, QAP_1552, QAP_1746, QAP_4509, QAP_4510, QAP_2296, QAP_2091, \
    QAP_2382, QAP_5814
from test_cases.fx.fx_mm_rfq.QAP_6192 import QAP_6192
from test_cases.fx.fx_mm_rfq.QAP_7129 import QAP_7129
from test_cases.fx.fx_mm_rfq.QAP_7130 import QAP_7130
from test_cases.fx.fx_mm_rfq.interpolation import QAP_3766, QAP_3734, QAP_3805
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3761 import QAP_3761
from test_cases.fx.fx_taker_esp import QAP_3141, QAP_3140, QAP_3418, QAP_3414, QAP_3415, QAP_5598, QAP_5635, QAP_5591, \
    QAP_5600, QAP_5564, QAP_5589, QAP_5537
from test_cases.fx.fx_taker_rfq import QAP_612
from test_cases.fx.fx_taker_rfq.QAP_6 import QAP_6
from test_cases.fx.fx_wrapper.common_tools import stop_fxfh, start_fxfh
from test_cases.fx.fx_mm_rfq import QAP_4505, QAP_5848
from test_cases.fx.fx_mm_rfq.QAP_7168 import QAP_7168
from test_cases.fx.fx_mm_rfq.QAP_7287 import QAP_7287
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ') #+ datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset

    # initializing FE session
    session_id = set_session_id(target_server_win="ashcherb")
    window_name = "Quod Financial - Quod site 314"
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    data_set = FxDataSet()
    # endregion
    Stubs.frontend_is_open = True

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id, window_name)

        # QAP_2098(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_2343(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_4149(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_3142(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_3761(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_3147.execute(report_id, session_id)
        # QAP_3146.execute(report_id, session_id)
        # QAP_3140.execute(report_id)
        # QAP_3805.execute(report_id)
        # QAP_2382.execute(report_id)
        # QAP_6691(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6697(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7279(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_5369.execute(report_id, session_id, data_set)
        # QAP_5589.execute(report_id, session_id)
        # QAP_5591.execute(report_id, session_id)
        # QAP_5537.execute(report_id, session_id, data_set)
        # QAP_3141.execute(report_id)
        # QAP_3140.execute(report_id)
        # MyTest(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # send_rfq.execute(report_id)
        SendMD(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_7129(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # SendMD_QAP_6337(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # rule_management.RuleManager.print_active_rules()
        # QAP_4509.execute(report_id)
        # QAP_4510.execute(report_id)
        # QAP_2966.execute(report_id)
        # stop_fxfh()
        # QAP_3414.execute(report_id)
        # QAP_3415.execute(report_id)
        # QAP_3418.execute(report_id)
        # start_fxfh()
        # prepare_position()
        # rm = RuleManager()
        # rm.print_active_rules()

        # Testing(report_id, session_id, configuration.data_set).execute()

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set).execute()


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
