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
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4906 import QAP_T4906
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4963 import QAP_T4963
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4965 import QAP_T4965
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4966 import QAP_T4966
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4967 import QAP_T4967
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4970 import QAP_T4970
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4971 import QAP_T4971
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4972 import QAP_T4972
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4973 import QAP_T4973
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4974 import QAP_T4974
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4975 import QAP_T4975
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4976 import QAP_T4976
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4977 import QAP_T4977
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4978 import QAP_T4978
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4979 import QAP_T4979
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4980 import QAP_T4980
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4981 import QAP_T4981
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4982 import QAP_T4982
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4983 import QAP_T4983
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4984 import QAP_T4984
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_T4985 import QAP_T4985

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
        # QAP_T4906(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T4963(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T4965(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T4966(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T4967(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4970(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4971(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4972(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4973(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4974(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4975(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4976(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4977(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4978(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4979(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4980(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4981(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4982(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4983(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4984(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4985(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5002(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5003(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5004(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5063(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5072(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5073(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5074(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5075(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5076(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()