import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_Synthetic_TIF.QAP_T8984 import QAP_T8984
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_Synthetic_TIF.QAP_T4188 import QAP_T4188
from test_cases.algo.Algo_Kepler.Algo_Synthetic_TIF.QAP_T4207 import QAP_T4207
from test_cases.algo.Algo_Kepler.Algo_Synthetic_TIF.QAP_T4747 import QAP_T4747
from test_cases.algo.Algo_Kepler.Algo_Synthetic_TIF.QAP_T8913 import QAP_T8913

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"SyntheticTIF" if version is None else f"SyntheticTIF (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Synthetic TIF
        configuration = ComponentConfiguration("Sorping")
        QAP_T4188(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4207(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4747(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8913(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8984(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()