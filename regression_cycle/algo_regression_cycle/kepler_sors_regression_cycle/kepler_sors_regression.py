from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle.kepler_sors_regression_cycle import kepler_sors_iceberg_regression, kepler_sors_mpdark_regression, kepler_sors_sorping_regression, kepler_sors_synthminqty_regression
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

        if eval(root.find(".//component[@name='sors_iceberg']").attrib["run"]):
            kepler_sors_iceberg_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='mp_dark']").attrib["run"]):
            kepler_sors_mpdark_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='sorping']").attrib["run"]):
            kepler_sors_sorping_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='synth_min_qty']").attrib["run"]):
            kepler_sors_synthminqty_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='multiple_emulation']").attrib["run"]):
            kepler_sors_synthminqty_regression.test_run(parent_id=report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()