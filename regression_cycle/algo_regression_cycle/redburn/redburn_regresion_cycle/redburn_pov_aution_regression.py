import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T11233 import QAP_T11233
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T11234 import QAP_T11234
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4176 import QAP_T4176
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4177 import QAP_T4177
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4386 import QAP_T4386
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4524 import QAP_T4524
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4526 import QAP_T4526
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4527 import QAP_T4527
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4533 import QAP_T4533
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4534 import QAP_T4534
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4535 import QAP_T4535
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4536 import QAP_T4536
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T8719 import QAP_T8719
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"POV - Auction (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        # configuration = ComponentConfiguration("Participation")
        configuration = ComponentConfigurationAlgo("Participation")
        QAP_T4386(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8719(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11233(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11234(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4534(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4526(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4524(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4527(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4536(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4535(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4533(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4177(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4176(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()