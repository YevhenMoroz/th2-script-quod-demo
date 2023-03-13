from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.environments.fix_environment import FixEnvironment
from test_framework.data_sets.environment_type import EnvironmentType
from test_cases.algo.Algo_Peg.QAP_T5110 import QAP_T5110
from test_cases.algo.Algo_Peg.QAP_T5111 import QAP_T5111
from test_cases.algo.Algo_Peg.QAP_T5112 import QAP_T5112
from test_cases.algo.Algo_Peg.QAP_T8288 import QAP_T8288

logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    logging.getLogger().setLevel(logging.WARN)


    try:
        report_id = bca.create_event(f"Algo_Peg" if version is None else f"Algo_Peg | {version}", parent_id)
        configuration = ComponentConfiguration("Peg")
        QAP_T5110(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5111(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5112(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8288(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
