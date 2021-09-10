import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Algo_Redburn.Algo_MOC import CLO_FPC_01, CLO_WW_01, CLO_VO_01, CLO_SCAL_OFF_01, CLO_LIM_01
from quod_qa.eq.Algo_Redburn.Algo_MOO import OPN_SCAL_OFF_01, OPN_FPC_01, OPN_LIM_01, OPN_WW_01, OPN_VO_01
from quod_qa.eq.Algo_Redburn.Algo_TWAP import TWAP_WW_01, TWAP_BA_01, TWAP_AUC_01, TWAP_MaxP_01, TWAP_MinP_01, TWAP_NAV_02, TWAP_NAV_01
from quod_qa.eq.Algo_Redburn.Algo_VWAP import VWAP_AUC_01, VWAP_BA_01, VWAP_MaxP_01, VWAP_MinP_01, VWAP_NAV_01, VWAP_NAV_02, VWAP_WW_01
from quod_qa.eq.Algo_Redburn.Algo_POV import POV_AUC_01, POV_BA_01, POV_MaxP_01, POV_MinP_01, POV_NAV_01, POV_NAV_02, POV_WW_01
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
        TWAP_BA_01.execute(report_id)
        TWAP_WW_01.execute(report_id)
        TWAP_NAV_01.execute(report_id)
        TWAP_NAV_02.execute(report_id)
        TWAP_AUC_01.execute(report_id)
        TWAP_MinP_01.execute(report_id)
        TWAP_MaxP_01.execute(report_id)

        VWAP_BA_01.execute(report_id)
        VWAP_WW_01.execute(report_id)
        VWAP_NAV_01.execute(report_id)
        VWAP_NAV_02.execute(report_id)
        VWAP_AUC_01.execute(report_id)
        VWAP_MinP_01.execute(report_id)
        VWAP_MaxP_01.execute(report_id)

        POV_BA_01.execute(report_id)
        POV_WW_01.execute(report_id)
        POV_NAV_01.execute(report_id)
        POV_NAV_02.execute(report_id)
        POV_AUC_01.execute(report_id)
        POV_MinP_01.execute(report_id)
        POV_MaxP_01.execute(report_id)

        CLO_VO_01.execute(report_id)
        CLO_WW_01.execute(report_id)
        CLO_LIM_01.execute(report_id)
        CLO_FPC_01.execute(report_id)
        CLO_SCAL_OFF_01.execute(report_id)

        OPN_VO_01.execute(report_id)
        OPN_WW_01.execute(report_id)
        OPN_LIM_01.execute(report_id)
        OPN_FPC_01.execute(report_id)
        OPN_SCAL_OFF_01.execute(report_id)

        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)

        #QAP_1324.execute(report_id, session_id)
        # QAP_1750.execute(report_id, session_id)
        # QAP_2837.execute(report_id, session_id)
        #QAP_2838.execute(report_id, session_id)
        # QAP_4605.execute(report_id)
        # QAP_1810.execute(report_id)
        # QAP_4395.execute(report_id)
        #QAP_4646.execute(report_id)
        #TraidingSession_test.execute(report_id)
        #SendMarketData.execute(report_id)

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