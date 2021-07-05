import logging
from datetime import datetime
from custom import basic_custom_actions as bca

from quod_qa.fx.fx_mm_rfq import  QAP_1545
from rule_management import RuleManager
from stubs import Stubs
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
    report_id = bca.create_event(' tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
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

        prepare_fe(report_id,s_id)
        # rm = RuleManager()
        # rm.print_active_rules()



    except Exception:
        logging.error("Error execution", exc_info=True)

    finally:
        Stubs.win_act.unregister(s_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
