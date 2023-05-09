from xml.etree import ElementTree

from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.environments.fix_environment import FixEnvironment
from test_framework.data_sets.environment_type import EnvironmentType
from test_cases.algo.Algo_Triggering.QAP_T5135 import QAP_T5135
from test_cases.algo.Algo_Triggering.QAP_T8817 import QAP_T8817
from test_cases.algo.Algo_Triggering.QAP_T9030 import QAP_T9030
from test_cases.algo.Algo_Triggering.QAP_T9031 import QAP_T9031
from test_cases.algo.Algo_Triggering.QAP_T9073 import QAP_T9073
from test_cases.algo.Algo_Triggering.QAP_T9080 import QAP_T9080
from test_cases.algo.Algo_Triggering.QAP_T9081 import QAP_T9081
from test_cases.algo.Algo_Triggering.QAP_T9083 import QAP_T9083
from test_cases.algo.Algo_Triggering.QAP_T9143 import QAP_T9143
from test_cases.algo.Algo_Triggering.QAP_T9161 import QAP_T9161
from test_cases.algo.Algo_Triggering.QAP_T7842 import QAP_T7842

logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    logging.getLogger().setLevel(logging.WARN)


    try:
        report_id = bca.create_event(f"Algo_Triggering (verification)" if version is None else f"Algo_Triggering (verification) | {version}", parent_id)
        configuration = ComponentConfiguration("Triggering")
        QAP_T8817(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5135(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9030(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9031(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9073(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9080(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9081(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9083(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9143(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9161(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7842(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
