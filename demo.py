import logging

from datetime import datetime

from custom import basic_custom_actions as bca

from stubs import Stubs

# from rule_management import RuleManager
# from quod_qa.fx import fix_demo, ui_tests

from quod_qa.eq.DMA import QAP_4297, QAP_4304, QAP_4310, QAP_4325, QAP_4311, QAP_4314, QAP_4291, QAP_4322, QAP_4300, \
    QAP_4280, QAP_4307
from quod_qa.eq.Care import QAP_4306, QAP_4288, QAP_4282, QAP_4303

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
        # QAP_4297.execute(report_id)
        # QAP_4304.execute(report_id)
        # QAP_4310.execute(report_id)
        # QAP_4325.execute(report_id)
        # QAP_4311.execute(report_id)
        # QAP_4314.execute(report_id)
        # QAP_4306.execute(report_id)
        # QAP_4291.execute(report_id)
        # QAP_4322.execute(report_id)
        # QAP_4300.execute(report_id)
        # QAP_4280.execute(report_id)
        # QAP_4307.execute(report_id)
        # QAP_4288.execute(report_id)
        # QAP_4282.execute(report_id)
        QAP_4303.execute(report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
