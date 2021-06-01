import logging
from datetime import datetime
from custom import basic_custom_actions as bca
# from quod_qa.fx import fix_demo, ui_tests
# from rule_management import RuleManager
from stubs import Stubs
from quod_qa.eq.DMA import RIN_1151
# from quod_qa.eq.DMA import RIN_4040
# from quod_qa.eq.DMA import RIN_1144
# from quod_qa.eq.DMA import RIN_1141

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(' i.kobyliatskyi  tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        RIN_1151.execute(report_id)
        # RIN_1147.execute(report_id)
        # RIN_1144.execute(report_id)
        # RIN_1141.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
