import importlib
import logging
import os
from datetime import datetime
from pathlib import Path

from get_project_root import root_path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"Commissions Analysis" if version is None else f"Commissions | {version}",
                                 parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Commissions")
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = None  #set_session_id(fe_env.target_server_win)
    data_set = configuration.data_set
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    try:
        tests = os.listdir(root_path(ignore_cwd=True) + '\\test_cases\\eq\\Commissions')
        for test in tests:
            class_ = getattr(importlib.import_module(f"test_cases.eq.Commissions.{test[:-3]}"), test[:-3])
            class_(report_id, session_id, data_set, configuration.environment).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Commissions regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
