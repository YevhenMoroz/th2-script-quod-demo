from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle.kepler_sors_regression_cycle import kepler_sors_iceberg_regression, kepler_sors_sorping_regression, kepler_sors_synthminqty_regression, kepler_sors_mpdark_dark_phase_regression, kepler_sors_mpdark_LIS_dark_phase_regression, \
    kepler_sors_mpdark_other_regression, kepler_sors_multiple_emulation_regression, kepler_iceberg_check_party_info, kepler_iceberg_multiday_phase, kepler_custom_tags, kepler_synthetic_tif, kepler_multiple_emulation_additional, kepler_multilisting, kepler_iceberg_modify, \
    kepler_instrument_identification, kepler_mic_identification, kepler_sors_mpdark_round_robin

import os
import pathlib

print("OS")
print(os.getcwd())

print("absolute path")
print(pathlib.Path(__file__).parent.resolve())