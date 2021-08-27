from quod_qa.fx.fx_mm_rfq import QAP_2103, QAP_3565, QAP_2382
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.utils import set_session_id

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
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)

        case_params = {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
            'Account': 'Iridium1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD9',
        }

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
        QAP_3565.execute(report_id)
        QAP_2382.execute(report_id)
        QAP_2103.execute(report_id)

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
