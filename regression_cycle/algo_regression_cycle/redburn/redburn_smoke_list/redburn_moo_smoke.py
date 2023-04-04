import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10488 import QAP_T10488
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10489 import QAP_T10489
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4463 import QAP_T4463
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4504 import QAP_T4504
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4505 import QAP_T4505
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4312 import QAP_T4312
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4467 import QAP_T4467
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4472 import QAP_T4472
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4474 import QAP_T4474
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4475 import QAP_T4475
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4525 import QAP_T4525
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T8869 import QAP_T8869
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T9405 import QAP_T9405
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Auction - MOO/MOC/Expiry (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        configuration = ComponentConfigurationAlgo("PreOpen_Auction")

        # region Basic
        QAP_T4475(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4474(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9405(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4472(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4525(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8869(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Would Price
        QAP_T4467(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region LimitPriceReference
        QAP_T4312(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Auction Scaling
        QAP_T10489(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10488(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4463(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4505(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4504(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion


    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()