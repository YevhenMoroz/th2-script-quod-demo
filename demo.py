import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Algo_Iceberg import QAP_2886, QAP_2950, QAP_3056, QAP_3055, QAP_3054, QAP_3029
from quod_qa.eq.Algo_Multilisted import QAP_3429, QAP_3134, QAP_2476, QAP_2837, QAP_3058, QAP_1967, QAP_1966, QAP_1963, QAP_1962, QAP_1958, QAP_1957, QAP_1954, QAP_1983, QAP_1984, QAP_2068, QAP_1953, QAP_3021, QAP_2982, QAP_1986, QAP_1988, QAP_1965, QAP_1985, QAP_1979, QAP_1977, QAP_1998, QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, QAP_3019, QAP_3022, QAP_3025, QAP_3027,QAP_1951, QAP_1990, QAP_3028
from quod_qa.eq.Algo_TWAP import Test, TEST_MAX, QAP_4760, QAP_4750, QAP_4338, QAP_4405, QAP_4335, QAP_4436, QAP_4254, QAP_4403, QAP_4951, QAP_4407, QAP_4395, QAP_4402, QAP_4333, QAP_4893, QAP_4876,QAP_4406, QAP_4612, QAP_4340, QAP_4404, QAP_4336, QAP_4413, QAP_2864, QAP_2865, QAP_3121, QAP_3117, QAP_3120, QAP_3119, QAP_2478, QAP_3532, QAP_2977, QAP_1318, QAP_1319, QAP_3032, QAP_2955, QAP_3123, QAP_2706, QAP_3122, QAP_3124, QAP_4274, QAP_4582, QAP_4583, QAP_4584
from quod_qa.eq.Algo_PercentageVolume import QAP_4952, QAP_4751, QAP_4778, QAP_4784, QAP_4868, QAP_4935, QAP_4934, QAP_4933, QAP_4930, QAP_4929, QAP_4752, QAP_4761, QAP_4890, QAP_4889, QAP_4646, QAP_4644, QAP_4624, QAP_4605, QAP_4606, QAP_4608, QAP_4607, QAP_1324, QAP_1750, QAP_1510, QAP_1515, QAP_1516, QAP_3070, QAP_2479, QAP_3116, QAP_3065, QAP_3063, QAP_3127, QAP_1633, QAP_2980, QAP_3061, QAP_3062, QAP_2838, QAP_2552, QAP_2553,QAP_1634, QAP_2583, QAP_3530
from quod_qa.eq.algo_acceptance_list import QAP_2994, QAP_2995, QAP_2996, QAP_2997, QAP_2842, QAP_2839
from quod_qa.eq.Algo_VWAP import QAP_4756, QAP_4801, QAP_4800, QAP_4940, QAP_4700, QAP_4699, QAP_4733, QAP_4734, QAP_4735
from quod_qa.eq.Care import QAP_1013
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
    report_id = bca.create_event('srublyov tests')
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)

        #QAP_1324.execute(report_id, session_id)
        # QAP_1750.execute(report_id, session_id) 
        # QAP_2837.execute(report_id, session_id)
        # QAP_2838.execute(report_id, session_id)
        # QAP_4605.execute(report_id)
        # QAP_1810.execute(report_id)
        # QAP_4395.execute(report_id)
        #QAP_4646.execute(report_id) 
        QAP_4890.execute(report_id)

        # QAP_2842.execute(report_id, session_id)
        # QAP_2839.execute(report_id, session_id)

        #region RB
        #TWAP
        # QAP_4612.execute(report_id)
        # QAP_4274.execute(report_id)
        # QAP_4582.execute(report_id)
        # QAP_4583.execute(report_id)
        # QAP_4584.execute(report_id)
        # QAP_4893.execute(report_id)
        # QAP_4951.execute(report_id)
        # QAP_4333.execute(report_id)
        # QAP_4335.execute(report_id)
        # QAP_4336.execute(report_id)
        # QAP_4338.execute(report_id)
        # QAP_4340.execute(report_id)
        # QAP_4876.execute(report_id)
        # QAP_4395.execute(report_id)
        # QAP_4402.execute(report_id)
        # QAP_4403.execute(report_id)
        # QAP_4404.execute(report_id)
        # QAP_4405.execute(report_id)
        # QAP_4406.execute(report_id)
        # QAP_4407.execute(report_id)
        # QAP_4413.execute(report_id)
        # QAP_4750.execute(report_id)
        # QAP_4760.execute(report_id)
        #POV
        # QAP_4624.execute(report_id)
        # QAP_4605.execute(report_id)
        # QAP_4606.execute(report_id)
        # QAP_4607.execute(report_id)
        # QAP_4608.execute(report_id)
        # QAP_4752.execute(report_id)
        # QAP_4761.execute(report_id)
        # QAP_4644.execute(report_id)
        # QAP_4929.execute(report_id)
        # QAP_4933.execute(report_id)
        # QAP_4890.execute(report_id)
        # QAP_4930.execute(report_id)
        # QAP_4934.execute(report_id)
        # QAP_4889.execute(report_id)
        # QAP_4868.execute(report_id)
        # QAP_4784.execute(report_id)
        # QAP_4751.execute(report_id)
        # QAP_4952.execute(report_id)
        #VWAP
        # QAP_4699.execute(report_id)
        # QAP_4700.execute(report_id)
        # QAP_4733.execute(report_id)
        # QAP_4734.execute(report_id)
        # QAP_4735.execute(report_id)
        # QAP_4940.execute(report_id)
        # QAP_4800.execute(report_id)
        # QAP_4801.execute(report_id)
        # QAP_4756.execute(report_id)
        #endregion

        #region Iceberg
        # QAP_3056.execute(report_id)
        # QAP_3055.execute(report_id)
        # QAP_3054.execute(report_id)
        # QAP_3029.execute(report_id)

        #VWAP
        # QAP_4699.execute(report_id)
        # QAP_4700.execute(report_id)
        # QAP_4733.execute(report_id)
        # QAP_4734.execute(report_id)
        # QAP_4735.execute(report_id)
        #endregion

        #region Acceptance list
        # QAP_2839.execute(report_id, session_id)
        # QAP_2842.execute(report_id, session_id)
        # QAP_2994.execute(report_id, session_id)
        # QAP_2995.execute(report_id, session_id)
        # QAP_2996.execute(report_id, session_id)
        # QAP_2997.execute(report_id, session_id)
        #endregion

        #region %Vol tests
        #FIX/FE
        # QAP_1324.execute(report_id, session_id)
        # QAP_1510.execute(report_id, session_id)
        # QAP_1515.execute(report_id, session_id)
        # QAP_1516.execute(report_id, session_id)
        # QAP_1750.execute(report_id, session_id)
        # QAP_2552.execute(report_id, session_id)
        # QAP_2553.execute(report_id, session_id)
        # QAP_2838.execute(report_id, session_id)
        #end FIX/FE
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
        #endregion
        
        #region TWAP tests
        #FIX/FE
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
        #endregion
        
        #region multilisting tests
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
        #endregion
    except Exception:
        #bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__': 
    logging.basicConfig()
    test_run()
    Stubs.factory.close()