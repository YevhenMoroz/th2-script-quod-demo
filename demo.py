import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_rfq import QAP_4748, QAP_4223, QAP_2103, QAP_2382, QAP_2296, QAP_2101, QAP_2091, QAP_5345
from quod_qa.fx.fx_mm_esp import QAP_3661, QAP_4016, QAP_2750, QAP_4094
from quod_qa.fx.fx_mm_rfq.interpolation import QAP_3734, QAP_3739, QAP_3689
from MyFiles import MyTest, SendMD, Test, StringThing, send_rfq
from quod_qa.fx.fx_taker_esp import QAP_2373, QAP_2761
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
    rm.print_active_rules_sim_test()


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
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        # QAP_1591.execute(report_id, session_id)
        # QAP_105.execute(report_id, session_id)
        # QAP_1511.execute(report_id, session_id)
        # QAP_1589.execute(report_id, session_id)
        # QAP_2055.execute(report_id, session_id)
        # QAP_3742.execute(report_id, session_id)
        # QAP_4673.execute(report_id, session_id)
        # QAP_4677.execute(report_id, session_id)
        # QAP_2113.execute(report_id, session_id)
        # QAP_2250.execute(report_id, session_id)
        # QAP_2252.execute(report_id, session_id)
        # QAP_2035.execute(report_id, session_id)
        # QAP_2556.execute(report_id, session_id)
        # QAP_4768.execute(report_id, session_id)
        # QAP_4794.execute(report_id, session_id)
        # QAP_4748.execute(report_id, session_id)
        # QAP_2958.execute(report_id, session_id)
        # QAP_2251.execute(report_id, session_id)
        # QAP_4777.execute(report_id, session_id)
        # QAP_4223.execute(report_id, session_id)
        # QAP_3739.execute(report_id)
        # QAP_3734.execute(report_id, session_id)
        # QAP_3689.execute(report_id)
        # QAP_2103.execute(report_id)
        # QAP_2382.execute(report_id)
        # QAP_3661.execute(report_id, session_id)
        # QAP_4016.execute(report_id, session_id)
        # QAP_2296.execute(report_id, session_id)
        # QAP_2101.execute(report_id, session_id)
        # QAP_2373.execute(report_id, session_id)
        # QAP_2750.execute(report_id)
        # QAP_4094.execute(report_id)
        # QAP_2091.execute(report_id)
        # QAP_5345.execute(report_id)
        QAP_2761.execute(report_id, session_id)


        # region my test files
        # SendMD.execute(report_id)
        # send_rfq.execute(report_id)
        # Test.execute(report_id)
        # ui_tests.execute(report_id, session_id)
        # StringThing.execute()
        # MyTest.execute(report_id, session_id)
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
