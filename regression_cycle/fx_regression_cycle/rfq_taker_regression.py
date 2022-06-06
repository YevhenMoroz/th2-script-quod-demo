from test_cases.fx.fx_taker_rfq import QAP_567, QAP_577, QAP_605, QAP_612, QAP_636, QAP_683, QAP_687, QAP_708, \
    QAP_718, QAP_1585, QAP_2419, QAP_2847, QAP_3589, QAP_2836, \
    QAP_3048
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_taker_rfq.QAP_1713 import QAP_1713
from test_cases.fx.fx_taker_rfq.QAP_2514 import QAP_2514
from test_cases.fx.fx_taker_rfq.QAP_2728 import QAP_2728
from test_cases.fx.fx_taker_rfq.QAP_2729 import QAP_2729
from test_cases.fx.fx_taker_rfq.QAP_2774 import QAP_2774
from test_cases.fx.fx_taker_rfq.QAP_2826 import QAP_2826
from test_cases.fx.fx_taker_rfq.QAP_2835 import QAP_2835
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
from test_cases.fx.fx_taker_rfq.QAP_710 import QAP_710
from test_cases.fx.fx_taker_rfq.QAP_714 import QAP_714
from test_cases.fx.fx_taker_rfq.QAP_741 import QAP_741
from test_cases.fx.fx_taker_rfq.QAP_751 import QAP_751
from test_cases.fx.fx_taker_rfq.QAP_842 import QAP_842
from test_cases.fx.fx_taker_rfq.QAP_847 import QAP_847
from test_cases.fx.fx_taker_rfq.QAP_848 import QAP_848
from test_cases.fx.fx_taker_rfq.QAP_849 import QAP_849
from test_cases.fx.fx_taker_rfq.QAP_850 import QAP_850
from test_cases.fx.fx_taker_rfq.QAP_982 import QAP_982
from test_cases.fx.fx_taker_rfq.QAP_992 import QAP_992
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.import_layouts.layout_loader import LayoutLoader

from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('RFQ Taker regression', parent_id)
    session_id = set_session_id()
    configuration = ComponentConfiguration("RFQ_Taker")
    try:

        LayoutLoader(report_id, session_id).import_layout("rfq_taker_layout.xml", "fx")

        QAP_6(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_564(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_565(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_566(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_567.execute(report_id, session_id)
        QAP_568(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_569(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_570(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_571(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_573(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_574(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_575(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_576(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_577.execute(report_id, session_id)
        QAP_578(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_579(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_580(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_581(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_582(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_584(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_585(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_587(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_589(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_590(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_591(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_592.execute(report_id, session_id)
        QAP_593(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_594(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_595(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_597(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_598(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_599(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_600(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_601(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_602(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_604(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_605.execute(report_id, session_id)
        QAP_606(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_609(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_610(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_611(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_612.execute(report_id, session_id)
        QAP_636.execute(report_id, session_id)
        QAP_643(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_645(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_646(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_648(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_683.execute(report_id, session_id)
        QAP_687.execute(report_id, session_id)
        QAP_702(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_708.execute(report_id, session_id)
        QAP_709(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_710(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_714(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_718.execute(report_id, session_id)
        QAP_741(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_751(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_842(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_847(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_848(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_849(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_850(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_982(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_992(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_1585.execute(report_id, session_id)
        QAP_1713(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2419.execute(report_id, session_id)
        QAP_2514(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2728(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2729(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2774(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2826(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2835(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_2836.execute(report_id, session_id)
        # QAP_2847.execute(report_id, session_id)
        # QAP_3048.execute(report_id, session_id)
        # QAP_3589.execute(report_id, session_id)
        # QAP_708.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
