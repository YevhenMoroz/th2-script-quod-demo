import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from MyFiles import send_rfq, SendMD, StreamRefresh, MyTest
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_6007, QAP_6008, QAP_6010, QAP_3017, QAP_3233, QAP_2325, QAP_6116, \
    QAP_2228, QAP_2113, QAP_3147, QAP_3146, QAP_2470, QAP_2159, AH_Precondition, QAP_2250, QAP_2251, QAP_2252, QAP_2255, \
    QAP_2265, QAP_2290, QAP_3354, QAP_3819, QAP_3939, QAP_4122, import_AH_layout, QAP_2292, QAP_2293, QAP_2322, \
    QAP_2326, QAP_3039, QAP_3067
from test_cases.fx.fx_mm_esp import QAP_6148, QAP_2082, QAP_2075, QAP_2078, QAP_1599, QAP_2034, QAP_2035, QAP_2037, \
    QAP_2038, QAP_2039, QAP_2079, QAP_2084, QAP_2085, QAP_2086, QAP_2556, QAP_2844, QAP_2855, QAP_2872, QAP_2880, \
    QAP_3045, QAP_3563, QAP_3661, QAP_3841, QAP_3848, QAP_4016, QAP_5389, QAP_3394, QAP_6153, QAP_2966
from test_cases.fx.fx_mm_rfq import QAP_3003, QAP_4777, QAP_5814
from test_cases.fx.fx_mm_rfq.QAP_5992 import QAP_5992
from test_cases.fx.fx_mm_rfq.interpolation import QAP_3766, QAP_3734
from test_cases.fx.fx_taker_esp import QAP_3140, QAP_3141, QAP_3414, QAP_3415, QAP_3418, QAP_3694, QAP_2373, QAP_3069
from test_cases.fx.fx_taker_rfq import QAP_3002, import_rfq_taker_layout, QAP_581, QAP_582, QAP_584, QAP_2847
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)
timeouts = False

channels = dict()

def test_run():

    # Generation id and time for test run
    report_id = bca.create_event('Aleksey tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"

    session_id = set_session_id()
    data_set = FxDataSet()

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)
        # QAP_5992(report_id, session_id, data_set).execute()
        # QAP_6153.QAP_6153(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_2966.execute(report_id)
        # send_rfq.execute(report_id)
        # QAP_4777.execute(report_id, session_id)
        # SendMD.execute(report_id)


        MyTest.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








