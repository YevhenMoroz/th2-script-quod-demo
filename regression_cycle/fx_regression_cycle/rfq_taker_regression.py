from test_cases.fx.fx_taker_rfq import QAP_567, QAP_577, QAP_593,\
    QAP_594, QAP_595, QAP_597,\
    QAP_598, QAP_592, QAP_599, QAP_600, QAP_601, QAP_602, QAP_604, QAP_605, QAP_606, QAP_609, QAP_610, QAP_611, \
    QAP_612, QAP_636, QAP_643, QAP_645, QAP_646, QAP_648, QAP_683, QAP_687, QAP_702, QAP_708, QAP_709, QAP_710, \
    QAP_714, QAP_718, QAP_741, QAP_751, QAP_842, QAP_847, QAP_849, QAP_850, QAP_982, QAP_992, QAP_1585, QAP_1713,\
    QAP_2419, QAP_2514, QAP_2728, QAP_2729, QAP_2774, QAP_2826, QAP_2835, QAP_2847, QAP_3589, QAP_2836, \
    import_rfq_taker_layout, QAP_3048
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
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
from test_cases.fx.fx_taker_rfq.QAP_6 import QAP_6
from test_cases.fx.fx_taker_rfq.QAP_848 import QAP_848
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.import_layouts.layout_loader import LayoutLoader

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()
data_set = FxDataSet()


def test_run(parent_id=None):
    report_id = bca.create_event('RFQ Taker regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        LayoutLoader(report_id, session_id).import_layout("rfq_taker_layout.xml", "fx")

        QAP_6(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_564(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_565(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_566(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_567.execute(report_id, session_id)
        QAP_568(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_569(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_570(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_571(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_573(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_574(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_575(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_576(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_577.execute(report_id, session_id)
        QAP_578(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_579(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_580(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_581(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_582(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_584(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_585(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_587(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_589(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_590(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_591(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_592.execute(report_id, session_id)
        QAP_593.execute(report_id, session_id)
        QAP_594.execute(report_id, session_id)
        QAP_595.execute(report_id, session_id)
        QAP_597.execute(report_id, session_id)
        QAP_598.execute(report_id, session_id)
        QAP_599.execute(report_id, session_id)
        QAP_600.execute(report_id, session_id)
        QAP_601.execute(report_id, session_id)
        QAP_602.execute(report_id, session_id)
        QAP_604.execute(report_id, session_id)
        QAP_605.execute(report_id, session_id)
        QAP_606.execute(report_id, session_id)
        QAP_609.execute(report_id, session_id)
        QAP_610.execute(report_id, session_id)
        QAP_611.execute(report_id, session_id)
        QAP_612.execute(report_id, session_id)
        QAP_636.execute(report_id, session_id)
        QAP_643.execute(report_id, session_id)
        QAP_645.execute(report_id, session_id)
        QAP_646.execute(report_id, session_id)
        QAP_648.execute(report_id, session_id)
        QAP_683.execute(report_id, session_id)
        QAP_687.execute(report_id, session_id)
        QAP_702.execute(report_id, session_id)

        QAP_709.execute(report_id, session_id)
        QAP_710.execute(report_id, session_id)
        QAP_714.execute(report_id, session_id)
        QAP_718.execute(report_id, session_id)
        QAP_741.execute(report_id, session_id)
        QAP_751.execute(report_id, session_id)
        QAP_842.execute(report_id, session_id)
        QAP_847.execute(report_id, session_id)
        QAP_848(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        QAP_849.execute(report_id, session_id)
        QAP_850.execute(report_id, session_id)
        QAP_982.execute(report_id, session_id)
        QAP_992.execute(report_id, session_id)
        QAP_1585.execute(report_id, session_id)
        QAP_1713.execute(report_id, session_id)
        QAP_2419.execute(report_id, session_id)
        QAP_2514.execute(report_id, session_id)
        QAP_2728.execute(report_id, session_id)
        QAP_2729.execute(report_id, session_id)
        QAP_2774.execute(report_id, session_id)
        QAP_2826.execute(report_id, session_id)
        QAP_2835.execute(report_id, session_id)
        QAP_2836.execute(report_id, session_id)
        QAP_2847.execute(report_id, session_id)
        QAP_3048.execute(report_id, session_id)
        QAP_3589.execute(report_id, session_id)
        # QAP_708.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
