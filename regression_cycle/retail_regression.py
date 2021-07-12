from regression_cycle.retail_regression_cycle import care_regression, dma_regression, login_regression, \
    risk_limits_regression, twap_regression
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca


from win_gui_modules.utils import prepare_fe, set_session_id


def test_run(parent_id=None):
    session_id = set_session_id()
    report_id = bca.create_event('Retail regression_cycle', parent_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    try:
        if not Stubs.frontend_is_open:
            login_regression.test_run(session_id, report_id)
        prepare_fe(report_id, session_id, work_dir, username, password)
        care_regression.test_run(session_id, report_id)
        dma_regression.test_run(session_id, report_id)
        risk_limits_regression.test_run(session_id, report_id)
        twap_regression.test_run(session_id, report_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()