import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Basket.QAP_3677 import QAP_3677
from test_cases.eq.Basket.QAP_3698 import QAP_3698
from test_cases.eq.Basket.QAP_3699 import QAP_3699
from test_cases.eq.Basket.QAP_3700 import QAP_3700
from test_cases.eq.Basket.QAP_3701 import QAP_3701
from test_cases.eq.Basket.QAP_3773 import QAP_3773
from test_cases.eq.Basket.QAP_3779 import QAP_3779
# from test_cases.eq.Basket.QAP_3874 import QAP_3874
from test_cases.eq.Basket.QAP_3874 import QAP_3874
from test_cases.eq.Basket.QAP_3877 import QAP_3877
from test_cases.eq.Basket.QAP_3882 import QAP_3882
from test_cases.eq.Basket.QAP_4007 import QAP_4007
from test_cases.eq.Basket.QAP_4011 import QAP_4011
from test_cases.eq.Basket.QAP_4012 import QAP_4012
from test_cases.eq.Basket.QAP_4013 import QAP_4013
from test_cases.eq.Basket.QAP_4021 import QAP_4021
from test_cases.eq.Basket.QAP_4022 import QAP_4022
from test_cases.eq.Basket.QAP_4023 import QAP_4023
from test_cases.eq.Basket.QAP_4046 import QAP_4046
from test_cases.eq.Basket.QAP_4220 import QAP_4220
from test_cases.eq.Basket.QAP_4359 import QAP_4359
# from test_cases.eq.Basket.QAP_4466 import QAP_4466
from test_cases.eq.Basket.QAP_4643 import QAP_4643
from test_cases.eq.Basket.QAP_4648 import QAP_4648
from test_cases.eq.Basket.QAP_4649 import QAP_4649
from test_cases.eq.Basket.QAP_4651 import QAP_4651
from test_cases.eq.Basket.QAP_4670 import QAP_4670
from test_cases.eq.Basket.QAP_5031 import QAP_5031
from test_cases.eq.Basket.QAP_5582 import QAP_5582
from test_cases.eq.Basket.QAP_5587 import QAP_5587
from test_cases.eq.Basket.QAP_6114 import QAP_6114
from test_cases.eq.Basket.QAP_6385 import QAP_6385
from test_cases.eq.Basket.QAP_6386 import QAP_6386
# from test_cases.eq.Basket.QAP_7033 import QAP_7033
# from test_cases.eq.Basket.QAP_7661 import QAP_7661
# from test_cases.eq.Basket.QAP_7662 import QAP_7662
from test_cases.eq.Basket.QAP_7033 import QAP_7033
from test_cases.eq.Basket.QAP_7661 import QAP_7661
from test_cases.eq.Basket.QAP_7662 import QAP_7662
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('BasketTrading', parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("BasketTrading")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("eq_regression_cycle/layouts")
    layout_name = "basket_templates_v172_layout.xml"
    try:
        base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_3677(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3698(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3699(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3700(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3701(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3773(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3779(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3874(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3877(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_3882(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4007(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4011(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4012(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4013(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4021(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4022(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4023(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4046(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4220(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4359(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_4466(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_4643(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4648(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4649(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4651(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_4670(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_5024(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_5031(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_5582(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_5587(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_6114(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_6385(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_6386(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_7033(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_7661(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_7662(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Basket regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        Stubs.win_act.unregister(session_id)
        # base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
