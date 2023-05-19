import time
from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle.kepler_sors_regression_cycle.kepler_change_configs_tests import kepler_mpdark_dark_phase_change_configs, kepler_mpdark_round_robin_change_configs, kepler_sorping_change_configs
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    try:
        # Generation id and time for test run
        report_id = bca.create_event('Kepler change configs tests')
        logger.info(f"Root event was created (id = {report_id.id})")

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text

        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        kepler_mpdark_dark_phase_change_configs.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        kepler_mpdark_round_robin_change_configs.test_run(parent_id=report_id, version=version)
        # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        kepler_sorping_change_configs.test_run(parent_id=report_id, version=version)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()