import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Bag.QAP_T6930 import QAP_T6930
from test_cases.eq.Bag.QAP_T6931 import QAP_T6931
from test_cases.eq.Bag.QAP_T6932 import QAP_T6932
from test_cases.eq.Bag.QAP_T7124 import QAP_T7124
from test_cases.eq.Bag.QAP_T7126 import QAP_T7126
from test_cases.eq.Bag.QAP_T7256 import QAP_T7256
from test_cases.eq.Bag.QAP_T7265 import QAP_T7265
from test_cases.eq.Bag.QAP_T7413 import QAP_T7413
from test_cases.eq.Bag.QAP_T7428 import QAP_T7428
from test_cases.eq.Bag.QAP_T7430 import QAP_T7430
from test_cases.eq.Bag.QAP_T7457 import QAP_T7457
from test_cases.eq.Bag.QAP_T7520 import QAP_T7520
from test_cases.eq.Bag.QAP_T7521 import QAP_T7521
from test_cases.eq.Bag.QAP_T7627 import QAP_T7627
from test_cases.eq.Bag.QAP_T7630 import QAP_T7630
from test_cases.eq.Bag.QAP_T7634 import QAP_T7634
from test_cases.eq.Bag.QAP_T7637 import QAP_T7637
from test_cases.eq.Bag.QAP_T7639 import QAP_T7639
from test_cases.eq.Bag.QAP_T7640 import QAP_T7640
from test_cases.eq.Bag.QAP_T7641 import QAP_T7641
from test_cases.eq.Bag.QAP_T7642 import QAP_T7642
from test_cases.eq.Bag.QAP_T7643 import QAP_T7643
from test_cases.eq.Bag.QAP_T7644 import QAP_T7644
from test_cases.eq.Bag.QAP_T7645 import QAP_T7645
from test_cases.eq.Bag.QAP_T7646 import QAP_T7646
from test_cases.eq.Bag.QAP_T7647 import QAP_T7647
from test_cases.eq.Bag.QAP_T7648 import QAP_T7648
from test_cases.eq.Bag.QAP_T7649 import QAP_T7649
from test_cases.eq.Bag.QAP_T7650 import QAP_T7650
from test_cases.eq.Bag.QAP_T7651 import QAP_T7651
from test_cases.eq.Bag.QAP_T7652 import QAP_T7652
from test_cases.eq.Bag.QAP_T7653 import QAP_T7653
from test_cases.eq.Bag.QAP_T7853 import QAP_T7853
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"Bag Analysis" if version is None else f"Bag Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Bag")
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    data_set = configuration.data_set
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle/layouts")
    layout_name = "all_columns_layout.xml"
    try:
        base_main_window.open_fe(test_id, fe_env=fe_env, is_open=False)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_T7653(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7652(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7651(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7650(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7649(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6930(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6931(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6932(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7124(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7126(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7256(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7265(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7413(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7428(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7430(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7457(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7520(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7521(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7627(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7630(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7634(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7637(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7639(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7640(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7641(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7642(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7643(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7644(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7645(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7646(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7647(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7648(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7853(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Bag regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()

if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
