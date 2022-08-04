import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5076 import QAP_T5076
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5075 import QAP_T5075
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5074 import QAP_T5074
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5073 import QAP_T5073
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5072 import QAP_T5072
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5063 import QAP_T5063
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5004 import QAP_T5004
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5003 import QAP_T5003
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T5002 import QAP_T5002

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
        QAP_T5076(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5075(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5074(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5073(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5072(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5063(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5004(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5003(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5002(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()