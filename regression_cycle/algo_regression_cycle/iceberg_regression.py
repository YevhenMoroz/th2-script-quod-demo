from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.environments.fix_environment import FixEnvironment
from test_framework.data_sets.environment_type import EnvironmentType
from test_cases.algo.Algo_Iceberg.QAP_T4917 import QAP_T4917
from test_cases.algo.Algo_Iceberg.QAP_T4918 import QAP_T4918
from test_cases.algo.Algo_Iceberg.QAP_T4919 import QAP_T4919
from test_cases.algo.Algo_Iceberg.QAP_T4925 import QAP_T4925
from test_cases.algo.Algo_Iceberg.QAP_T4182 import QAP_T4182
from test_cases.algo.Algo_Iceberg.QAP_T4183 import QAP_T4183


logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    logging.getLogger().setLevel(logging.WARN)


    try:
        report_id = bca.create_event(f"Algo_Iceberg" if version is None else f"Algo_Iceberg | {version}", parent_id)
        configuration = ComponentConfiguration("Iceberg")
        QAP_T4917(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4918(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4919(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4925(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4182(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4183(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
