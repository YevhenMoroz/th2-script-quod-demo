from quod_qa.fx.fx_mm_rfq import QAP_1537, QAP_1539, QAP_1540, QAP_1542, QAP_1545, QAP_1547, QAP_1548, QAP_1550, \
    QAP_1551, QAP_1562, QAP_1563, QAP_1746, QAP_1755, QAP_1970, QAP_1971, QAP_1972, QAP_1978, QAP_2055, QAP_2063, \
    QAP_2066, QAP_2089, QAP_2090, QAP_2103, QAP_2121
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
    report_id = bca.create_event('FX MM RFQ regression', parent_id)
    session_id = set_session_id()
    try:
        Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
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

        QAP_1537.execute(report_id, case_params)
        QAP_1539.execute(report_id)
        QAP_1540.execute(report_id, case_params)
        QAP_1542.execute(report_id, case_params)
        QAP_1545.execute(report_id, case_params, session_id)
        QAP_1547.execute(report_id, case_params, session_id)
        QAP_1548.execute(report_id, case_params, session_id)
        QAP_1550.execute(report_id, case_params, session_id)
        QAP_1551.execute(report_id, case_params, session_id)
        QAP_1562.execute(report_id, case_params, session_id)
        QAP_1563.execute(report_id, case_params, session_id)
        QAP_1746.execute(report_id)
        QAP_1755.execute(report_id)
        QAP_1970.execute(report_id, case_params, session_id)
        QAP_1971.execute(report_id, case_params, session_id)
        QAP_1972.execute(report_id, case_params, session_id)
        QAP_2055.execute(report_id, session_id)
        QAP_2063.execute(report_id, case_params, session_id)
        QAP_2066.execute(report_id, case_params, session_id)
        QAP_2089.execute(report_id)
        QAP_2090.execute(report_id)
        QAP_2103.execute(report_id)
        QAP_2121.execute(report_id, case_params, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
