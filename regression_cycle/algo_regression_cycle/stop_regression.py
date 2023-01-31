from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.environments.fix_environment import FixEnvironment
from test_framework.data_sets.environment_type import EnvironmentType
from test_cases.algo.Algo_Stop.QAP_T4277 import QAP_T4277
from test_cases.algo.Algo_Stop.QAP_T4278 import QAP_T4278
from test_cases.algo.Algo_Stop.QAP_T4280 import QAP_T4280
from test_cases.algo.Algo_Stop.QAP_T4272 import QAP_T4272
from test_cases.algo.Algo_Stop.QAP_T4273 import QAP_T4273

logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    logging.getLogger().setLevel(logging.WARN)


    try:
        report_id = bca.create_event(f"Algo_Stop" if version is None else f"Algo_Stop | {version}", parent_id)
        configuration = ComponentConfiguration("Stop")
        QAP_T4277(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4278(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4280(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4272(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4273(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
