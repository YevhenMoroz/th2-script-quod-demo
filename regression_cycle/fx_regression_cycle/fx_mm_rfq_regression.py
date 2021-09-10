from quod_qa.fx.fx_mm_positions import QAP_2496
from quod_qa.fx.fx_mm_rfq import QAP_1537, QAP_1539, QAP_1540, QAP_1542, QAP_1545, QAP_1547, QAP_1548, QAP_1550, \
    QAP_1551, QAP_1562, QAP_1563, QAP_1746, QAP_1755, QAP_1970, QAP_1971, QAP_1972, QAP_1978, QAP_2055, QAP_2063, \
    QAP_2066, QAP_2089, QAP_2090, QAP_2103, QAP_2121, QAP_2483, QAP_2484, QAP_2486, QAP_2488, QAP_2489, QAP_2490, \
    QAP_2877, QAP_2878, QAP_2345, QAP_1552, QAP_2062, QAP_2091, QAP_2092, QAP_2101, QAP_2104, QAP_2105, QAP_2143, \
    QAP_2177, QAP_2294, QAP_2295, QAP_2296, QAP_2297, QAP_2353, QAP_2670, QAP_2866, QAP_2867, QAP_2868, QAP_2958, \
    QAP_3565, QAP_4223, QAP_4777, QAP_4748, QAP_2382
from quod_qa.fx.fx_mm_rfq.interpolation import QAP_3739, QAP_3689, QAP_3766, QAP_3747, QAP_3734, QAP_3805, QAP_4234, \
    QAP_3807, QAP_3850, QAP_3811, QAP_3851, QAP_3806
from quod_qa.fx.fx_mm_rfq.manual_intervention import QAP_3721
from quod_qa.fx.fx_mm_rfq.rejection import QAP_3720, QAP_3735
from quod_qa.fx.fx_mm_rfq.update_quod_settings import update_settings_and_restart_qs

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('FX_MM_RFQ', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    try:

        case_params = {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
            'Account': 'Iridium1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD9',
        }
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        # region Rejection
        update_settings_and_restart_qs("Rejection")
        QAP_3720.execute(report_id)
        QAP_3735.execute(report_id, session_id)
        # endregion

        # region Manual Intervention
        update_settings_and_restart_qs("Manual Intervention")
        QAP_3721.execute(report_id)
        # endregion

        # region Interpolation
        update_settings_and_restart_qs("Interpolation")
        QAP_3689.execute(report_id)
        QAP_3766.execute(report_id)
        QAP_3747.execute(report_id)
        QAP_3734.execute(report_id, session_id)
        QAP_3805.execute(report_id)
        QAP_4234.execute(report_id)
        QAP_3807.execute(report_id)
        QAP_3739.execute(report_id)
        QAP_3850.execute(report_id)
        QAP_3811.execute(report_id, session_id)
        QAP_3851.execute(report_id)
        QAP_3806.execute(report_id)
        # endregion

        # QAP_1552.execute(report_id)
        # QAP_1746.execute(report_id)
        # QAP_1755.execute(report_id)
        # QAP_1978.execute(report_id)
        # QAP_2089.execute(report_id)
        # QAP_2090.execute(report_id)
        # QAP_2091.execute(report_id)
        # QAP_2103.execute(report_id)
        # QAP_2177.execute(report_id)
        # QAP_2295.execute(report_id)
        # QAP_2297.execute(report_id)
        # QAP_2345.execute(report_id)
        # QAP_2353.execute(report_id)
        # QAP_3739.execute(report_id)
        # QAP_3565.execute(report_id)
        # QAP_2382.execute(report_id)
        # QAP_2103.execute(report_id)

        # QAP_1537.execute(report_id, case_params)
        # QAP_1539.execute(report_id, session_id)
        # QAP_1540.execute(report_id, case_params)
        # QAP_1542.execute(report_id, case_params)
        # QAP_1545.execute(report_id, case_params, session_id)
        # QAP_1547.execute(report_id, case_params, session_id)
        # QAP_1548.execute(report_id, case_params, session_id)
        # QAP_1550.execute(report_id, case_params, session_id)
        # QAP_1551.execute(report_id, case_params, session_id)
        # QAP_1562.execute(report_id, case_params, session_id)
        # QAP_1563.execute(report_id, case_params, session_id)
        # QAP_1970.execute(report_id, case_params, session_id)
        # QAP_1971.execute(report_id, case_params, session_id)
        # QAP_1972.execute(report_id, case_params, session_id)
        # QAP_2063.execute(report_id, case_params, session_id)
        # QAP_2066.execute(report_id, case_params, session_id)
        # QAP_2121.execute(report_id, case_params, session_id)
        # QAP_2055.execute(report_id, session_id)
        # QAP_2062.execute(report_id, session_id)
        #
        # QAP_2092.execute(report_id, session_id)
        # QAP_2101.execute(report_id, session_id)
        # QAP_2104.execute(report_id, session_id)
        # QAP_2105.execute(report_id, session_id)
        #
        # QAP_2143.execute(report_id, session_id)
        # QAP_2294.execute(report_id, session_id)
        # QAP_2296.execute(report_id, session_id)
        # QAP_2483.execute(report_id, session_id)
        # QAP_2484.execute(report_id, session_id)
        # QAP_2486.execute(report_id, session_id)
        # QAP_2488.execute(report_id, session_id)
        # QAP_2489.execute(report_id, session_id)
        # QAP_2490.execute(report_id, session_id)
        # QAP_2670.execute(report_id, session_id)
        # QAP_2866.execute(report_id, session_id)
        # QAP_2867.execute(report_id, session_id)
        # QAP_2868.execute(report_id, session_id)
        # QAP_2877.execute(report_id, session_id)
        # QAP_2878.execute(report_id, session_id)
        # QAP_2958.execute(report_id, session_id)
        #
        # QAP_4223.execute(report_id, session_id)
        # QAP_4777.execute(report_id, session_id)
        # QAP_4748.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        # close_fe(report_id, session_id)
        pass


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
