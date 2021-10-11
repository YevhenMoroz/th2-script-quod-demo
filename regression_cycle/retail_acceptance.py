from regression_cycle.retail_acceptance_list import care_acceptance_list, dma_acceptance_list, iceberg_acceptance_list,\
    gating_rules_acceptance_list, login_acceptance_list, multilisted_acceptance_list, risk_limits_acceptance_list, \
    twap_acceptance_list, washbook_acceptance_list, benchmark_acceptance_list

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from quod_qa.wrapper.ret_wrappers import close_fe
from win_gui_modules.utils import prepare_fe, set_session_id


def test_run(parent_id=None):
    session_id = set_session_id()
    report_id = bca.create_event('Retail Acceptance', parent_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    try:
        if not Stubs.frontend_is_open:
            login_acceptance_list.test_run(session_id, report_id)
        prepare_fe(report_id, session_id, work_dir, username, password)
        care_acceptance_list.test_run(session_id, report_id)
        dma_acceptance_list.test_run(session_id, report_id)
        risk_limits_acceptance_list.test_run(session_id, report_id)
        iceberg_acceptance_list.test_run(session_id, report_id)
        multilisted_acceptance_list.test_run(session_id, report_id)
        twap_acceptance_list.test_run(session_id, report_id)
        benchmark_acceptance_list.test_run(session_id, report_id)
        washbook_acceptance_list.test_run(session_id, report_id)
        # close_fe(report_id, session_id)
        # gating_rules_acceptance_list.test_run(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()