import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Algo_Multilisted import  QAP_1967, QAP_1966, QAP_1963, QAP_1962, QAP_1958, QAP_1957, QAP_1954, QAP_1983, QAP_1984, QAP_2068, QAP_1953, QAP_3021, QAP_2982, QAP_1986, QAP_1988, QAP_1965, QAP_1985, QAP_1979, QAP_1977, QAP_1998, QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027,QAP_1951, QAP_1990, QAP_3028
from quod_qa.eq.Algo_TWAP import QAP_2864, QAP_2865, QAP_3121, QAP_3117, QAP_3120, QAP_3119, QAP_2478, QAP_3532, QAP_2977, QAP_1318, QAP_1319, QAP_3032, QAP_2955, QAP_3123, QAP_2706, QAP_3122, QAP_3124
from quod_qa.eq.Algo_PercentageVolume import QAP_3070, QAP_2479, QAP_3116, QAP_3065, QAP_3063, QAP_3127, QAP_1633, QAP_2980, QAP_3061, QAP_3062, QAP_2838, QAP_2552, QAP_2553,QAP_1634, QAP_2583, QAP_3062, QAP_3530
from quod_qa.eq.Care import QAP_1013
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe, close_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('FiLL tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        #QAP_1984.execute(report_id)
        #region multilisting tests
        QAP_1810.execute(report_id)
        QAP_1951.execute(report_id)
        QAP_1952.execute(report_id)
        QAP_1953.execute(report_id)
        QAP_1954.execute(report_id)
        QAP_1957.execute(report_id)
        QAP_1958.execute(report_id)
        QAP_1959.execute(report_id)
        QAP_1960.execute(report_id)
        QAP_1961.execute(report_id)
        QAP_1962.execute(report_id)
        QAP_1963.execute(report_id)
        QAP_1965.execute(report_id)
        QAP_1966.execute(report_id)
        QAP_1967.execute(report_id)
        QAP_1968.execute(report_id)
        QAP_1969.execute(report_id)
        QAP_1974.execute(report_id)
        QAP_1975.execute(report_id)
        QAP_1976.execute(report_id)
        QAP_1977.execute(report_id)
        QAP_1979.execute(report_id)
        QAP_1980.execute(report_id)
        QAP_1983.execute(report_id)
        QAP_1984.execute(report_id)
        QAP_1985.execute(report_id)
        QAP_1986.execute(report_id)
        QAP_1988.execute(report_id)
        QAP_1990.execute(report_id)
        QAP_1992.execute(report_id)
        QAP_1995.execute(report_id)
        QAP_1996.execute(report_id)
        QAP_1997.execute(report_id)
        QAP_1998.execute(report_id)
        QAP_2982.execute(report_id)
        QAP_3019.execute(report_id)
        QAP_3021.execute(report_id)
        QAP_3022.execute(report_id)
        QAP_3025.execute(report_id)
        QAP_3027.execute(report_id)
        QAP_3028.execute(report_id)
        #endregion
    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__': 
    logging.basicConfig()
    test_run()
    Stubs.factory.close()