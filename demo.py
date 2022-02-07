import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from rule_management import RuleManager

from stubs import Stubs
from test_cases.fx.fx_mm_esp import QAP_2750, QAP_6148
from test_cases.fx.fx_mm_esp.QAP_1589 import QAP_1589
from test_cases.fx.fx_mm_rfq import QAP_3494
from test_cases.fx.fx_taker_rfq.QAP_564 import QAP_564
from test_cases.fx.fx_taker_rfq.QAP_565 import QAP_565
from test_cases.fx.fx_taker_rfq.QAP_566 import QAP_566
from test_cases.fx.fx_taker_rfq.QAP_568 import QAP_568
from test_cases.fx.fx_taker_rfq.QAP_569 import QAP_569
from test_cases.fx.fx_taker_rfq.QAP_570 import QAP_570
from test_cases.fx.fx_taker_rfq.QAP_571 import QAP_571
from test_cases.fx.fx_taker_rfq.QAP_573 import QAP_573
from test_cases.fx.fx_taker_rfq.QAP_574 import QAP_574
from test_cases.fx.fx_taker_rfq.QAP_575 import QAP_575
from test_cases.fx.fx_taker_rfq.QAP_576 import QAP_576
from test_cases.fx.fx_taker_rfq.QAP_578 import QAP_578
from test_cases.fx.fx_taker_rfq.QAP_579 import QAP_579
from test_cases.fx.fx_taker_rfq.QAP_580 import QAP_580
from test_cases.fx.fx_taker_rfq.QAP_581 import QAP_581
from test_cases.fx.fx_taker_rfq.QAP_582 import QAP_582
from test_cases.fx.fx_taker_rfq.QAP_584 import QAP_584
from test_cases.fx.fx_taker_rfq.QAP_585 import QAP_585
from test_cases.fx.fx_taker_rfq.QAP_587 import QAP_587
from test_cases.fx.fx_taker_rfq.QAP_589 import QAP_589
from test_cases.fx.fx_taker_rfq.QAP_590 import QAP_590
from test_cases.fx.fx_taker_rfq.QAP_591 import QAP_591
from test_cases.fx.fx_taker_rfq.QAP_593 import QAP_593
from test_cases.fx.fx_taker_rfq.QAP_594 import QAP_594
from test_cases.fx.fx_taker_rfq.QAP_595 import QAP_595
from test_cases.fx.fx_taker_rfq.QAP_597 import QAP_597
from test_cases.fx.fx_taker_rfq.QAP_598 import QAP_598
from test_cases.fx.fx_taker_rfq.QAP_599 import QAP_599
from test_cases.fx.fx_taker_rfq.QAP_6 import QAP_6
from test_cases.fx.fx_taker_rfq.QAP_600 import QAP_600
from test_cases.fx.fx_taker_rfq.QAP_601 import QAP_601
from test_cases.fx.fx_taker_rfq.QAP_602 import QAP_602
from test_cases.fx.fx_taker_rfq.QAP_604 import QAP_604
from test_cases.fx.fx_taker_rfq.QAP_606 import QAP_606
from test_cases.fx.fx_taker_rfq.QAP_609 import QAP_609
from test_cases.fx.fx_taker_rfq.QAP_610 import QAP_610
from test_cases.fx.fx_taker_rfq.QAP_611 import QAP_611
from test_cases.fx.fx_taker_rfq.QAP_643 import QAP_643
from test_cases.fx.fx_taker_rfq.QAP_645 import QAP_645
from test_cases.fx.fx_taker_rfq.QAP_646 import QAP_646
from test_cases.fx.fx_taker_rfq.QAP_648 import QAP_648
from test_cases.fx.fx_taker_rfq.QAP_702 import QAP_702
from test_cases.fx.fx_taker_rfq.QAP_709 import QAP_709

from test_framework.core.example_of_ideal_test_case_ui import QAP_Example
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, get_opened_fe, prepare_fe_2

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run

    report_id = bca.create_event("RNenakhov " + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    logging.getLogger().setLevel(logging.WARN)
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id()
    start_time = datetime.now()
    print(f"Start time :{start_time}")
    data_set = FxDataSet()

    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        # rm= RuleManager()
        # rm.remove_rule_by_id(15)
        # rm.add_fx_md_to("fix-fh-314-luna")
        # rm.print_active_rules()
        # send_md.execute(report_id, 1.18123, 1.18223)
        # QAP_6(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_564(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_565(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_566(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_568(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_569(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_570(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_571(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_573(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_574(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_575(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_576(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_578(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_579(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_580(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_581(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_582(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_584(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_585(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_587(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_589(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_590(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_591(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_593(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_594(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_595(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_597(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_598(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_599(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_600(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_601(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_602(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_604(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_606(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_609(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_610(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_611(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_643(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_645(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_646(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_702(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_709(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        print(f"Duration is {datetime.now() - start_time}")
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
