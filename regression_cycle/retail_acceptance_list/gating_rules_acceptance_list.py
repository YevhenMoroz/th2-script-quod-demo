import os

from th2_grpc_hand import rhbatch_pb2

from test_cases.RET.Gating_Rules import QAP_4280, QAP_4282, QAP_4288, QAP_4307
from test_framework.old_wrappers.ret_wrappers import enable_gating_rule, disable_gating_rule
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    # Create session for DMA tests
    session_id_dma = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID

    # Create session for Care tests
    session_id_care = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID

    # Create events for each REST API requests
    report_id = bca.create_event('Gating Rules', parent_id)
    case_id_enable_rule_dma = bca.create_event("Enable Gating Rule for DMA", report_id)
    case_id_disable_rule_dma = bca.create_event("Disable Gating Rule for DMA", report_id)
    case_id_enable_rule_care = bca.create_event("Enable Gating Rule for Care", report_id)
    case_id_disable_rule_care = bca.create_event("Disable Gating Rule for Care", report_id)

    # Default data for login
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    try:
        # DMA block
        # Send RETS API request for Enable the gating rule - QAP-4307(Gr_for_DMA)
        enable_gating_rule(case_id_enable_rule_dma, gating_rule_id=1)

        # Open FE using session_id_dma
        prepare_fe(report_id, session_id_dma, work_dir, username, password)

        QAP_4280.execute(session_id_dma, report_id)
        QAP_4307.execute(session_id_dma, report_id)

        # Drop DMA session
        close_fe(report_id, session_id_dma)

        # Send REST API request for Disable the gating rule - QAP-4307(Gr_for_DMA)
        disable_gating_rule(case_id_disable_rule_dma, gating_rule_id=1)

        # Care block
        # Send REST API request for Enable the gating rule - QAP-4282(Gr_for_Care)
        enable_gating_rule(case_id_enable_rule_care, gating_rule_id=3)

        # Open FE using session_id_care
        prepare_fe(report_id, session_id_care, work_dir, username, password)

        QAP_4282.execute(session_id_care, report_id)
        QAP_4288.execute(session_id_care, report_id)

        # Send REST API request for Disable the gating rule - QAP-4282(Gr_for_Care)
        disable_gating_rule(case_id_disable_rule_care, gating_rule_id=3)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
