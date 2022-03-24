import logging
import time
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_6151, QAP_2957
from test_cases.fx.fx_mm_esp.QAP_1418 import QAP_1418
from test_cases.fx.fx_mm_esp.QAP_1589 import QAP_1589
from test_cases.fx.fx_mm_esp.QAP_1643 import QAP_1643
from test_cases.fx.fx_mm_esp.QAP_2049 import QAP_2049
from test_cases.fx.fx_mm_esp.QAP_2077 import QAP_2077
from test_cases.fx.fx_mm_esp.QAP_2080 import QAP_2080
from test_cases.fx.fx_mm_esp.QAP_2087 import QAP_2087
from test_cases.fx.fx_mm_esp.QAP_2815 import QAP_2815
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389
from test_cases.fx.fx_mm_esp.QAP_6149 import QAP_6149
from test_cases.fx.fx_mm_esp.QAP_6155 import QAP_6155
from test_cases.fx.fx_mm_esp.QAP_6353 import QAP_6353
from test_cases.fx.fx_mm_esp.QAP_6697 import QAP_6697
from test_cases.fx.fx_mm_esp.QAP_6931 import QAP_6931
from test_cases.fx.fx_mm_esp.QAP_6932 import QAP_6932
from test_cases.fx.fx_mm_esp.QAP_6933 import QAP_6933
from test_cases.fx.fx_mm_esp.QAP_7073 import QAP_7073
from test_cases.fx.fx_mm_esp.QAP_7081 import QAP_7081
from test_cases.fx.fx_mm_rfq import for_test_77679
from test_cases.fx.fx_mm_rfq.QAP_2472 import QAP_2472
from test_cases.fx.fx_mm_rfq.QAP_2670 import QAP_2670
from test_cases.fx.fx_mm_rfq.QAP_3704 import QAP_3704
from test_cases.fx.fx_taker_esp import QAP_5600
from test_cases.fx.fx_taker_esp.QAP_3636 import QAP_3636
from test_cases.fx.fx_taker_esp.QAP_3801 import QAP_3801
from test_cases.fx.fx_taker_esp.QAP_3802 import QAP_3802
from test_cases.fx.fx_taker_esp.QAP_5553 import QAP_5553
from test_cases.fx.fx_taker_esp.QAP_6593 import QAP_6593
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
# from test_framework.for_testing import Testing
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(f'amedents ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset

    # initializing FE session
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id(target_server_win="amedents")
    # region environment and fe values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = datetime.now()
    print(f"Start time: {start_time}")
    # endregion
    Stubs.frontend_is_open = True

    try:
        # get_opened_fe(report_id, session_id)

        # QAP_7081(report_id, session_id, data_set=configuration.data_set).execute()
        QAP_7073(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_3494.execute(report_id)

        # rm = RuleManager()
        # rm.remove_rule_by_id(9)
        # rm.add_fx_md_to("fix-fh-309-kratos")
        # rm.print_active_rules()

        print(f"Duration is {datetime.now() - start_time}")

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
