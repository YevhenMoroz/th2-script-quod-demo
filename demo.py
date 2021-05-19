import logging
from datetime import datetime
from custom import basic_custom_actions as bca
<<<<<<< HEAD
from quod_qa.eq.Algo_Iceberg import QAP_3055, QAP_3054
from quod_qa.eq.Algo_Multilisted import QAP_1988, QAP_1965, QAP_1985, QAP_1979, QAP_1977, QAP_1998, QAP_1974, QAP_1968, QAP_1969, QAP_1976, QAP_1975, QAP_1961, QAP_1960, QAP_1980, QAP_1959, QAP_1810, QAP_1952, QAP_1997, QAP_1996, QAP_1995, QAP_1992, QAP_2857, QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027,QAP_1951, QAP_1990, QAP_3028
from quod_qa.eq.Algo_TWAP import QAP_1318, QAP_3121, QAP_3120
from rule_management import RuleManager
from stubs import Stubs
from MD_SOR import md
=======
from quod_qa.fx import fix_demo, ui_tests
from quod_qa.fx.fx_taker_rfq import QAP_636
from rule_management import RuleManager
from stubs import Stubs
from test_cases import QAP_638
from quod_qa.eq.Care import QAP_1072
>>>>>>> origin/mziuban_c3

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
<<<<<<< HEAD
    report_id = bca.create_event('FiLL tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        #md(report_id)
        QAP_1965.execute(report_id)
    except Exception:
        logging.error("Error execution",exc_info=True)
=======
    report_id = bca.create_event(' vskulinec  tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        QAP_1072.execute(report_id)
        test_cases =  {
                'case_id': bca.create_event_id(),
                'TraderConnectivity': 'gtwquod5-fx',
                'Account': 'MMCLIENT1',
                'SenderCompID': 'QUODFX_UAT',
                'TargetCompID': 'QUOD5',
                }

        # rm = RuleManager()
        # # rm.remove_rules_by_id_range(5,150)
        # # rm.add_RFQ('fix-fh-fx-rfq')
        # # rm.add_TRFQ('fix-fh-fx-rfq')
        # # rm.print_active_rules()
        # # ui_tests.execute(report_i)
        # start = datetime.now()
        # print(f'start time = {start}')
        #
        # # fix_demo.execute(report_id,test_cases)
        # ui_tests.execute(report_id)
        # # QAP_1520.TestCase(report_id).execute()
        # # QAP_636.execute(report_id)
        # print("1 - done")
        # print('duration time = ' + str(datetime.now() - start), str(report_id))inec



    except Exception:
        logging.error("Error execution", exc_info=True)

>>>>>>> origin/mziuban_c3

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
