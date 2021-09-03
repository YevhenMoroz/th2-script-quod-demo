import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_autohedging import QAP_2228, QAP_2290
from quod_qa.fx.fx_mm_esp import QAP_1418, QAP_4094
from quod_qa.fx.fx_mm_positions import QAP_1898
from quod_qa.fx.fx_mm_rfq import QAP_1552, QAP_1539, QAP_2091, QAP_2101, QAP_2104, QAP_2105, QAP_2295, QAP_2296, \
    QAP_2297, QAP_2958, QAP_1746, QAP_1540, QAP_1562, QAP_1563, QAP_1970, QAP_2103, QAP_2177, QAP_3565, QAP_2877, \
    QAP_4228, QAP_4085, QAP_3106, QAP_3107, QAP_3108, QAP_3109, QAP_2382, QAP_3110, QAP_3111, QAP_3112, QAP_3113, \
    QAP_3234, QAP_3250, QAP_1978, QAP_3409, QAP_3494, QAP_2353, QAP_3704, QAP_3003, QAP_4509
from quod_qa.fx.fx_taker_esp import QAP_2949
from quod_qa.fx.fx_taker_rfq import QAP_2826, QAP_3048
from quod_qa.fx.my_methods import send_rfq, send_md, sequence_test

from rule_management import RuleManager

from stubs import Stubs
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def rule_creation():
    rule_manager = RuleManager()
    rfq_quote = rule_manager.add_RFQ('fix-bs-rfq-314-luna-standard')
    rfq_trade = rule_manager.add_TRFQ('fix-bs-rfq-314-luna-standard')
    # return [rfq_quote, rfq_trade]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('ostronov tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"

    session_id = set_session_id()
    # rules = rule_creation()
    try:
        start = datetime.now()
        print(f'start time = {start}')
        case_params = {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
            'Account': 'Iridium1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD9',
        }

        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)

        # rm = RuleManager()
        # rm.print_active_rules()
        # rm.print_active_rules_sim_test()
         # Add scripts
        # QAP_3409.execute(report_id, session_id)
        # QAP_3048.execute(report_id, session_id)
        # QAP_3003.execute(report_id)
        QAP_4509.execute(report_id)
        # QAP_3494.execute(report_id)

        # QAP_2296.execute(report_id, session_id)

        # QAP_2353.execute(report_id)
        # QAP_3704.execute(report_id, session_id)
        # sequence_test.execute(report_id)
        # send_rfq.execute(report_id)

        print('duration time = ' + str(datetime.now() - start))

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
