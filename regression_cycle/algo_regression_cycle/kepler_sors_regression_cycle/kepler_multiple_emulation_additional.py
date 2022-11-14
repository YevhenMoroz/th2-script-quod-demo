import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4709 import QAP_T4709
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4920 import QAP_T4920
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4921 import QAP_T4921
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4922 import QAP_T4922
from test_cases.algo.Algo_Kepler.Algo_Multiple_Emulation.QAP_T4923 import QAP_T4923


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MultipleEmulation (additional tests)" if version is None else f"MultipleEmulation (additional tests) (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Multiple Emulation additional
        configuration = ComponentConfiguration("Multiple_emulation")
        QAP_T4709(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4920(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4921(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4922(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4923(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()