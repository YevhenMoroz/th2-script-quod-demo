from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle.redburn_regresion_cycle import redburn_twap_regression, redburn_twap_navigator_regression, redburn_twap_aution_regression, redburn_twap_additional_features_regression, redburn_vwap_regression, redburn_vwap_navigator_regression, redburn_vwap_aution_regression, redburn_vwap_additional_features_regression, redburn_pov_regression, redburn_pov_navigator_regression, redburn_pov_aution_regression, redburn_pov_additional_features_regression, redburn_moo_regression, redburn_exa_auction_regression, redburn_moc_aution_regression, redburn_auction_scaling_regression, redburn_pov_scaling_regression
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    try:
        # Generation id and time for test run
        report_id = bca.create_event('Redburn')
        logger.info(f"Root event was created (id = {report_id.id})")

        tree = ElementTree.parse(f"{ROOT_DIR}/test_framework/configuration_files/regression_run_config_algo.xml")
        root = tree.getroot()
        version = '5.1.132.145'

        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            redburn_twap_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            redburn_twap_navigator_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            redburn_twap_aution_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            redburn_twap_additional_features_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            redburn_vwap_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            redburn_vwap_navigator_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            redburn_vwap_aution_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            redburn_vwap_additional_features_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            redburn_pov_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            redburn_pov_navigator_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            redburn_pov_aution_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            redburn_pov_additional_features_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='PreOpen_Auction']").attrib["run"]):
            redburn_moo_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Expiry_Auction']").attrib["run"]):
            redburn_exa_auction_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='PreClose_Auction']").attrib["run"]):
            redburn_moc_aution_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='Scaling']").attrib["run"]):
            redburn_auction_scaling_regression.test_run(parent_id=report_id, version=version)
        if eval(root.find(".//component[@name='POV_Scaling']").attrib["run"]):
            redburn_pov_scaling_regression.test_run(parent_id=report_id, version=version)

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()