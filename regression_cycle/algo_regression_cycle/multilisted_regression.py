from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_Multilisted import QAP_1988, QAP_1992, QAP_1967, QAP_1995, QAP_2476, QAP_1996, \
    QAP_2982, QAP_3058, QAP_3028, QAP_3027, QAP_1977, QAP_3025, QAP_3134, QAP_1990,  QAP_1997, QAP_1998, QAP_3022, \
    QAP_1966, QAP_3021, QAP_3019
from test_cases.algo.Algo_Multilisted.QAP_1810 import QAP_1810
from test_cases.algo.Algo_Multilisted.QAP_1951 import QAP_1951
from test_cases.algo.Algo_Multilisted.QAP_1952 import QAP_1952
from test_cases.algo.Algo_Multilisted.QAP_1953 import QAP_1953
from test_cases.algo.Algo_Multilisted.QAP_1954 import QAP_1954
from test_cases.algo.Algo_Multilisted.QAP_1957 import QAP_1957
from test_cases.algo.Algo_Multilisted.QAP_1958 import QAP_1958
from test_cases.algo.Algo_Multilisted.QAP_1959 import QAP_1959
from test_cases.algo.Algo_Multilisted.QAP_1960 import QAP_1960
from test_cases.algo.Algo_Multilisted.QAP_1961 import QAP_1961
from test_cases.algo.Algo_Multilisted.QAP_1962 import QAP_1962
from test_cases.algo.Algo_Multilisted.QAP_1963 import QAP_1963
from test_cases.algo.Algo_Multilisted.QAP_1965 import QAP_1965
from test_cases.algo.Algo_Multilisted.QAP_1966 import QAP_1966
from test_cases.algo.Algo_Multilisted.QAP_1967 import QAP_1967
from test_cases.algo.Algo_Multilisted.QAP_1968 import QAP_1968
from test_cases.algo.Algo_Multilisted.QAP_1969 import QAP_1969
from test_cases.algo.Algo_Multilisted.QAP_1974 import QAP_1974
from test_cases.algo.Algo_Multilisted.QAP_1975 import QAP_1975
from test_cases.algo.Algo_Multilisted.QAP_1976 import QAP_1976
from test_cases.algo.Algo_Multilisted.QAP_1977 import QAP_1977
from test_cases.algo.Algo_Multilisted.QAP_1979 import QAP_1979
from test_cases.algo.Algo_Multilisted.QAP_1980 import QAP_1980
from test_cases.algo.Algo_Multilisted.QAP_1983 import QAP_1983
from test_cases.algo.Algo_Multilisted.QAP_1984 import QAP_1984
from test_cases.algo.Algo_Multilisted.QAP_1985 import QAP_1985
from test_cases.algo.Algo_Multilisted.QAP_1986 import QAP_1986
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None):
    report_id = bca.create_event('Algo', parent_id)
    try:
        configuration = ComponentConfiguration("multilisted")
        QAP_1810(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1951(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1952(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1953(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1954(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1957(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1958(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1959(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1960(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1961(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1962(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1963(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1965(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1966(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1967(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1968(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1969(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1974(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1975(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1976(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1977(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1979(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1980(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1983(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1984(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1985(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1986(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1988.execute(report_id)
        QAP_1990.execute(report_id)
        QAP_1992.execute(report_id)
        QAP_1995.execute(report_id)
        QAP_1996.execute(report_id)
        QAP_1997.execute(report_id)
        QAP_1998.execute(report_id)
        QAP_2476.execute(report_id)
        QAP_2982.execute(report_id)
        QAP_3019.execute(report_id)
        QAP_3021.execute(report_id)
        QAP_3022.execute(report_id)
        QAP_3025.execute(report_id)
        QAP_3027.execute(report_id)
        QAP_3028.execute(report_id)
        QAP_3058.execute(report_id)
        QAP_3134.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
