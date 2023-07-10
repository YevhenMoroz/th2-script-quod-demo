import importlib
import logging
import os
from datetime import datetime

from get_project_root import root_path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def check_ssh(file):
    with open(file) as f:
        return 'ssh' in f.read()


def test_run(parent_id=None, version=None, skip_ssh=False, only_ssh=False):
    report_id = bca.create_event(f"Positions" if version is None else f"Positions Analysis | {version}",
                                 parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Gating_Rules")
    data_set = configuration.data_set
    try:
        tests = os.listdir(f'{root_path(ignore_cwd=True)}/test_cases/eq/Positions')
        for test in tests:
            class_ = getattr(importlib.import_module(f"test_cases.eq.Positions.{test[:-3]}"), test[:-3])
            print(str(class_))
            ssh_test = check_ssh(f'{root_path(ignore_cwd=True)}/test_cases/eq/Positions/{test}')
            print(class_)
            if (skip_ssh and not ssh_test) or (only_ssh and ssh_test) or (not skip_ssh and not only_ssh):
                class_(report_id, None, data_set, configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Positions regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")


if __name__ == '__main__':
    test_run(version="5.1.180.193", skip_ssh=True)
    Stubs.factory.close()
