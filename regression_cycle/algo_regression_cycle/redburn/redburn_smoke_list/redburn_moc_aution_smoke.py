import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10976 import QAP_T10976
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10977 import QAP_T10977
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10978 import QAP_T10978
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4364 import QAP_T4364
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4201 import QAP_T4201
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4311 import QAP_T4311
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9332 import QAP_T9332
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
        configuration = ComponentConfigurationAlgo("PreClose_Auction")

        # region Basic
        QAP_T4364(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9332(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Would Price
        # endregion

        # region LimitPriceReference
        QAP_T4201(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4311(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Auction Scaling
        configuration = ComponentConfigurationAlgo("Scaling")
        QAP_T10977(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10976(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10978(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4364(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()