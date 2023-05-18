import logging
import time
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11325 import QAP_T11325
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4592 import QAP_T4592
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4593 import QAP_T4593
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4594 import QAP_T4594
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4595 import QAP_T4595
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4596 import QAP_T4596
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4597 import QAP_T4597
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4602 import QAP_T4602
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4617 import QAP_T4617
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4618 import QAP_T4618
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4619 import QAP_T4619
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4620 import QAP_T4620
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4621 import QAP_T4621
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4622 import QAP_T4622
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4623 import QAP_T4623
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4624 import QAP_T4624
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4625 import QAP_T4625
from test_cases.algo.Algo_VWAP.QAP_T4338 import QAP_T4338
from test_cases.algo.Algo_VWAP.QAP_T4341 import QAP_T4341
from test_cases.algo.Algo_VWAP.QAP_T4344 import QAP_T4344
from test_cases.algo.Algo_VWAP.QAP_T4598 import QAP_T4598
from test_cases.algo.Algo_VWAP.QAP_T4601 import QAP_T4601
from test_cases.algo.Algo_VWAP.QAP_T4607 import QAP_T4607
from test_cases.algo.Algo_VWAP.QAP_T4608 import QAP_T4608
from test_cases.algo.Algo_VWAP.QAP_T4609 import QAP_T4609
from test_cases.algo.Algo_VWAP.QAP_T4610 import QAP_T4610
from test_cases.algo.Algo_VWAP.QAP_T4611 import QAP_T4611
from test_cases.algo.Algo_VWAP.QAP_T4612 import QAP_T4612
from test_cases.algo.Algo_VWAP.QAP_T4613 import QAP_T4613
from test_cases.algo.Algo_VWAP.QAP_T4615 import QAP_T4615
from test_cases.algo.Algo_VWAP.QAP_T4616 import QAP_T4616
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"VWAP - Additional Features (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfigurationAlgo("Vwap")
        # region SSH
        config_file = "client_sats.xml"
        xpath = ".//bpsOffsets"
        new_config_value = "false"
        ssh_client_env = configuration.environment.get_list_ssh_client_environment()[0]
        ssh_client = SshClient(ssh_client_env.host, ssh_client_env.port, ssh_client_env.user, ssh_client_env.password, ssh_client_env.su_user, ssh_client_env.su_password)
        default_config_value = ssh_client.get_and_update_file(config_file, {xpath: new_config_value})
        # endregion

        # region precondition: Prepare SATS configuration
        ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        # endregion

        QAP_T4592(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4593(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4594(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4595(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4596(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4597(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4602(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4617(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4618(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4619(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4620(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4621(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4622(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4623(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4624(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4625(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4338(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4341(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4598(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4344(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4601(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4607(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4608(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4609(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4610(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4611(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4612(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4613(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4615(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4616(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # region config reset
        default_config_value = ssh_client.get_and_update_file(config_file, {xpath: new_config_value})
        ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        ssh_client.close()
        # endregion
        # endregion

        QAP_T11325(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T4331.execute(report_id)
        # QAP_T4334.execute(report_id)

        # region Needs Refactoring
        # QAP_T4563.execute(report_id)
        # QAP_T4583.execute(report_id)
        # QAP_T4584.execute(report_id)
        # QAP_T4601.execute(report_id)
        # QAP_T4611.execute(report_id)
        # QAP_T4612.execute(report_id)
        # QAP_T4613.execute(report_id)
        # QAP_T4615.execute(report_id)
        # QAP_T4616.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()