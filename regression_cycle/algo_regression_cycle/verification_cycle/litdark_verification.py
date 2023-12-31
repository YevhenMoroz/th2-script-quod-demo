from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.environments.fix_environment import FixEnvironment
from test_framework.data_sets.environment_type import EnvironmentType
from test_cases.algo.Algo_LitDark.QAP_T7732 import QAP_T7732
from test_cases.algo.Algo_LitDark.QAP_T7728 import QAP_T7728
from test_cases.algo.Algo_LitDark.QAP_T7729 import QAP_T7729
from test_cases.algo.Algo_LitDark.QAP_T7730 import QAP_T7730


logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    logging.getLogger().setLevel(logging.WARN)


    try:
        report_id = bca.create_event(f"Algo_LitDark (verification) | 5.1.169.182" if version is None else f"Algo_LitDark (verification) | {version}", parent_id)
        configuration = ComponentConfiguration("Lit_dark")
        QAP_T7732(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7728(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7729(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7730(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
