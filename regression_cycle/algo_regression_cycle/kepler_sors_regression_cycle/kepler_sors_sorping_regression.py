import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2407 import QAP_2407
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2408 import QAP_2408
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2409 import QAP_2409
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2410 import QAP_2410
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2411 import QAP_2411
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2503 import QAP_2503
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2665 import QAP_2665
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2666 import QAP_2666
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2667 import QAP_2667

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None):
    # Generation id and time for test run
    report_id = bca.create_event('SORPING', parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region SORPING
        configuration = ComponentConfiguration("sorping")
        QAP_2407(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2408(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2409(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2410(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2411(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2503(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2665(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2666(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2667(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()