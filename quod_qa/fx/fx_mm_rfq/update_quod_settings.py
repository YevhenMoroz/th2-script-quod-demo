import time

from quod_qa.fx.fx_wrapper.common_tools import update_quod_settings, restart_component_on_back


def update_settings_and_restart_qs(setting_value: str):
    update_quod_settings(setting_value)
    restart_component_on_back()
    time.sleep(120)
