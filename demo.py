import logging
import time
from getpass import getuser as get_pc_name
from datetime import datetime

from Test_UI import Test_UI
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from send_rqf import Send_RFQ
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_T2697, QAP_T2682, QAP_T2681, QAP_T2713, QAP_T2679
from test_cases.fx.fx_mm_esp.QAP_T2432 import QAP_T2432
from test_cases.fx.fx_mm_esp.QAP_T2605 import QAP_T2605
from test_cases.fx.fx_mm_esp.QAP_T2719 import QAP_T2719
from test_cases.fx.fx_mm_esp.QAP_T2896 import QAP_T2896
from test_cases.fx.fx_mm_positions.QAP_T8544 import QAP_T8544
from test_cases.fx.fx_mm_rfq.QAP_T2376 import QAP_T2376
from test_cases.fx.fx_mm_rfq.QAP_T2385 import QAP_T2385
from test_cases.fx.fx_mm_rfq.QAP_T2417 import QAP_T2417
from test_cases.fx.fx_mm_rfq.QAP_T2418 import QAP_T2418
from test_cases.fx.fx_mm_rfq.QAP_T2419 import QAP_T2419
from test_cases.fx.fx_mm_rfq.QAP_T2443 import QAP_T2443
from test_cases.fx.fx_mm_rfq.QAP_T2454 import QAP_T2454
from test_cases.fx.fx_mm_rfq.QAP_T2466 import QAP_T2466
from test_cases.fx.fx_mm_rfq.QAP_T2480 import QAP_T2480
from test_cases.fx.fx_mm_rfq.QAP_T2481 import QAP_T2481
from test_cases.fx.fx_mm_rfq.QAP_T2482 import QAP_T2482
from test_cases.fx.fx_mm_rfq.QAP_T2500 import QAP_T2500
from test_cases.fx.fx_mm_rfq.QAP_T2519 import QAP_T2519
from test_cases.fx.fx_mm_rfq.QAP_T2527 import QAP_T2527
from test_cases.fx.fx_mm_rfq.QAP_T2528 import QAP_T2528
from test_cases.fx.fx_mm_rfq.QAP_T2546 import QAP_T2546
from test_cases.fx.fx_mm_rfq.QAP_T2611 import QAP_T2611
from test_cases.fx.fx_mm_rfq.QAP_T2691 import QAP_T2691
from test_cases.fx.fx_mm_rfq.QAP_T2694 import QAP_T2694
from test_cases.fx.fx_mm_rfq.QAP_T2716 import QAP_T2716
from test_cases.fx.fx_mm_rfq.QAP_T2818 import QAP_T2818
from test_cases.fx.fx_mm_rfq.QAP_T2828 import QAP_T2828
from test_cases.fx.fx_mm_rfq.QAP_T2834 import QAP_T2834
from test_cases.fx.fx_mm_rfq.QAP_T2842 import QAP_T2842
from test_cases.fx.fx_mm_rfq.QAP_T2844 import QAP_T2844
from test_cases.fx.fx_mm_rfq.QAP_T2845 import QAP_T2845
from test_cases.fx.fx_mm_rfq.QAP_T2861 import QAP_T2861
from test_cases.fx.fx_mm_rfq.QAP_T2878 import QAP_T2878
from test_cases.fx.fx_mm_rfq.QAP_T2879 import QAP_T2879
from test_cases.fx.fx_mm_rfq.QAP_T2880 import QAP_T2880
from test_cases.fx.fx_mm_rfq.QAP_T2886 import QAP_T2886
from test_cases.fx.fx_mm_rfq.QAP_T2887 import QAP_T2887
from test_cases.fx.fx_mm_rfq.QAP_T2939 import QAP_T2939
from test_cases.fx.fx_mm_rfq.QAP_T2940 import QAP_T2940
from test_cases.fx.fx_mm_rfq.QAP_T5995 import QAP_T5995
from test_cases.fx.fx_mm_rfq.QAP_T7967 import QAP_T7967
from test_cases.fx.fx_mm_rfq.QAP_T8011 import QAP_T8011
from test_cases.fx.fx_mm_rfq.QAP_T8020 import QAP_T8020
from test_cases.fx.fx_mm_rfq.QAP_T8168 import QAP_T8168
from test_cases.fx.fx_mm_rfq.QAP_T8378 import QAP_T8378
from test_cases.fx.fx_mm_rfq.QAP_T8409 import QAP_T8409
from test_cases.fx.fx_mm_rfq.QAP_T8636 import QAP_T8636
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2444 import QAP_T2444

from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2448 import QAP_T2448
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2475 import QAP_T2475
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2537 import QAP_T2537
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2558 import QAP_T2558
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2572 import QAP_T2572
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2573 import QAP_T2573
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2575 import QAP_T2575
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2579 import QAP_T2579
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2603 import QAP_T2603
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T8015 import QAP_T8015
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2442 import QAP_T2442
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2549 import QAP_T2549
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2550 import QAP_T2550
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2592 import QAP_T2592
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2597 import QAP_T2597
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2581 import QAP_T2581
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2593 import QAP_T2593
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2595 import QAP_T2595
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2598 import QAP_T2598
from test_cases.fx.fx_price_cleansing.QAP_T2637 import QAP_T2637
from test_cases.fx.fx_taker_esp import QAP_T2487, QAP_T2488
from test_cases.fx.fx_taker_esp.QAP_T8666 import QAP_T8666

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
    session_id = set_session_id(target_server_win="ostronov")

    window_name = "Quod Financial - Quod site 309"
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    # endregion
    Stubs.frontend_is_open = True

    try:

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        QAP_T2679.execute(report_id, session_id)
        # Send_RFQ(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Test_UI(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T2697.execute(report_id, session_id)
        # QAP_T2719(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()


        # rm = RuleManager()
        # # rm.remove_rule_by_id(5)
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