import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.eq import MD_test_3, MD_test
from rule_management import RuleManager

from stubs import Stubs
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False

channels = dict()


def prepare_fe(case_id, session_id):
    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
        # ,
        #          fe_dir='qf_trading_fe_folder_308',
        #          fe_user='qf_trading_fe_user_308',
        #          fe_pass='qf_trading_fe_password_308')
    else:
        get_opened_fe(case_id, session_id)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    Stubs.frontend_is_open = True
    try:


        # MD_test_3.execute(report_id)
        # MD_test.execute(report_id)

        # params = {
        #     "OrderID": "test_1",
        #     "ExecID": "test_1",
        #     "CumQty": "0",
        #     "ExecType": "A",
        #     "OrdStatus": "A",
        #     "AvgPx": "0",
        #     "Text": "Pending New status",
        #     "LeavesQty": 10,
        #     "Price": 20,
        #     "Account": "XPAR_CLIENT1",
        #     "ExDestination": "XPAR",
        #     "TransactTime": datetime.utcnow().isoformat(),
        #     "Side": "1",
        #     "ClOrdID": "123456",
        #     "OrdType": "2",
        #     "OrderQty": "100",
        #     "TimeInForce": "0",
        #     "OrigClOrdID": "123456"
        # }
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send ExecutionReport',
        #     "fix-buy-side-316-ganymede",
        #     report_id,
        #     message_to_grpc('ExecutionReport', params, "fix-buy-side-316-ganymede")
        # ))
        rm = RuleManager()
        rm.add_NewOrderSingle_ExecutionReport_Reject("fix-buy-side-316-ganymede", "XPAR_CLIENT1", "XPAR", 20)
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
