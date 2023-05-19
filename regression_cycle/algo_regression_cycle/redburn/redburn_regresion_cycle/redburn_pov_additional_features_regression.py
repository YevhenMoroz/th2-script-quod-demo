import logging
import time
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_PercentageVolume.QAP_T4342 import QAP_T4342
from test_cases.algo.Algo_PercentageVolume.QAP_T4345 import QAP_T4345
from test_cases.algo.Algo_PercentageVolume.QAP_T4599 import QAP_T4599
from test_cases.algo.Algo_PercentageVolume.QAP_T4603 import QAP_T4603
from test_cases.algo.Algo_PercentageVolume.QAP_T4632 import QAP_T4632
from test_cases.algo.Algo_PercentageVolume.QAP_T4633 import QAP_T4633
from test_cases.algo.Algo_PercentageVolume.QAP_T4634 import QAP_T4634
from test_cases.algo.Algo_PercentageVolume.QAP_T4635 import QAP_T4635
from test_cases.algo.Algo_PercentageVolume.QAP_T4648 import QAP_T4648
from test_cases.algo.Algo_PercentageVolume.QAP_T4659 import QAP_T4659
from test_cases.algo.Algo_PercentageVolume.QAP_T4660 import QAP_T4660
from test_cases.algo.Algo_PercentageVolume.QAP_T4661 import QAP_T4661
from test_cases.algo.Algo_PercentageVolume.QAP_T4662 import QAP_T4662
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T10939 import QAP_T10939
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T11326 import QAP_T11326
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4604 import QAP_T4604
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4636 import QAP_T4636
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4637 import QAP_T4637
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4638 import QAP_T4638
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4639 import QAP_T4639
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4640 import QAP_T4640
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4641 import QAP_T4641
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4642 import QAP_T4642
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4643 import QAP_T4643
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4644 import QAP_T4644
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4645 import QAP_T4645
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4646 import QAP_T4646
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4649 import QAP_T4649
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4650 import QAP_T4650
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4651 import QAP_T4651
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4706 import QAP_T4706
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8716 import QAP_T8716
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8718 import QAP_T8718
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8728 import QAP_T8728
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo
from test_framework.ssh_wrappers.ssh_client import SshClient


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"POV - Additional Features (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        # configuration = ComponentConfiguration("Participation")
        configuration = ComponentConfigurationAlgo("Participation")

        QAP_T8716(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8718(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8728(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10939(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11326(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

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

        QAP_T4604(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4636(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4637(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4638(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4639(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4640(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4641(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4642(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4643(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4644(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4645(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4646(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4649(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4650(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4651(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4706(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4342(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4345(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4599(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4603(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4632(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4633(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4634(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4635(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4648(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4659(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4660(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4661(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4662(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # region config reset
        ssh_client.get_and_update_file(config_file, {xpath: default_config_value})
        ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        ssh_client.close()
        # endregion
        # endregion


        # QAP_T4333.execute(report_id)
        # QAP_T4330.execute(report_id)

        # region Needs Refactoring
        # QAP_T4569.execute(report_id)
        # QAP_T4573.execute(report_id)
        # QAP_T4574.execute(report_id)
        # QAP_T4580.execute(report_id)
        # QAP_T4599.execute(report_id)
        # QAP_T4604.execute(report_id)
        # QAP_T4629.execute(report_id)
        # QAP_T4631.execute(report_id)
        # QAP_T4648.execute(report_id)
        # QAP_T4659.execute(report_id)
        # QAP_T4660.execute(report_id)
        # QAP_T4556.execute(report_id)
        # QAP_T4661.execute(report_id)
        # QAP_T4565.execute(report_id)
        # QAP_T4662.execute(report_id)
        # QAP_T4566.execute(report_id)
        # QAP_T4567.execute(report_id)
        # QAP_T4568.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()