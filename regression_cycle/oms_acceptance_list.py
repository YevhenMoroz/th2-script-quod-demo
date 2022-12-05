import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.ArchiveWindows.QAP_T8159 import QAP_T8159
from test_cases.eq.ArchiveWindows.QAP_T7541 import QAP_T7541
from test_cases.eq.Bag.QAP_T7634 import QAP_T7634
from test_cases.eq.Basket.QAP_T7453 import QAP_T7453
from test_cases.eq.Basket.QAP_T7447 import QAP_T7447
from test_cases.eq.Basket.QAP_T7433 import QAP_T7433
from test_cases.eq.Care.QAP_T7689 import QAP_T7689
from test_cases.eq.Care.QAP_T7626 import QAP_T7626
from test_cases.eq.Commissions.QAP_T7534 import QAP_T7534
from test_cases.eq.Commissions.QAP_T7497 import QAP_T7497
from test_cases.eq.DMA.QAP_T7549 import QAP_T7549
from test_cases.eq.DMA.QAP_T7615 import QAP_T7615
from test_cases.eq.DMA.QAP_T7610 import QAP_T7610
from test_cases.eq.Gateway.QAP_T7507 import QAP_T7507
from test_cases.eq.GatingRules.QAP_T4928 import QAP_T4928
from test_cases.eq.GatingRules.QAP_T4929 import QAP_T4929
from test_cases.eq.GatingRules.QAP_T4930 import QAP_T4930
from test_cases.eq.GatingRules.QAP_T4931 import QAP_T4931
from test_cases.eq.Position.QAP_T7598 import QAP_T7598
from test_cases.eq.PositionsMgt.QAP_T7606 import QAP_T7606
from test_cases.eq.PostTrade.QAP_T7552 import QAP_T7552
from test_cases.eq.PostTrade.QAP_T7517 import QAP_T7517
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"PEQ Acceptance v.180" if version is None else f"PEQ Acceptance v.180 | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("AcceptanceList")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("layouts")
    layout_name = "all_columns_layout.xml"

    try:
        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        # base_main_window.import_layout(layout_path, layout_name)
        QAP_T4930(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4931(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4928(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4929(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7549(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7689(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7626(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7615(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7610(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7608(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7606(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7598(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7561(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7552(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7550(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7549(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7541(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T8159(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7497(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7534(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7517(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7507(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7453(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7433(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7598(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7606(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7447(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7634(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Acceptance list was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        Stubs.win_act.unregister(session_id)
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
