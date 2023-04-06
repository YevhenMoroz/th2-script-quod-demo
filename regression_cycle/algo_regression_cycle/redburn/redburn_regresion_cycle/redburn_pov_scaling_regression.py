import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4287 import QAP_T4287
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4288 import QAP_T4288
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4289 import QAP_T4289
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4478 import QAP_T4478
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4473 import QAP_T4473
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4470 import QAP_T4470
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4464 import QAP_T4464
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"POV - Scaling (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        configuration = ComponentConfigurationAlgo("POV_Scaling")

        # region Reject
        QAP_T4287(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4288(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4289(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Basic POV + Scaling behavior
        QAP_T4478(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4470(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4464(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region change in sats.xml config <Participate><maxAggressiveAttempts> = 0
        QAP_T4473(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()