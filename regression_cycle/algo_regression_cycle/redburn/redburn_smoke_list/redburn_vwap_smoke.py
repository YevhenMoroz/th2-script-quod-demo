import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T10943 import QAP_T10943
from test_cases.algo.Algo_Redburn.Algo_VWAP_Auction.QAP_T8554 import QAP_T8554
from test_cases.algo.Algo_Redburn.Algo_VWAP_Auction.QAP_T9062 import QAP_T9062
from test_cases.algo.Algo_VWAP.QAP_T4616 import QAP_T4616
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"VWAP (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfigurationAlgo("Vwap")

        # region Basic
        QAP_T10943(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Sub-slice
        # endregion

        # region Would
        QAP_T4616(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Navigator
        # endregion

        # region Auction
        QAP_T8554(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9062(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
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