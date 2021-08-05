import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from examples import example_java_api
from quod_qa.fx import clone, SendMD
from quod_qa.fx.fx_mm_autohedging import QAP_2290, QAP_2228

from quod_qa.fx.fx_mm_esp import QAP_2990, QAP_1518, QAP_1558, QAP_1559, QAP_2797, QAP_2082, QAP_2084, QAP_2086, \
    QAP_2085, QAP_2079, QAP_3841, QAP_1554, QAP_1597, QAP_3390, QAP_2823, QAP_2750, QAP_2874, QAP_2876, QAP_2880, \
    QAP_2879, QAP_2873, QAP_2872, QAP_2966, QAP_3848, QAP_2012, QAP_2078, QAP_4094
from quod_qa.fx.fx_mm_positions import QAP_2500, QAP_1898
from quod_qa.fx.fx_mm_rfq import QAP_1537, QAP_1539, QAP_2345, QAP_1746, QAP_1978, QAP_2089, QAP_2055, QAP_2090, \
    QAP_1755, QAP_2103, QAP_2353, QAP_2101, QAP_2104
from quod_qa.fx.fx_taker_esp import QAP_404
from quod_qa.fx.qs_fx_routine import rfq_spot, java_api
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

def fx_mm_esp_fix(report_id):
    QAP_1518.execute(report_id)
    QAP_1558.execute(report_id)
    QAP_1559.execute(report_id)
    QAP_2797.execute(report_id)
    QAP_2082.execute(report_id)
    QAP_2084.execute(report_id)
    QAP_2086.execute(report_id)
    QAP_2085.execute(report_id)
    QAP_2079.execute(report_id)
    QAP_2078.execute(report_id)
    QAP_3841.execute(report_id)
    QAP_1554.execute(report_id)
    QAP_1597.execute(report_id)
    QAP_3390.execute(report_id)
    QAP_2750.execute(report_id)
    QAP_2823.execute(report_id)
    QAP_2874.execute(report_id)
    QAP_2876.execute(report_id)
    QAP_2880.execute(report_id)
    QAP_2879.execute(report_id)
    QAP_2873.execute(report_id)
    QAP_2872.execute(report_id)
    QAP_2966.execute(report_id)
    QAP_3848.execute(report_id)
    QAP_2012.execute(report_id)
    # QAP_2082.execute(report_id)

def fx_mm_rfq_fix(report_id):
    QAP_1746.execute(report_id)
    QAP_1978.execute(report_id)
    QAP_2089.execute(report_id)
    QAP_2090.execute(report_id)
    QAP_1755.execute(report_id)


def test_run():
    # Generation id and time for test run

    # report_id = bca.create_event(' tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    report_id = bca.create_event('KKL    ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"


    test_cases = {
        'case_id': bca.create_event_id(),
        'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
        'Account': 'Iridium1',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
    }

    session_id=set_session_id()
    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)

        # QAP_2092WIP.execute(report_id,session_id)
        # QAP_1558.execute(report_id)

        # java_api.TestCase(report_id).execute()
        # example_java_api.TestCase(report_id).execute()
        # QAP_2012.execute(report_id)

        rfq_spot.execute(report_id)

        # QAP_2104.execute(report_id,session_id)


        # clone.execute(report_id)

        # QAP_2103.execute(report_id)

        # QAP_3841.execute(report_id)
        # QAP_1898.execute(report_id, session_id)
        # QAP_2089.execute(report_id)
        # QAP_3841.execute(report_id)
        # QAP_1518.execute(report_id)
        # QAP_404.execute(report_id)
        # SendMD.execute(report_id)

        # QAP_2290.execute(report_id,session_id)





        #
        # rm = RuleManager()
        # # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
        # rm.print_active_rules()
        # rm.remove_rule_by_id()


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

#
   #     rm.print_active_rules()
#
    #   ui_tests.execute(report_id)

    #except Exception:
        #logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








