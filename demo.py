import logging
from datetime import datetime

# MyFiles import SendMD
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_2470, QAP_3082
from test_cases.fx.fx_mm_esp import QAP_2069, QAP_1536, QAP_1559, QAP_1511, QAP_1554, QAP_1589, QAP_1599, QAP_1601, \
    QAP_1643, QAP_1696, QAP_2012, QAP_2034, QAP_2035, QAP_2037, QAP_2038, QAP_2039, QAP_2050, QAP_2051, QAP_2587, \
    QAP_2750, QAP_2872, QAP_2873, QAP_2874, QAP_2876, QAP_2879, QAP_2957, QAP_3045, QAP_2823, QAP_2880, QAP_3390, \
    QAP_3661, QAP_6151, QAP_6148
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389
from test_cases.fx.fx_mm_rfq import QAP_2101, QAP_3003, QAP_4777, QAP_3494, QAP_3409, QAP_3110, QAP_3111, QAP_2103, \
    QAP_1537
from test_cases.fx.fx_mm_rfq.QAP_5992 import QAP_5992
from test_cases.fx.fx_mm_rfq.QAP_6364 import QAP_6364
from test_cases.fx.fx_mm_rfq.QAP_6531 import QAP_6531
from test_cases.fx.fx_mm_rfq.interpolation import QAP_3766, QAP_3762, QAP_3739
from test_cases.fx.fx_taker_esp import QAP_3141, QAP_2373
from test_cases.fx.fx_taker_rfq import QAP_569, QAP_574, QAP_2836, QAP_2847, QAP_849, QAP_3048
from test_cases.fx.fx_taker_rfq.QAP_6 import QAP_6
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)
timeouts = False

channels = dict()

def test_run():

    # Generation id and time for test run
    report_id = bca.create_event('amedents tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
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
    data_set = FxDataSet()
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        QAP_6531(report_id, session_id, data_set).execute()
        # QAP_5992(report_id, data_set=data_set).execute()
    #     QAP_3766.execute(report_id)
        #QAP_653.execute(report_id, session_id)
        #SendMD.execute(report_id)



    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()







