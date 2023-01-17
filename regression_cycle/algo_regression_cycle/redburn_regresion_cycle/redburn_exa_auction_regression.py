import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_MOE.QAP_T4307 import QAP_T4307
from test_cases.algo.Algo_Redburn.Algo_MOE.QAP_T4310 import QAP_T4310
from test_cases.algo.Algo_Redburn.Algo_MOE.QAP_T8625 import QAP_T8625
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Auction - MOO/MOC/Expiry (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfigurationAlgo("Expity_Auction")

        # region General
        QAP_T8625(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region WouldPrice
        QAP_T4307(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region LimitPriceOffset
        QAP_T4310(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()