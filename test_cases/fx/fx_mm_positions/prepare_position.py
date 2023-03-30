from time import sleep

from test_cases.fx.fx_wrapper.common_tools import clear_position, restart_pks


def prepare_position():
    clear_position()
    restart_pks()
    sleep(120)
