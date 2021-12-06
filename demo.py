import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from MyFiles import send_rfq, SendMD, StreamRefresh, MyTest
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_6007, QAP_6008, QAP_6010, QAP_3017, QAP_3233, QAP_2325, QAP_6116, \
    QAP_2228, QAP_2113
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
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        # QAP_6007.execute(report_id, session_id)
        # QAP_6008.execute(report_id, session_id)
        # QAP_6010.execute(report_id, session_id)
        # QAP_3017.execute(report_id, session_id)
        # QAP_3233.execute(report_id, session_id)
        # QAP_2325.execute(report_id, session_id)
        # QAP_6116.execute(report_id, session_id)
        # QAP_2113.execute(report_id, session_id) # TODO: Amend order via new wrapper
        # rm = RuleManager()
        # SendMD.execute(report_iid)
        # send_rfq.execute(report_id)
        # StreamRefresh.execute(report_id)
        # MyTest.execute(report_id)


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








