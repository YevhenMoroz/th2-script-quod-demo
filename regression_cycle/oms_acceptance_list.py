import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.ArchiveWindows.QAP_2791 import QAP_2791
from test_cases.eq.Basket.QAP_3677 import QAP_3677
from test_cases.eq.Basket.QAP_3701 import QAP_3701
from test_cases.eq.Basket.QAP_3874 import QAP_3874
from test_cases.eq.Care.QAP_1012 import QAP_1012
from test_cases.eq.Care.QAP_1717 import QAP_1717
from test_cases.eq.Commissions.QAP_2998 import QAP_2998
from test_cases.eq.Commissions.QAP_3350 import QAP_3350
from test_cases.eq.DMA.QAP_2002 import QAP_2002
from test_cases.eq.DMA.QAP_2008 import QAP_2008
from test_cases.eq.PostTrade.QAP_2614 import QAP_2614
from test_cases.eq.PostTrade.QAP_3304 import QAP_3304
from test_cases.eq.PostTrade.QAP_3332 import QAP_3332
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Acceptance list ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("AcceptanceList")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("eq_regression_cycle/layouts")
    layout_name = "all_columns_v172_layout.xml"

    try:
        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_1012(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_1101(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_1717(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_2002(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_2008(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_2173(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_2178(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_2201(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_2550(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_2614(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_2618(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_2659(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_2791(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_2801(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_3350(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_2998(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3304(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3332(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3677(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3701(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3874(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Acceptance list was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        # Stubs.win_act.unregister(session_id)
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
