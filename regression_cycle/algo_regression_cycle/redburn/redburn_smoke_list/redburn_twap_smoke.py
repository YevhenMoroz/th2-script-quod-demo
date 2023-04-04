import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T10471 import QAP_T10471
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4297 import QAP_T4297
from test_cases.algo.Algo_Redburn.Algo_TWAP_Auction.QAP_T10704 import QAP_T10704
from test_cases.algo.Algo_Redburn.Algo_TWAP_Auction.QAP_T4452 import QAP_T4452
from test_cases.algo.Algo_Redburn.Algo_TWAP_Auction.QAP_T8553 import QAP_T8553
from test_cases.algo.Algo_Redburn.Algo_TWAP_Auction.QAP_T9061 import QAP_T9061
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"TWAP (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region TWAP tests
        configuration = ComponentConfigurationAlgo("Twap")

        # region Basic
        QAP_T10471(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4297(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Sub-slice
        # endregion

        # region Would
        # endregion

        # region Navigator
        # dublicate QAP_T4297(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Auction
        QAP_T8553(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9061(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10704(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4452(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region MinParticipation
        # endregion

        # region MaxParticipation
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()