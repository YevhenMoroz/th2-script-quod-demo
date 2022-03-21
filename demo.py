import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_3661, QAP_4016, QAP_6148
from test_cases.fx.fx_mm_esp.QAP_1554 import QAP_1554
from test_cases.fx.fx_mm_esp.QAP_6145 import QAP_6145
from test_cases.fx.fx_mm_esp.QAP_6149 import QAP_6149
from test_cases.fx.fx_mm_rfq import QAP_3494
from test_cases.fx.fx_mm_rfq.QAP_5992 import QAP_5992
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3761 import QAP_3761
from test_cases.fx.fx_taker_esp import QAP_5600, QAP_5537, QAP_5564, QAP_5589, QAP_5591, QAP_5598, QAP_5635
from test_cases.fx.fx_taker_esp.QAP_3636 import QAP_3636
from test_cases.fx.fx_taker_esp.QAP_3801 import QAP_3801
from test_cases.fx.fx_taker_esp.QAP_3802 import QAP_3802
from test_cases.fx.fx_taker_rfq import QAP_683
from test_cases.fx.fx_taker_rfq.QAP_568 import QAP_568
from test_cases.fx.send_md import QAP_MD
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.for_testing import Testing
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
    session_id = set_session_id(target_server_win="quod_11q")
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
        #     get_opened_fe(report_id, session_id)

        # rm = RuleManager()
        # rm.remove_rule_by_id(9)
        # rm.add_fx_md_to("fix-fh-309-kratos")
        # rm.print_active_rules()

        # QAP_683(report_id, session_id, configuration.data_set).execute()
        # Testing(report_id, session_id, configuration.data_set).execute()

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # QAP_3494.execute(report_id)
        QAP_6149(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

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
