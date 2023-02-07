import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10278 import QAP_T10278
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10273 import QAP_T10273
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4460 import QAP_T4460
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Auction - Scaling (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:

        configuration = ComponentConfigurationAlgo("Scaling")
        QAP_T10278(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10273(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4460(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        pass


    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()