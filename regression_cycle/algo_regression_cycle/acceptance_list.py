from stubs import Stubs, ROOT_DIR
from xml.etree import ElementTree
import time
from datetime import timedelta

from rule_management import RuleManager, Simulators
from test_framework.ssh_wrappers.ssh_client import SshClient
from win_gui_modules.utils import set_session_id
import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TWAP.QAP_T4886 import QAP_T4886
from test_cases.algo.Algo_TWAP.QAP_T4935 import QAP_T4935
from test_cases.algo.Algo_TWAP.QAP_T4988 import QAP_T4988
from test_cases.algo.Algo_TWAP.QAP_T4884 import QAP_T4884
from test_cases.algo.Algo_TWAP.QAP_T4887 import QAP_T4887
from test_cases.algo.Algo_PercentageVolume.QAP_T4879 import QAP_T4879
from test_cases.algo.Algo_PercentageVolume.QAP_T4890 import QAP_T4890
from test_cases.algo.Algo_PercentageVolume.QAP_T4911 import QAP_T4911
from test_cases.algo.Algo_PercentageVolume import QAP_T4950
# from test_cases.algo.Algo_PercentageVolume.QAP_T5083 import QAP_T5083 # not automated yet
# from test_cases.algo.Algo_PercentageVolume.QAP_T5085 import QAP_T5085 # not automated yet
from test_cases.algo.Algo_PercentageVolume import QAP_T5113
from test_cases.algo.Algo_Multilisted import QAP_T4093
from test_cases.algo.Algo_Multilisted.QAP_T4091 import QAP_T4091
from test_cases.algo.Algo_Multilisted.QAP_T4120 import QAP_T4120
from test_cases.algo.Algo_Multilisted.QAP_T4115 import QAP_T4115
from test_cases.algo.Algo_Multilisted.QAP_T4106 import QAP_T4106
from test_cases.algo.Algo_Multilisted.QAP_T4114 import QAP_T4114
from test_cases.algo.Algo_Multilisted.QAP_T4117 import QAP_T4117
# from test_cases.algo.Algo_Multilisted.QAP_T4148 import QAP_T4148 not automated yet
from test_cases.algo.Algo_Iceberg.QAP_T4925 import QAP_T4925
from test_cases.algo.Algo_Iceberg.QAP_T4918 import QAP_T4918
from test_cases.algo.Algo_Iceberg.QAP_T4919 import QAP_T4919
from test_cases.algo.algo_acceptance_list import QAP_T4949 # Cannot find reference 'wrapper' in 'imported module test_cases'
from test_cases.algo.algo_acceptance_list import QAP_T4948 # Cannot find reference 'wrapper' in 'imported module test_cases'
from test_cases.algo.Algo_Triggering.QAP_T5135 import QAP_T5135
from test_cases.algo.Algo_Triggering.QAP_T7842 import QAP_T7842
from test_cases.algo.Algo_Triggering.QAP_T9083 import QAP_T9083
from test_cases.algo.Algo_Triggering.QAP_T9081 import QAP_T9081
from test_cases.algo.Algo_LitDark.QAP_T7730 import QAP_T7730
from test_cases.algo.Algo_Block.QAP_T5108 import QAP_T5108
from test_cases.algo.Algo_TimeInForce.QAP_T4207 import QAP_T4207
from test_cases.algo.Algo_Stop.QAP_T4278 import QAP_T4278
from test_cases.algo.Algo_Peg.QAP_T8288 import QAP_T8288
from test_cases.algo.Algo_PairTrading.QAP_T8104 import QAP_T8104
from test_cases.algo.Algo_PairTrading.QAP_T7851 import QAP_T7851
from test_cases.algo.Algo_PairTrading.QAP_T8582 import QAP_T8582
from test_cases.algo.Algo_PairTrading.QAP_T4254 import QAP_T4254
# from test_cases.algo.Algo_PairTrading.QAP_T8106 import QAP_T8106
from test_cases.algo.Algo_PairTrading.QAP_T7850 import QAP_T7850
from test_cases.algo.Algo_PairTrading.QAP_T4249 import QAP_T4249

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()



def test_run(parent_id=None, version=None):
    # pc_name = get_pc_name()  # getting PC name
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    full_ver = root.find(".//version").text
    ver = full_ver[-3:]
    # report_id_main = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    report_id = bca.create_event('PDAT Acceptance v.' + ver + ' | ' + full_ver)
    logger.info(f"Root event was created (id = {report_id.id})")
    # session_id = set_session_id(pc_name) # grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated

    try:
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules_by_alias("fix-bs-310-columbia")
        start_time = time.monotonic()
        print(f'Algo_AcceptanceList StartTime is {datetime.utcnow()}')
        configuration = ComponentConfiguration("Acceptance_list")
        # TWAP
        QAP_T4886(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4935(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4988(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4884(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4887(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # POV
        QAP_T4879(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4890(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4911(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T5113.execute(report_id, session_id) # session ID error (line 44)
        # Iceberg
        QAP_T4925(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4918(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4919(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Multilisted
        QAP_T4120(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4106(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4117(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4115(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4091(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Triggering
        QAP_T5135(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7842(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9083(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9081(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Algo_LitDark
        QAP_T7730(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Algo_Block
        QAP_T5108(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Algo_TimeInForce
        QAP_T4207(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Algo_Stop
        QAP_T4278(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Algo_Peg
        QAP_T8288(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # Algo_PairTrading
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

        # usePoV = true
        QAP_T8104(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # usePoV = false

        # region precondition: Prepare SATS configuration
        ssh_client.get_and_update_file(config_file, {".//PairTrading/usePoV": mod_conf_value})
        ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        # endregion

        QAP_T7851(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8582(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4254(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7850(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4249(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # region postcondition: Return SATS configuration
        ssh_client.get_and_update_file(config_file, {".//PairTrading/usePoV": def_conf_value})
        ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        # endregion

        # TradLim and CumTradLim
        # QAP_T4949.execute(report_id, session_id) # session ID error (line 44)
        # QAP_T4948.execute(report_id, session_id) # session ID error (line 44)

        end_time = time.monotonic()
        print(f'Algo_AcceptanceList EndTime is {datetime.utcnow()}, duration is {timedelta(seconds=end_time-start_time)}')
    except Exception:
        logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
