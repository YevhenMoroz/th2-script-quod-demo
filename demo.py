import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_autohedging import QAP_2292, QAP_2291, QAP_2265, QAP_3902, QAP_2470, QAP_2113, QAP_2250, QAP_2252, \
    QAP_2251, QAP_3819, AH_Precondition, QAP_3147, QAP_2322, QAP_3039, QAP_3082, import_AH_layout, QAP_2293, QAP_4149
from quod_qa.fx.fx_mm_rfq import QAP_4748, QAP_4223, QAP_2103, QAP_2382, QAP_2296, QAP_2101, QAP_2091, QAP_5345, \
    QAP_2055, QAP_2958, QAP_4777, QAP_4509, QAP_5814
from quod_qa.fx.fx_mm_esp import QAP_3661, QAP_4016, QAP_2750, QAP_4094, QAP_2844, QAP_3394, QAP_1511, QAP_1589, \
    QAP_2035, QAP_2556, QAP_4794, QAP_1599, QAP_3563
from quod_qa.fx.fx_mm_rfq.interpolation import QAP_3734, QAP_3739, QAP_3689, QAP_3747
from MyFiles import SendMD
from quod_qa.fx.fx_taker_esp import QAP_2373, QAP_2761, QAP_2812, QAP_4768, QAP_1591, QAP_105, QAP_3742, QAP_4673, \
    QAP_4677
from quod_qa.fx.fx_taker_rfq import QAP_2836
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe_2, get_opened_fe

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


def rule_check():
    rm = RuleManager()
    rm.print_active_rules()
    # rm.print_active_rules_sim_test()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('aleksey tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()
    # rules = rule_creation()
    start = datetime.now()
    print(f'start time = {start}')
    # rule_check()
    try:
        # pass
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)
        # import_AH_layout.execute(report_id, session_id)
        # QAP_3082.execute(report_id, session_id)
        # QAP_2265.execute(report_id, session_id)
        # QAP_2296.execute(report_id, session_id)
        # QAP_2293.execute(report_id, session_id)
        # QAP_4149.execute(report_id, session_id)
        QAP_5814.execute(report_id)

        # region my test files
        SendMD.execute(report_id)
        # send_rfq.execute(report_id)
        # Test.execute(report_id, session_id)
        # ui_tests.execute(report_id, session_id)
        # StringThing.execute()
        # MyTest.execute(report_id)
        # AH_Precondition.execute(report_id)
        # import_AH_layout.execute(report_id, session_id)
        # endregion

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)
        print('duration time = ' + str(datetime.now() - start))


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
