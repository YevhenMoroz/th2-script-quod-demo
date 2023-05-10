import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4225 import QAP_T4225
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8728 import QAP_T8728
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8791 import QAP_T8791
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8792 import QAP_T8792
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8793 import QAP_T8793
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8795 import QAP_T8795
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8796 import QAP_T8796
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T9056 import QAP_T9056
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8749 import QAP_T8749
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8751 import QAP_T8751
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8752 import QAP_T8752
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8845 import QAP_T8845
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4350 import QAP_T4350
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4351 import QAP_T4351
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"POV (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfigurationAlgo("Participation")
        # QAP_T8728(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4225(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4350(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4351(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8791(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8792(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8793(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8795(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8796(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9056(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8845(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8751(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8752(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # region config change sats -> maxChildren = 3
        QAP_T8749(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        pass

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()