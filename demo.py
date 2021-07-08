import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from examples.dealer_intervention import get_rfq_details
from quod_qa.eq.Algo_Multilisted import QAP_2982, QAP_1986, QAP_1988, QAP_1965, QAP_1985, QAP_1979, QAP_1977, QAP_1998, \
    QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, \
    QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027, QAP_1951, \
    QAP_1990, QAP_3028

from quod_qa.fx import ui_tests
from quod_qa.fx.fx_mm_esp import QAP_2084
from quod_qa.fx.fx_mm_rfq import (QAP_1970, QAP_1971, QAP_1972, QAP_2062, QAP_2121, QAP_1545, QAP_1537, QAP_1539,
                                  QAP_1541CANCELLED, QAP_1542, QAP_1547, QAP_1548, QAP_1562, QAP_1563, QAP_1746_WIP,
                                  QAP_2066)
from quod_qa.fx.fx_taker_rfq import QAP_718
from rule_management import RuleManager
from stubs import Stubs
from test_cases import QAP_638, QAP_1552, QAP_2715
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()


def prepare_fe(case_id, session_id):
    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
        # ,
        #          fe_dir='qf_trading_fe_folder_308',
        #          fe_user='qf_trading_fe_user_308',
        #          fe_pass='qf_trading_fe_password_308')
    else:
        get_opened_fe(case_id, session_id)

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('kbrit tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    s_id = set_session_id()
    Stubs.frontend_is_open = True
    try:
        # case_params = {
        #     'case_id': bca.create_event_id(),
        #     'TraderConnectivity': 'gtwquod5-fx',
        #     'Account': 'MMCLIENT1',
        #     'SenderCompID': 'QUODFX_UAT',
        #     'TargetCompID': 'QUOD5',
        #     }
        case_params = {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
            'Account': 'Iridium1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD9',
            }

        start = datetime.now()
        print(f'start time = {start}')
        prepare_fe(report_id,s_id)


        ui_tests.execute(report_id, s_id)
        # QAP_2715.TestCase(report_id,s_id).execute( )
        # QAP_2066.execute(report_id, case_params, s_id)



        rm = RuleManager()
        # rm.add_fx_md_to('fix-fh-314-luna')
        # rm.add_RFQ_test_sim('fix-bs-rfq-314-luna-standard')
        # rm.add_TRFQ_test_sim('fix-bs-rfq-314-luna-standard')
        # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
        # rm.remove_rule_by_id_test_sim(1)
        # rm.print_active_rules_sim_test()
        # rm.print_active_rules()
        # rm.remove_rule_by_id(630)


        print('duration time = ' + str(datetime.now() - start))

    except Exception:
        logging.error("Error execution", exc_info=True)

    finally:
        Stubs.win_act.unregister(s_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
