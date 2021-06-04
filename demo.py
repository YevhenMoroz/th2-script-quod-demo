import logging
import os
from datetime import datetime
from os import listdir
from os.path import isfile, join

from custom import basic_custom_actions as bca
from quod_qa.eq.Algo_Multilisted import *
from quod_qa.eq import MD_test_3, MD_test
from quod_qa.eq.Algo_Multilisted import QAP_1810, QAP_3028, QAP_3058, QAP_3059, QAP_3134, QAP_3429, QAP_1951, QAP_1952, \
    QAP_1953, QAP_1954, QAP_1957, QAP_1958, QAP_1959, QAP_1960, QAP_1961, QAP_1962, QAP_1963, QAP_1965, QAP_1966, \
    QAP_1967, QAP_1968, QAP_1969, QAP_1974, QAP_1975, QAP_1976, QAP_1977, QAP_1979, QAP_1980, QAP_1983, QAP_1984, \
    QAP_1985, QAP_1988, QAP_1990, QAP_1992, QAP_1995, QAP_1996, QAP_1997, QAP_1998, QAP_2068, QAP_2476, QAP_2857, \
    QAP_2982, QAP_3019, QAP_3021, QAP_3022, QAP_3025, QAP_3027
from quod_qa.eq.Algo_PercentageVolume import QAP_3062
from quod_qa.eq.Algo_TWAP import QAP_3122
from quod_qa.eq.Sorping import QAP_2409
from rule_management import RuleManager
from stubs import Stubs
from test_cases import QAP_1641

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # QAP_3122.execute(report_id)
        # QAP_3058.execute(report_id)
        # QAP_3429.execute(report_id)
        # MD_test_3.execute(report_id)
        # MD_test.execute(report_id)
        # rm = RuleManager()
        # rm.remove_all_rules()
        # rm.print_active_rules()

        # rm.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-310-columbia", "XPAR_CLIENT1", "XPAR", 20)
        # rm.add_OrderCancelRequest("fix-bs-310-columbia", "XPAR_CLIENT1","XPAR", True)
        # rm.add_NewOrdSingle_IOC("fix-bs-310-columbia", "XPAR_CLIENT1","XPAR", False, 100, 40)
        # rm.add_NewOrdSingle_IOC("fix-bs-310-columbia", "XPAR_CLIENT1","XPAR", False, 100, 20)


        # onlyfiles = [f for f in listdir() if isfile(join(, f))]
        # arr = os.listdir('C:\\QA\\Git\\th2-script-quod-demo-schema\\quod_qa\\eq\\Algo_Multilisted')
        #
        #
        # for i, file in enumerate(arr):
        #     arr[i] = file[:-3]
        #     filepath = os.path.join(a_directory, filename)

        # # region Multilisting
        # QAP_1810.execute(report_id)
        # QAP_1951.execute(report_id)
        # QAP_1952.execute(report_id)
        # QAP_1953.execute(report_id)
        # QAP_1954.execute(report_id)
        # QAP_1957.execute(report_id)
        # QAP_1958.execute(report_id)
        # QAP_1959.execute(report_id)
        # QAP_1960.execute(report_id)
        # QAP_1961.execute(report_id)
        # QAP_1962.execute(report_id)
        # QAP_1963.execute(report_id)
        # QAP_1965.execute(report_id)
        # QAP_1966.execute(report_id)
        # QAP_1967.execute(report_id)
        # QAP_1968.execute(report_id)
        # QAP_1969.execute(report_id)
        # QAP_1974.execute(report_id)
        # QAP_1975.execute(report_id)
        # QAP_1976.execute(report_id)
        # QAP_1977.execute(report_id)
        # QAP_1979.execute(report_id)
        # QAP_1980.execute(report_id)
        # QAP_1983.execute(report_id)
        # QAP_1984.execute(report_id)
        # QAP_1985.execute(report_id)
        # QAP_1988.execute(report_id)
        # QAP_1990.execute(report_id)
        # QAP_1992.execute(report_id)
        # QAP_1995.execute(report_id)
        # QAP_1996.execute(report_id)
        # QAP_1997.execute(report_id)
        # QAP_1998.execute(report_id)
        # QAP_2068.execute(report_id)
        # QAP_2476.execute(report_id)
        # QAP_2857.execute(report_id)
        # QAP_2982.execute(report_id)
        # QAP_3019.execute(report_id)
        # QAP_3021.execute(report_id)
        # QAP_3022.execute(report_id)
        # QAP_3025.execute(report_id)
        # QAP_3027.execute(report_id)
        # QAP_3028.execute(report_id)
        # QAP_3058.execute(report_id)
        # QAP_3059.execute(report_id)
        # QAP_3134.execute(report_id)

        # QAP_2409.execute(report_id)
        # # endregion
        # rm = RuleManager()
        # rm.remove_all_rules()
        # rm.print_active_rules()
        # QAP_3429.execute(report_id)
        # QAP_1641.execute(report_id)
        QAP_3062.execute(report_id)




    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()