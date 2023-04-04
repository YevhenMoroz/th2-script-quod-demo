import logging
from xml.etree import ElementTree
from custom import basic_custom_actions as bca
from regression_cycle.algo_regression_cycle.redburn.redburn_smoke_list import redburn_twap_smoke, redburn_exa_auction_smoke, redburn_moc_aution_smoke, redburn_pov_smoke, redburn_moo_smoke, redburn_vwap_smoke
from stubs import Stubs, ROOT_DIR

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    try:
        # Generation id and time for test run
        report_id = bca.create_event('Redburn Smoke')
        logger.info(f"Root event was created (id = {report_id.id})")

        tree = ElementTree.parse(f"{ROOT_DIR}/test_framework/configuration_files/regression_run_config_algo.xml")
        root = tree.getroot()
        version = '5.1.132.145'

        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            redburn_twap_smoke.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            redburn_vwap_smoke.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            redburn_pov_smoke.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='PreOpen_Auction']").attrib["run"]):
            redburn_moo_smoke.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Expiry_Auction']").attrib["run"]):
            redburn_exa_auction_smoke.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='PreClose_Auction']").attrib["run"]):
            redburn_moc_aution_smoke.test_run(parent_id=report_id, version=version)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()