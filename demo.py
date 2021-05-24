import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq import MD_test_3, MD_test, TradingSession_test
from quod_qa.eq.Algo_Multilisted import QAP_1962, QAP_1965, QAP_1966, QAP_1963, QAP_1983, QAP_1984, QAP_1967, QAP_2068, \
    QAP_3134, QAP_2476, QAP_3059
from quod_qa.eq.Algo_TWAP import QAP_3119
from quod_qa.eq.Sorping import QAP_2409, QAP_2408
from rule_management import RuleManager
from stubs import Stubs

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban  tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        # QAP_1072.execute(report_id)
        # QAP_1965.execute(report_id)
        # QAP_1966.execute(report_id)
        # QAP_1962.execute(report_id)
        # QAP_1967.execute(report_id)
        # QAP_1983.execute(report_id)
        # QAP_1984.execute(report_id)
        # QAP_1963.execute(report_id)
        # QAP_2409.execute(report_id)
        # QAP_2068.execute(report_id)
        # QAP_3134.execute(report_id)
        # QAP_3119.execute(report_id)
        # TradingSession_test.execute(report_id)

        # QAP_2476.execute(report_id)
        # QAP_3134.execute(report_id)
        # QAP_2476.execute(report_id)
        QAP_3059.execute(report_id)
        # MD_test_3.execute(report_id)
        # MD_test.execute(report_id)
        # MD_test.execute(report_id)
        # rule_manager = RuleManager()
        # market_rule_1 = rule_manager.add_NewOrdSingle_Market("fix-bs-310-columbia", "XPAR_CLIENT1", "XPAR", False, 0, 20)
        # rm.remove_all_rules()
        # rule_manager.print_active_rules()
        # rm.add_NewOrdSingle_Market("fix-bs-310-columbia", "XPAR_CLIENT2", "XPAR", True, 100, 20.5)
        # rm.remove_all_rules()

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
