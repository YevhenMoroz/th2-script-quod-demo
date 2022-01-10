import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from MyFiles import send_rfq, SendMD, StreamRefresh, MyTest
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_6007, QAP_6008, QAP_6010, QAP_3017, QAP_3233, QAP_2325, QAP_6116, \
    QAP_2228, QAP_2113, QAP_3147, QAP_3146, QAP_2470, QAP_2159, AH_Precondition, QAP_2250, QAP_2251, QAP_2252, QAP_2255, \
    QAP_2265, QAP_2290, QAP_3354, QAP_3819, QAP_3939, QAP_4122
from test_cases.fx.fx_mm_esp import QAP_6148, QAP_2082, QAP_2075, QAP_2078, QAP_1599, QAP_2034, QAP_2035, QAP_2037, \
    QAP_2038, QAP_2039, QAP_2079, QAP_2084, QAP_2085, QAP_2086, QAP_2556, QAP_2844, QAP_2855, QAP_2872, QAP_2880, \
    QAP_3045, QAP_3563, QAP_3661, QAP_3841, QAP_3848, QAP_4016, QAP_5389, QAP_3394
from test_cases.fx.fx_mm_rfq import QAP_3003, QAP_4777, QAP_5814
from test_cases.fx.fx_mm_rfq.interpolation import QAP_3766, QAP_3734
from test_cases.fx.fx_taker_esp import QAP_3140, QAP_3141, QAP_3414, QAP_3415, QAP_3418, QAP_3694, QAP_2373
from test_cases.fx.fx_taker_rfq import QAP_3002
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
    test_cases = {
        'case_id': bca.create_event_id(),
        'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
        'Account': 'Iridium1',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
    }

    session_id = set_session_id()
    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)
        # QAP_6007.execute(report_id, session_id)
        # QAP_6008.execute(report_id, session_id)
        # QAP_6010.execute(report_id, session_id)
        # QAP_3017.execute(report_id, session_id)
        # QAP_3233.execute(report_id, session_id)
        # QAP_2325.execute(report_id, session_id)
        # QAP_6116.execute(report_id, session_id)
        # QAP_2113.execute(report_id, session_id) # TODO: Amend order via new wrapper
        # QAP_3661.execute(report_id, session_id)
        # QAP_6148.execute(report_id, session_id)
        # QAP_3002.execute(report_id, session_id)
        # QAP_2844.execute(report_id, session_id)
        # QAP_3394.execute(report_id, session_id)
        # rm = RuleManager()
        # QAP_5389.QAP_5389().execute(report_id)
        # SendMD.execute(report_id)
        # send_rfq.execute(report_id)
        # StreamRefresh.execute(report_id)
        MyTest.execute(report_id, session_id)
        # QAP_3140.execute(report_id, session_id)
        # QAP_3141.execute(report_id)
        # QAP_2082.execute(report_id)
        # QAP_2075.execute(report_id, session_id)
        # QAP_2078.execute(report_id)
        # QAP_3147.execute(report_id, session_id)
        # QAP_3146.execute(report_id, session_id)
        # AH_Precondition.execute(report_id)
        # QAP_2470.execute(report_id, session_id)
        # QAP_2159.execute(report_id, session_id)
        # QAP_3017.execute(report_id, session_id)
        # QAP_3734.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








