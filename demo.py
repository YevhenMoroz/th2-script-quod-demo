import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx import send_md
from quod_qa.fx.fx_mm_esp import QAP_1418
from quod_qa.fx.fx_mm_positions import QAP_1897
from quod_qa.fx.fx_mm_rfq import QAP_2483, QAP_2490, QAP_2488, QAP_2484, QAP_2486, QAP_2489, QAP_2877, QAP_2878
from quod_qa.fx.fx_taker_esp import QAP_2, QAP_19, QAP_492, QAP_228, QAP_458, QAP_530, QAP_3066, QAP_3068, QAP_3069, \
    QAP_3157, QAP_3644

from quod_qa.fx.fx_taker_rfq import QAP_612

from rule_management import RuleManager

from stubs import Stubs
from test_cases import QAP_1552, QAP_2143
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

        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)


        # # Add scripts
        # QAP_2483.execute(report_id, session_id)
        # QAP_2484.execute(report_id, session_id)
        # QAP_2486.execute(report_id, session_id)
        QAP_2488.execute(report_id, session_id)
        # QAP_2489.execute(report_id, session_id)
        # QAP_2490.execute(report_id, session_id)
        # QAP_2877.execute(report_id, session_id)
        # QAP_2878.execute(report_id, session_id)

        # rule_manager = RuleManager()
        # rule_manager.remove_rules_by_id_list([5, 7])
        # rule_manager.add_RFQ('fix-bs-rfq-314-luna-standard')
        # rule_manager.print_active_rules()
        print('duration time = ' + str(datetime.now() - start))

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
