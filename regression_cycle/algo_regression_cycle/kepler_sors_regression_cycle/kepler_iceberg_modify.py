import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5005 import QAP_T5005
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5006 import QAP_T5006
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5011 import QAP_T5011
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5012 import QAP_T5012
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5019 import QAP_T5019
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5020 import QAP_T5020
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5021 import QAP_T5021
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5038 import QAP_T5038
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5042 import QAP_T5042
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5043 import QAP_T5043
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5044 import QAP_T5044
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5045 import QAP_T5045
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5046 import QAP_T5046
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5047 import QAP_T5047
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5056 import QAP_T5056
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5057 import QAP_T5057
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T5058 import QAP_T5058
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Iceberg modification" if version is None else f"Iceberg modification (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Check PartyInfo
        configuration = ComponentConfiguration("Lit_dark_iceberg")
        QAP_T5042(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5043(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5044(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5056(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5057(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5058(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5045(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5046(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5047(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()