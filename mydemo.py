import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_cases.algo.Algo_Multilisted.QAP_1810 import QAP_1810
from test_cases.algo.Algo_Multilisted.QAP_1968 import QAP_1968
from test_cases.algo.Algo_Multilisted.QAP_1969 import QAP_1969
from test_cases.algo.Algo_Multilisted.QAP_1977 import QAP_1977
from test_cases.algo.Algo_Multilisted.QAP_1979 import QAP_1979
from test_cases.algo.Algo_Multilisted.QAP_1983 import QAP_1983
from test_cases.algo.Algo_Multilisted.QAP_1984 import QAP_1984
from test_cases.algo.Algo_Redburn.Test import PDAT_1549
from test_cases.algo.Algo_Redburn.Test import PDAT_1507


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('skolesnyk tests')
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
       configuration = ComponentConfiguration("multilisted")
       # QAP_1810(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       # QAP_1968(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       # QAP_1969(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       # QAP_1977(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       # QAP_1979(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       # QAP_1983(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       QAP_1984(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
       # PDAT_1507.execute(report_id)

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()