import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx import ui_tests
from quod_qa.fx.fx_mm_esp import QAP_1560, QAP_2825, QAP_2555, QAP_2038, QAP_1599, QAP_1518, QAP_2034, QAP_2075, \
    QAP_1601, QAP_2039, QAP_2035, QAP_1418, QAP_2556, QAP_2117, QAP_2855, QAP_3563, QAP_2069, QAP_2646, QAP_2587, \
    QAP_2796, QAP_1536, QAP_2037, QAP_2072, QAP_2523, QAP_3045, QAP_1589, QAP_1643_wip
from quod_qa.fx.fx_mm_positions import QAP_2505, QAP_2378, QAP_2491, QAP_2492, QAP_2494, QAP_2496, QAP_2497, \
    QAP_1897, QAP_1898, QAP_2506, QAP_2508, QAP_2500, QAP_2779, QAP_2501_WIP, QAP_3484
from quod_qa.fx.fx_mm_rfq import QAP_1746
from quod_qa.fx.fx_taker_esp import QAP_833, QAP_1115, QAP_110, QAP_231, QAP_1591, QAP_492, QAP_105, QAP_851
from quod_qa.fx.fx_taker_rfq import QAP_6, QAP_564, QAP_565, QAP_566, QAP_567, QAP_568, QAP_569, QAP_570, QAP_571, \
    QAP_573, QAP_574, QAP_576, QAP_577, QAP_578, QAP_579, QAP_580, QAP_581, QAP_582, QAP_584, QAP_585, QAP_587, QAP_589, \
    QAP_590, QAP_591, QAP_593, QAP_594, QAP_595, QAP_597, QAP_598, QAP_599, QAP_600, QAP_601, QAP_602, QAP_604, QAP_605, \
    QAP_606, QAP_609, QAP_610, QAP_611, QAP_612, QAP_636, QAP_643, QAP_645, QAP_646, QAP_648, QAP_683, QAP_687, QAP_702, \
    QAP_708, QAP_709, QAP_710, QAP_714, QAP_718, QAP_741, QAP_751, QAP_842, QAP_847, QAP_848, QAP_849, QAP_850, QAP_982, \
    QAP_992, QAP_1585, QAP_1713, QAP_2514, QAP_2728, QAP_2729, QAP_2774, QAP_2826, QAP_2835, QAP_2847, \
    QAP_3589, QAP_575, QAP_592
from rule_management import RuleManager

from stubs import Stubs
from test_cases import QAP_1552
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
    return [rfq_quote, rfq_trade]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('ostronov tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 308"

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
        #

        # # Add scripts
        QAP_612.execute(report_id, session_id)
        # QAP_710.execute(report_id, session_id)

        rule_manager = RuleManager()
        rule_manager.print_active_rules()
        print('duration time = ' + str(datetime.now() - start))

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
