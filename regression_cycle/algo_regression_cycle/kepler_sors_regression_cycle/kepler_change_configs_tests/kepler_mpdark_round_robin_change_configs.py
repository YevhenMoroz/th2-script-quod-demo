import logging
import time

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10572 import QAP_T10572
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10573 import QAP_T10573
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10591 import QAP_T10591
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10592 import QAP_T10592
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MPDark (RoundRobin)" if version is None else f"MPDark (RoundRobin) (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region MP Dark (RoundRobin)
        configuration = ComponentConfiguration("Mp_dark")
        QAP_T10572(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10573(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10591(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10592(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
