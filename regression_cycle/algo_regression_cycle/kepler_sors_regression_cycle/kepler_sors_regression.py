from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle.kepler_sors_regression_cycle import kepler_sors_iceberg_regression, kepler_sors_sorping_regression, kepler_sors_synthminqty_regression, kepler_sors_mpdark_dark_phase_regression, kepler_sors_mpdark_LIS_dark_phase_regression, \
    kepler_sors_mpdark_other_regression, kepler_sors_multiple_emulation_regression, kepler_iceberg_check_party_info, kepler_iceberg_multiday_phase, kepler_custom_tags, kepler_synthetic_tif, kepler_multiple_emulation_additional, kepler_multilisting, kepler_iceberg_modify, \
    kepler_instrument_identification, kepler_mic_identification, kepler_sors_mpdark_round_robin
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    try:
        # Generation id and time for test run
        report_id = bca.create_event('Kepler SORS regression_cycle')
        logger.info(f"Root event was created (id = {report_id.id})")

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text

        # if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
        kepler_sors_iceberg_regression.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        # kepler_sors_mpdark_dark_phase_regression.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        # kepler_sors_mpdark_other_regression.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        kepler_sors_sorping_regression.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Synth_min_qty']").attrib["run"]):
        kepler_sors_synthminqty_regression.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Multiple_emulation']").attrib["run"]):
        kepler_sors_multiple_emulation_regression.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
        kepler_iceberg_check_party_info.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
        kepler_iceberg_multiday_phase.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
        kepler_custom_tags.test_run(parent_id=report_id, version=version)
        # # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        kepler_synthetic_tif.test_run(parent_id=report_id, version=version)
        # # if eval(root.find(".//component[@name='Multiple_emulation']").attrib["run"]):
        kepler_multiple_emulation_additional.test_run(parent_id=report_id, version=version)
        # # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        kepler_multilisting.test_run(parent_id=report_id, version=version)
        # # if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
        kepler_iceberg_modify.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        kepler_instrument_identification.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        kepler_mic_identification.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        # kepler_sors_mpdark_round_robin.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        # kepler_sors_mpdark_LIS_dark_phase_regression.test_run(parent_id=report_id, version=version)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()