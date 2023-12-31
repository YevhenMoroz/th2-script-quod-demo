import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_VWAP import QAP_T4285
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T10427 import QAP_T10427
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T10429 import QAP_T10429
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T10943 import QAP_T10943
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T10944 import QAP_T10944
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11220 import QAP_T11220
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11227 import QAP_T11227
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11304 import QAP_T11304
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11312 import QAP_T11312
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11329 import QAP_T11329
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11355 import QAP_T11355
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11373 import QAP_T11373
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T11374 import QAP_T11374
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T4218 import QAP_T4218
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T7958 import QAP_T7958
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T8801 import QAP_T8801
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T9462 import QAP_T9462
from test_cases.algo.Algo_Redburn.Algo_VWAP.QAP_T9463 import QAP_T9463
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
        QAP_T10943(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10944(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11227(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11304(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11312(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11329(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11355(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11373(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11374(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # region sub-slices
        QAP_T4218(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        QAP_T8801(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11220(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # region Buy-back
        QAP_T7958(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9462(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9463(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10427(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10429(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()