import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5015 import QAP_T5015
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5016 import QAP_T5016
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5017 import QAP_T5017
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5018 import QAP_T5018
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5022 import QAP_T5022
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5023 import QAP_T5023
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5024 import QAP_T5024
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5025 import QAP_T5025
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5026 import QAP_T5026
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5027 import QAP_T5027
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Kepler custom tags" if version is None else f"Kepler custom tags (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Check PartyInfo
        configuration = ComponentConfiguration("Lit_dark_iceberg")
        QAP_T5015(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5016(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5018(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5022(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5023(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5024(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()