import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq.Basket import QAP_4648
from quod_qa.eq.Care import QAP_1012, QAP_1016, QAP_477, QAP_1014, QAP_1017, QAP_1022, QAP_1034, QAP_1045
from quod_qa.eq.Commissions import QAP_4535, QAP_3312
from quod_qa.eq.Counterpart import QAP_3503
from quod_qa.eq.DMA import QAP_2000, QAP_2548, QAP_2002, QAP_2008
from quod_qa.eq.PostTrade import QAP_3386, QAP_4334, QAP_3781, QAP_4462, QAP_4896, QAP_2614, QAP_3303, QAP_3338, \
    QAP_3333
from stubs import Stubs
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('ymoroz ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()
    try:
        QAP_1045.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
