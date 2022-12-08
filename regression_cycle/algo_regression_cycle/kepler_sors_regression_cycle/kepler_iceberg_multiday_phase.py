import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4181 import QAP_T4181
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4182 import QAP_T4182
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4183 import QAP_T4183
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5007 import QAP_T5007
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5008 import QAP_T5008
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5040 import QAP_T5040
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5041 import QAP_T5041
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Iceberg - Multiday, Phase" if version is None else f"Iceberg (Multiday, Phases) (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Check PartyInfo
        configuration = ComponentConfiguration("Lit_dark_iceberg")
        QAP_T4181(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4182(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4183(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5007(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5008(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5040(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5041(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()