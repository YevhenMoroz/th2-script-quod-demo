from xml.etree import ElementTree
from regression_cycle.algo_regression_cycle import iceberg_regression, twap_regression, multilisted_regression, participation_regression, tif_regression
from regression_cycle.algo_regression_cycle.kepler_sors_regression_cycle import kepler_sors_mpdark_other_regression, kepler_sors_iceberg_regression, kepler_sors_multiple_emulation_regression, kepler_sors_sorping_regression, kepler_sors_synthminqty_regression, kepler_sors_mpdark_dark_phase_regression, kepler_sors_mpdark_LIS_dark_phase_regression
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca


def test_run(parent_id=None):
    try:
        logging.getLogger().setLevel(logging.WARN)
        report_id = bca.create_event('Algo regression_cycle', parent_id)

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text

        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            twap_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            participation_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Iceberg']").attrib["run"]):
            iceberg_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Multilisted']").attrib["run"]):
            multilisted_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Peg']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Stop']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Lit_dark']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Block']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Gating_rules']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Web_admin']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
            kepler_sors_mpdark_dark_phase_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
            kepler_sors_mpdark_LIS_dark_phase_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
            kepler_sors_mpdark_other_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='Synth_min_qty']").attrib["run"]):
            kepler_sors_synthminqty_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
            kepler_sors_iceberg_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
            kepler_sors_sorping_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='Multiple_emulation']").attrib["run"]):
            kepler_sors_multiple_emulation_regression.test_run(report_id, version)
        if eval(root.find(".//component[@name='PreOpen_Auction']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Expity_Auction']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='PreClose_Auction']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Scaling']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='POV_Scaling']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Pair_trading']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='TimeInForce']").attrib["run"]):
            tif_regression.test_run(report_id, version)

        #RB
        #twap_regression_rb.test_run(report_id)
        #parcitipation_regression_rb.test_run(report_id)
        #vwap_regression_rb.test_run(report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()