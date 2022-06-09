import logging
import time
from datetime import datetime
from pathlib import Path

from SendMD import QAP_MD
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_3082, QAP_2470
from test_cases.fx.fx_mm_esp import QAP_1599, QAP_2750, QAP_2823, QAP_3390, QAP_3394, QAP_3841, QAP_4094, \
    QAP_3848, QAP_3661, QAP_4016, QAP_6148, QAP_6151, QAP_1559, QAP_2012, QAP_2034
from test_cases.fx.fx_mm_esp.QAP_1418 import QAP_1418
from test_cases.fx.fx_mm_esp.QAP_1518 import QAP_1518
from test_cases.fx.fx_mm_esp.QAP_1536 import QAP_1536
from test_cases.fx.fx_mm_esp.QAP_1554 import QAP_1554
from test_cases.fx.fx_mm_esp.QAP_1589 import QAP_1589
from test_cases.fx.fx_mm_esp.QAP_1596 import QAP_1596
from test_cases.fx.fx_mm_esp.QAP_1643 import QAP_1643
from test_cases.fx.fx_mm_esp.QAP_2049 import QAP_2049
from test_cases.fx.fx_mm_esp.QAP_2078 import QAP_2078
from test_cases.fx.fx_mm_esp.QAP_2079 import QAP_2079
from test_cases.fx.fx_mm_esp.QAP_2080 import QAP_2080
from test_cases.fx.fx_mm_esp.QAP_2081 import QAP_2081
from test_cases.fx.fx_mm_esp.QAP_2082 import QAP_2082
from test_cases.fx.fx_mm_esp.QAP_2087 import QAP_2087
from test_cases.fx.fx_mm_esp.QAP_2797 import QAP_2797
from test_cases.fx.fx_mm_esp.QAP_2815 import QAP_2815
from test_cases.fx.fx_mm_esp.QAP_2825 import QAP_2825
from test_cases.fx.fx_mm_esp.QAP_2855 import QAP_2855
from test_cases.fx.fx_mm_esp.QAP_2957 import QAP_2957
from test_cases.fx.fx_mm_esp.QAP_3045 import QAP_3045
from test_cases.fx.fx_mm_esp.QAP_3555 import QAP_3555
from test_cases.fx.fx_mm_esp.QAP_3798 import QAP_3798
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389
from test_cases.fx.fx_mm_esp.QAP_6145 import QAP_6145
from test_cases.fx.fx_mm_esp.QAP_6149 import QAP_6149
from test_cases.fx.fx_mm_esp.QAP_6153 import QAP_6153
from test_cases.fx.fx_mm_esp.QAP_6155 import QAP_6155
from test_cases.fx.fx_mm_esp.QAP_6353 import QAP_6353
from test_cases.fx.fx_mm_esp.QAP_6691 import QAP_6691
from test_cases.fx.fx_mm_esp.QAP_6697 import QAP_6697
from test_cases.fx.fx_mm_esp.QAP_6931 import QAP_6931
from test_cases.fx.fx_mm_esp.QAP_6933 import QAP_6933
from test_cases.fx.fx_mm_esp.QAP_7073 import QAP_7073
from test_cases.fx.fx_mm_esp.QAP_7081 import QAP_7081
from test_cases.fx.fx_mm_esp.QAP_7279 import QAP_7279
from test_cases.fx.fx_mm_rfq.QAP_1542 import QAP_1542
from test_cases.fx.fx_mm_rfq.QAP_2382 import QAP_2382
from test_cases.fx.fx_mm_rfq.QAP_2472 import QAP_2472
from test_cases.fx.fx_mm_rfq.QAP_2670 import QAP_2670
from test_cases.fx.fx_mm_rfq.QAP_3704 import QAP_3704
from test_cases.fx.fx_mm_rfq.QAP_3610 import QAP_3610
from test_cases.fx.fx_mm_rfq.QAP_3834 import QAP_3834
from test_cases.fx.fx_mm_rfq.QAP_4085 import QAP_4085
from test_cases.fx.fx_mm_rfq.QAP_4510 import QAP_4510
from test_cases.fx.fx_mm_rfq.QAP_4777 import QAP_4777
from test_cases.fx.fx_mm_rfq.QAP_5345 import QAP_5345
from test_cases.fx.fx_mm_rfq.QAP_5353 import QAP_5353
from test_cases.fx.fx_mm_rfq.QAP_7125 import QAP_7125
from test_cases.fx.fx_mm_rfq.QAP_7129 import QAP_7129
from test_cases.fx.fx_mm_rfq.QAP_7130 import QAP_7130
from test_cases.fx.fx_mm_rfq.QAP_7162 import QAP_7162
from test_cases.fx.fx_mm_rfq.QAP_7556 import QAP_7556
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3761 import QAP_3761
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3811 import QAP_3811
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3850 import QAP_3850
from test_cases.fx.fx_mm_synthetic import QAP_2646
from test_cases.fx.fx_taker_esp import QAP_3140
from test_cases.fx.fx_taker_esp.QAP_3636 import QAP_3636
from test_cases.fx.fx_taker_esp.QAP_3801 import QAP_3801
from test_cases.fx.fx_taker_esp.QAP_3802 import QAP_3802
from test_cases.fx.fx_taker_esp.QAP_5553 import QAP_5553
from test_cases.fx.fx_taker_esp.QAP_6593 import QAP_6593
from test_cases.fx.fx_taker_rfq import QAP_2826, QAP_3002
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
    main_window = "Quod Financial - Quod site 314"
    try:
        # QAP_MD(report_id, data_set=configuration.data_set).execute()

        QAP_1554(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_3140.execute(report_id)
        # QAP_3140(report_id).execute()

        get_opened_fe(report_id, session_id, main_window)
        # QAP_1554.execute(report_id, session_id)
        # QAP_1536.execute(report_id, session_id, data_set=configuration.data_set)
        # QAP_6932(report_id, session_id).execute()

        # QAP_2103(report_id, session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_1536(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

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
