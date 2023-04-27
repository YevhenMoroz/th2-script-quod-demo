import time
from datetime import timedelta, datetime

from test_framework.ssh_wrappers.ssh_client import SshClient
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_PairTrading.QAP_T4233 import QAP_T4233
from test_cases.algo.Algo_PairTrading.QAP_T4236 import QAP_T4236
from test_cases.algo.Algo_PairTrading.QAP_T4239 import QAP_T4239
from test_cases.algo.Algo_PairTrading.QAP_T4247 import QAP_T4247
from test_cases.algo.Algo_PairTrading.QAP_T4249 import QAP_T4249
from test_cases.algo.Algo_PairTrading.QAP_T4253 import QAP_T4253
from test_cases.algo.Algo_PairTrading.QAP_T4254 import QAP_T4254
from test_cases.algo.Algo_PairTrading.QAP_T7850 import QAP_T7850
from test_cases.algo.Algo_PairTrading.QAP_T7851 import QAP_T7851
from test_cases.algo.Algo_PairTrading.QAP_T7928 import QAP_T7928
from test_cases.algo.Algo_PairTrading.QAP_T8037 import QAP_T8037
from test_cases.algo.Algo_PairTrading.QAP_T8064 import QAP_T8064
from test_cases.algo.Algo_PairTrading.QAP_T8104 import QAP_T8104
from test_cases.algo.Algo_PairTrading.QAP_T8105 import QAP_T8105
from test_cases.algo.Algo_PairTrading.QAP_T8108 import QAP_T8108
from test_cases.algo.Algo_PairTrading.QAP_T8114 import QAP_T8114
from test_cases.algo.Algo_PairTrading.QAP_T8115 import QAP_T8115
from test_cases.algo.Algo_PairTrading.QAP_T8119 import QAP_T8119
from test_cases.algo.Algo_PairTrading.QAP_T8120 import QAP_T8120
from test_cases.algo.Algo_PairTrading.QAP_T8128 import QAP_T8128
from test_cases.algo.Algo_PairTrading.QAP_T8298 import QAP_T8298
from test_cases.algo.Algo_PairTrading.QAP_T8573 import QAP_T8573
from test_cases.algo.Algo_PairTrading.QAP_T8574 import QAP_T8574
from test_cases.algo.Algo_PairTrading.QAP_T8575 import QAP_T8575
from test_cases.algo.Algo_PairTrading.QAP_T8577 import QAP_T8577
from test_cases.algo.Algo_PairTrading.QAP_T8578 import QAP_T8578
from test_cases.algo.Algo_PairTrading.QAP_T8579 import QAP_T8579
from test_cases.algo.Algo_PairTrading.QAP_T8580 import QAP_T8580
from test_cases.algo.Algo_PairTrading.QAP_T8581 import QAP_T8581
from test_cases.algo.Algo_PairTrading.QAP_T8582 import QAP_T8582
from test_cases.algo.Algo_PairTrading.QAP_T8584 import QAP_T8584
from test_cases.algo.Algo_PairTrading.QAP_T8619 import QAP_T8619
from test_cases.algo.Algo_PairTrading.QAP_T8710 import QAP_T8710
from test_cases.algo.Algo_PairTrading.QAP_T8711 import QAP_T8711
from test_cases.algo.Algo_PairTrading.QAP_T8818 import QAP_T8818
from test_cases.algo.Algo_PairTrading.QAP_T8819 import QAP_T8819
from test_cases.algo.Algo_PairTrading.QAP_T8921 import QAP_T8921
from test_cases.algo.Algo_PairTrading.QAP_T9171 import QAP_T9171
from test_cases.algo.Algo_PairTrading.QAP_T9172 import QAP_T9172
from test_cases.algo.Algo_PairTrading.QAP_T9173 import QAP_T9173
from test_cases.algo.Algo_PairTrading.QAP_T9174 import QAP_T9174
from test_cases.algo.Algo_PairTrading.QAP_T9179 import QAP_T9179

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id=None, version=None, mode=None):
    if mode == 'Regression':
        report_id = bca.create_event(f"Algo_PairTrading" if version is None else f"Algo_PairTrading | {version}", parent_id)
    else:
        report_id = bca.create_event(f"Algo_PairTrading" if version is None else f"Algo_PairTrading (verification) | {version}", parent_id)

    try:
        start_time = time.monotonic()
        print(f'Algo_PairTrading StartTime is {datetime.utcnow()}')
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)

        configuration = ComponentConfiguration("Pair_trading")

        # region SSH
        environment = configuration.environment
        config_file = "client_sats.xml"
        def_conf_value = "true"
        mod_conf_value = "false"
        ssh_client_env = environment.get_list_ssh_client_environment()[0]
        ssh_client = SshClient(ssh_client_env.host, ssh_client_env.port, ssh_client_env.user,
                               ssh_client_env.password, ssh_client_env.su_user,
                               ssh_client_env.su_password)
        # endregion

        # usePoV=true
        QAP_T8710(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4249(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4253(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4236(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4233(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7850(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8573(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8577(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8575(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8921(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8115(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8128(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8108(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T8105(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
        # QAP_T8104(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
        QAP_T7851(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T8119(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
        # QAP_T8120(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
        QAP_T8298(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8578(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8579(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8580(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8581(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8818(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9174(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9179(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9171(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T9173(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
        # QAP_T9172(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
        QAP_T7928(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8574(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        if __name__ == '__main__':
            # tests with config change
            # usePoV=false

            # region precondition: Prepare SATS configuration
            ssh_client.get_and_update_file(config_file, {".//PairTrading/usePoV": mod_conf_value})
            ssh_client.send_command("qrestart SATS")
            time.sleep(35)
            # endregion

            # QAP_T8064(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
            # QAP_T4247(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
            QAP_T8037(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T4254(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T4239(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            # QAP_T8584(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
            # QAP_T8582(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() test will fail because FIX ER Fill is not sent to the SS
            QAP_T8819(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T8711(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            # QAP_T8619(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() waiting for Vivien's answer

            # region postcondition: Return SATS configuration
            ssh_client.get_and_update_file(config_file, {".//PairTrading/usePoV": def_conf_value})
            ssh_client.send_command("qrestart SATS")
            time.sleep(35)
            # endregion
        
        end_time = time.monotonic()
        print(f'Algo_PairTrading EndTime is {datetime.utcnow()}, duration is {timedelta(seconds=end_time-start_time)}')
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
