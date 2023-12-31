import time

from test_cases.fx.fx_wrapper.common_tools import update_quod_settings, restart_qs_rfq_fix_th2


def update_settings_and_restart_qs(setting_value: str, timeout: int = 180):
    update_quod_settings(setting_value)
    restart_qs_rfq_fix_th2()
    time.sleep(timeout)
    print("\nComponent QS_RFQ_FIX_TH2 started\n")
