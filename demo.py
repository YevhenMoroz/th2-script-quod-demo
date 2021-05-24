import logging
from datetime import datetime
from custom import basic_custom_actions as bca

from stubs import Stubs

#from quod_qa.eq.DMA import RIN_244
from quod_qa.eq.DMA import RIN_258

from quod_qa.eq.DMA import RIN_1142
from quod_qa.eq.DMA import RIN_1143
from quod_qa.eq.DMA import RIN_1145
#from quod_qa.eq.DMA import RIN_1146

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(' irovchak  tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        #RIN_244.execute(report_id)
        RIN_258.execute(report_id)
        #RIN_1142.execute(report_id)
        #RIN_1143.execute(report_id)
        #RIN_1145.execute(report_id)
        #RIN_1146.execute(report_id)
        test_cases =  {
                'case_id': bca.create_event_id(),
                'TraderConnectivity': 'gtwquod5-fx',
                'Account': 'MMCLIENT1',
                'SenderCompID': 'QUODFX_UAT',
                'TargetCompID': 'QUOD5',
                }
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

