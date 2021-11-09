import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_autohedging import QAP_3147
from quod_qa.fx.fx_mm_esp import QAP_3141, QAP_2050
from quod_qa.fx.fx_mm_positions import QAP_1895, QAP_1896, preconditions_for_pos
from quod_qa.fx.fx_mm_rfq import for_test_77679, QAP_2089, QAP_2090, QAP_2103, QAP_2345
from quod_qa.fx.fx_mm_synthetic import QAP_2646
from quod_qa.fx.fx_taker_esp import test_new_wrappers
from quod_qa.fx.fx_taker_rfq import QAP_568
from quod_qa.fx.my_methods import send_rfq
from quod_qa.fx.ui_wrappers import wrapper_test

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
        #
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        # rm = RuleManager()
        # # rm.remove_rule_by_id(2)
        # rm.add_fx_md_to("fix-fh-314-luna")
        #
        # rm.print_active_rules()
        #  # Add scripts

        # wrapper_test.execute(report_id, session_id)

        print('duration time = ' + str(datetime.now() - start))

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
