import time
from datetime import timedelta, datetime

from xml.etree import ElementTree
from rule_management import RuleManager, Simulators
from regression_cycle.algo_regression_cycle import iceberg_regression, twap_regression, multilisted_regression, participation_regression, tif_regression, litdark_regression, \
    block_regression, stop_regression, peg_regression, triggering_regression, pairtrading_regression
from regression_cycle.algo_regression_cycle.kepler_sors_regression_cycle import kepler_sors_mpdark_other_regression, kepler_sors_iceberg_regression, kepler_sors_multiple_emulation_regression, kepler_sors_sorping_regression, kepler_sors_synthminqty_regression, kepler_sors_mpdark_dark_phase_regression, kepler_sors_mpdark_LIS_dark_phase_regression
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca


def test_run(parent_id=None):
    try:
        start_time = time.monotonic()
        print(f'StartTime is {datetime.utcnow()}')
        mode = 'Verification'
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules_by_alias("fix-bs-310-columbia")
        logging.getLogger().setLevel(logging.WARN)
        report_id = bca.create_event(f'Algo_{mode} cycle', parent_id)

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text

        if eval(root.find(".//component[@name='Twap']").attrib["run"]):
            twap_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Vwap']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Participation']").attrib["run"]):
            participation_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='TimeInForce']").attrib["run"]):
            tif_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Iceberg']").attrib["run"]):
            iceberg_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Block']").attrib["run"]):
            block_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Stop']").attrib["run"]):
            stop_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Multilisted']").attrib["run"]):
            multilisted_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Peg']").attrib["run"]):
            peg_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Triggering']").attrib["run"]):
            triggering_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Lit_dark']").attrib["run"]):
            litdark_regression.test_run(report_id, version, mode)
        if eval(root.find(".//component[@name='Gating_rules']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Web_admin']").attrib["run"]):
            pass
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        #     kepler_sors_mpdark_dark_phase_regression.test_run(parent_id=report_id)
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        #     kepler_sors_mpdark_LIS_dark_phase_regression.test_run(parent_id=report_id)
        # if eval(root.find(".//component[@name='Mp_dark']").attrib["run"]):
        #     kepler_sors_mpdark_other_regression.test_run(parent_id=report_id)
        # if eval(root.find(".//component[@name='Synth_min_qty']").attrib["run"]):
        #     kepler_sors_synthminqty_regression.test_run(report_id, version)
        # if eval(root.find(".//component[@name='Lit_dark_iceberg']").attrib["run"]):
        #     kepler_sors_iceberg_regression.test_run(report_id, version)
        # if eval(root.find(".//component[@name='Sorping']").attrib["run"]):
        #     kepler_sors_sorping_regression.test_run(report_id, version)
        # if eval(root.find(".//component[@name='Multiple_emulation']").attrib["run"]):
        #     kepler_sors_multiple_emulation_regression.test_run(report_id, version)
        # if eval(root.find(".//component[@name='PreOpen_Auction']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='Expity_Auction']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='PreClose_Auction']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='Scaling']").attrib["run"]):
        #     pass
        # if eval(root.find(".//component[@name='POV_Scaling']").attrib["run"]):
        #     pass
        if eval(root.find(".//component[@name='Pair_trading']").attrib["run"]):
            pairtrading_regression.test_run(report_id, version, mode)

        #RB
        #twap_regression_rb.test_run(report_id)
        #parcitipation_regression_rb.test_run(report_id)
        #vwap_regression_rb.test_run(report_id)
        end_time = time.monotonic()
        print(f'EndTime is {datetime.utcnow()}, duration is {timedelta(seconds=end_time-start_time)}')

    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()