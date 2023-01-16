import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7894 import QAP_T7894
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7895 import QAP_T7895
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7896 import QAP_T7896
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7897 import QAP_T7897
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7898 import QAP_T7898
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7899 import QAP_T7899
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7900 import QAP_T7900
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7901 import QAP_T7901
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7902 import QAP_T7902
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7903 import QAP_T7903
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7904 import QAP_T7904
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7905 import QAP_T7905
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7906 import QAP_T7906
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7907 import QAP_T7907
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7908 import QAP_T7908
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7909 import QAP_T7909
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7910 import QAP_T7910
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7911 import QAP_T7911
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7912 import QAP_T7912
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7913 import QAP_T7913
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7914 import QAP_T7914
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7915 import QAP_T7915
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7916 import QAP_T7916
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7917 import QAP_T7917
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7918 import QAP_T7918
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7919 import QAP_T7919
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7920 import QAP_T7920
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7921 import QAP_T7921
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7922 import QAP_T7922
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7923 import QAP_T7923
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7924 import QAP_T7924
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7925 import QAP_T7925
from test_cases.algo.Algo_Kepler.Algo_Instrument_Identification.QAP_T7926 import QAP_T7926
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Instrument Identification" if version is None else f"Instrument Identification (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Instrument identification
        configuration = ComponentConfiguration("Sorping")
        QAP_T7894(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7895(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7896(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7897(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7898(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7899(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7900(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7901(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7902(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7903(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7904(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7905(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7906(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7907(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7908(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7909(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7910(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7911(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7912(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7913(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7914(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7915(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7916(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7917(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7918(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7919(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7920(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7921(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7922(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7923(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7924(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7925(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7926(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()