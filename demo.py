import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.eq import MD_test, MD_test_3
from quod_qa.eq.Algo_Multilisted import  QAP_3058
from quod_qa.eq.Algo_Stop import QAP_4513
from quod_qa.eq.Algo_TWAP import QAP_4563
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe, close_fe

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
        # QAP_3058.execute(report_id)
        #region TWAP tests
        #endregion
        #region multilisting tests
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
        # QAP_1986.execute(report_id)
        # QAP_1988.execute(report_id)
        # QAP_1990.execute(report_id)
        # QAP_1992.execute(report_id)
        # QAP_1995.execute(report_id)
        # QAP_1996.execute(report_id)
        # QAP_1997.execute(report_id)
        # QAP_1998.execute(report_id)
        # QAP_2982.execute(report_id)
        # QAP_3019.execute(report_id)
        # QAP_3021.execute(report_id)
        # QAP_3022.execute(report_id)
        # QAP_3025.execute(report_id)
        # QAP_3027.execute(report_id)
        # QAP_3028.execute(report_id)
        # QAP_3058.execute(report_id)
        #endregion


        # rm = RuleManager()
        # rm.print_active_rules()
        # rm.remove_all_rules()
        # rm.print_active_rules()

        # rm = RuleManager()
        # rm.add_NewOrdSingleExecutionReportPendingAndNew("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", 18.995)
        # rm.add_NewOrdSingleExecutionReportPendingAndNew("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", 19.99)
        # rm.add_NewOrdSingleExecutionReportPendingAndNew("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", 20)
        # rm.add_NewOrdSingleExecutionReportPendingAndNew("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", 21)
        # rm.add_NewOrdSingleExecutionReportTrade("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", 18.995, 100, 0)
        # rm.add_OrderCancelRequest("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", True)
        # rm.add_NewOrdSingle_IOC("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", True, 400, 19.99)
        # rm.print_active_rules()

        # MD_test.execute(report_id)
        # MD_test_3.execute(report_id)
        # rm.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-310-columbia", "XPAR_CLIENT3", "XPAR", 40)

        QAP_4563.execute(report_id)

    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__': 
    logging.basicConfig()
    test_run()
    Stubs.factory.close()