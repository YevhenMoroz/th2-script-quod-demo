import logging

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10298 import QAP_T10298
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10299 import QAP_T10299
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MPDark (Dark phase)" if version is None else f"MPDark (Dark phase) (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region MP Dark (Dark Phase Only)
        configuration = ComponentConfiguration("Mp_dark")
        # The tolerance for the DarkPool algo will change from 1 to 3 in the QAP-T10298 and revert in the QP-T10592 from the 'kepler_mpdark_round_robin_change_configs.py'
        QAP_T10298(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10299(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
