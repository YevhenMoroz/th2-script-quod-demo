from xml.etree import ElementTree
import time
from datetime import timedelta, datetime

from test_framework.ssh_wrappers.ssh_client import SshClient
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
from test_cases.algo.Algo_Iceberg.QAP_T4191 import QAP_T4191
from test_cases.algo.Algo_Iceberg.QAP_T4947 import QAP_T4947
from test_cases.algo.Algo_Iceberg.QAP_T4520 import QAP_T4520
from test_cases.algo.Algo_Iceberg.QAP_T4544 import QAP_T4544
from test_cases.algo.Algo_Iceberg.QAP_T4545 import QAP_T4545
from test_cases.algo.Algo_Iceberg.QAP_T4546 import QAP_T4546
from test_cases.algo.Algo_Iceberg.QAP_T4937 import QAP_T4937
from test_cases.algo.Algo_Iceberg.QAP_T8712 import QAP_T8712


logging.basicConfig(format='%(asctime)s - %(message)s')
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None, mode=None):
    logging.getLogger().setLevel(logging.WARN)
    if mode == 'Regression':
        report_id = bca.create_event(f"Algo_Iceberg" if version is None else f"Algo_Iceberg | {version}", parent_id)
    else:
        report_id = bca.create_event(f"Algo_Iceberg" if version is None else f"Algo_Iceberg (verification) | {version}", parent_id)

    try:
        start_time = time.monotonic()
        print(f'Algo_Iceberg StartTime is {datetime.utcnow()}')

        configuration = ComponentConfiguration("Iceberg")
        QAP_T4917(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4918(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4919(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4925(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4191(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4183(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4182(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4520(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4544(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4545(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4546(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4937(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8712(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        if __name__ == '__main__':
            # tests with config change
            # usePoV=false
            # region SSH
            configuration = ComponentConfiguration("Iceberg")
            environment = configuration.environment
            config_file = "client_sats.xml"
            def_conf_value = "true"
            mod_conf_value = "false"
            ssh_client_env = environment.get_list_ssh_client_environment()[0]
            ssh_client = SshClient(ssh_client_env.host, ssh_client_env.port, ssh_client_env.user,
                                   ssh_client_env.password, ssh_client_env.su_user,
                                   ssh_client_env.su_password)
            # endregion

            # region precondition: Prepare SATS configuration
            ssh_client.get_and_update_file(config_file, {".//manualResume": mod_conf_value})
            ssh_client.send_command("qrestart SATS")
            time.sleep(35)
            # endregion

            QAP_T4947(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

            # region postcondition: Return SATS configuration
            ssh_client.get_and_update_file(config_file, {".//PairTrading/usePoV": def_conf_value})
            ssh_client.send_command("qrestart SATS")
            time.sleep(35)
            # endregion

        end_time = time.monotonic()
        print(f'Algo_Iceberg EndTime is {datetime.utcnow()}, duration is {timedelta(seconds=end_time-start_time)}')

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
