import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Algo_Multilisted import QAP_3429, QAP_3134, QAP_2476, QAP_2837, QAP_3058, QAP_1967, QAP_1966, QAP_1963, \
    QAP_1962, QAP_1958, QAP_1957, QAP_1954, QAP_1983, QAP_1984, QAP_2068, QAP_1953, QAP_3021, QAP_2982, QAP_1986, \
    QAP_1988, QAP_1965, QAP_1985, QAP_1979, QAP_1977, QAP_1998, QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, \
    QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, \
    QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027, QAP_1951, QAP_1990, QAP_3028
from quod_qa.eq.Algo_TWAP import QAP_4340, QAP_4404, QAP_4336, QAP_4413, QAP_2864, QAP_2865, QAP_3121, QAP_3117, \
    QAP_3120, QAP_3119, QAP_2478, QAP_3532, QAP_2977, QAP_1318, QAP_1319, QAP_3032, QAP_2955, QAP_3123, QAP_2706, \
    QAP_3122, QAP_3124
from quod_qa.eq.Algo_PercentageVolume import QAP_1324, QAP_1750, QAP_1510, QAP_1515, QAP_1516, QAP_3070, QAP_2479, \
    QAP_3116, QAP_3065, QAP_3063, QAP_3127, QAP_1633, QAP_2980, QAP_3061, QAP_3062, QAP_2838, QAP_2552, QAP_2553, \
    QAP_1634, QAP_2583, QAP_3062, QAP_3530
from quod_qa.eq.Care import QAP_1013, QAP_1070, QAP_2592, QAP_1365, QAP_4686, QAP_4716, QAP_3616, QAP_3328, QAP_1723, \
    QAP_1045, QAP_1067, QAP_1068, QAP_3339, QAP_4901
from quod_qa.eq.DMA import QAP_2551, QAP_4393
from quod_qa.eq.PostTrade import QAP_3936
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('vskulinec tests ')
    logger.info(f"Root event was created (id = {report_id.id})")

    session_id = set_session_id()
    # QAP_1324.execute(report_id, session_id)
    # QAP_1750.execute(report_id, session_id)
    # QAP_1365.execute(report_id, session_id)
    # QAP_3339.execute(report_id, session_id)
    QAP_4901.execute(report_id, session_id)
    # QAP_2838.execute(report_id, session_id)
    # QAP_1810.execute(report_id)

    # QAP_2842.execute(report_id, session_id)
    # QAP_2839.execute(report_id, session_id)

    # region %Vol tests
    # FIX/FE
    # QAP_1324.execute(report_id, session_id)
    # QAP_1510.execute(report_id, session_id)
    # QAP_1515.execute(report_id, session_id)
    # QAP_1516.execute(report_id, session_id)
    # QAP_1750.execute(report_id, session_id)
    # QAP_2552.execute(report_id, session_id)
    # QAP_2553.execute(report_id, session_id)
    # QAP_2838.execute(report_id, session_id)
    # end FIX/FE
    # QAP_1633.execute(report_id)
    # QAP_1634.execute(report_id)
    # QAP_2479.execute(report_id)
    # QAP_2980.execute(report_id)
    # QAP_3061.execute(report_id)
    # QAP_3062.execute(report_id)
    # QAP_3063.execute(report_id)
    # QAP_3065.execute(report_id)
    # QAP_3070.execute(report_id)
    # QAP_3116.execute(report_id)
    # QAP_3127.execute(report_id)
    # QAP_3530.execute(report_id)
    # endregion

    # region TWAP tests
    # FIX/FE
    # QAP_2864.execute(report_id, session_id)
    # QAP_2865.execute(report_id, session_id)
    # #end FIX/FE
    # QAP_2706.execute(report_id)
    # QAP_2478.execute(report_id)
    # QAP_2955.execute(report_id)
    # QAP_2977.execute(report_id)
    # QAP_3032.execute(report_id)
    # QAP_3117.execute(report_id)
    # QAP_3119.execute(report_id)
    # QAP_3120.execute(report_id)
    # QAP_3121.execute(report_id)
    # QAP_3122.execute(report_id)
    # QAP_3123.execute(report_id)
    # QAP_3124.execute(report_id)
    # QAP_3532.execute(report_id)
    # endregion

    # region multilisting tests
    # QAP_1810.execute(report_id)
    # QAP_1951.execute(report_id)
    # QAP_1952.execute(report_id)
    # QAP_1953.execute(report_id)
    # QAP_1954.execute(report_id)
    # QAP_1957.execute(report_id)
    # QAP_1958.execute(report_id)
    # QAP_1959.execute(report_id)
    # QAP_1960.execute(report_id)
    # QAP_1961.execute(report_id)
    # QAP_1962.execute(report_id)
    # QAP_1963.execute(report_id)
    # QAP_1965.execute(report_id)
    # QAP_1966.execute(report_id)
    # QAP_1967.execute(report_id)
    # QAP_1968.execute(report_id)
    # QAP_1969.execute(report_id)
    # QAP_1974.execute(report_id)
    # QAP_1975.execute(report_id)
    # QAP_1976.execute(report_id)
    # QAP_1977.execute(report_id)
    # QAP_1979.execute(report_id)
    # QAP_1980.execute(report_id)
    # QAP_1983.execute(report_id)
    # QAP_1984.execute(report_id)
    # QAP_1985.execute(report_id)
    # QAP_1986.execute(report_id)
    # QAP_1988.execute(report_id)
    # QAP_1990.execute(report_id)
    # QAP_1992.execute(report_id)
    # QAP_1995.execute(report_id)
    # QAP_1996.execute(report_id)
    # QAP_1997.execute(report_id)
    # QAP_1998.execute(report_id)
    # QAP_2476.execute(report_id)
    # QAP_2982.execute(report_id)
    # QAP_3019.execute(report_id)
    # QAP_3021.execute(report_id)
    # QAP_3022.execute(report_id)
    # QAP_3025.execute(report_id)
    # QAP_3027.execute(report_id)
    # QAP_3028.execute(report_id)
    # QAP_3058.execute(report_id)
    # QAP_3134.execute(report_id)
    # endregion


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
