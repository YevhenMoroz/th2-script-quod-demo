from regression_cycle import fx_acceptance_list
from regression_cycle.fx_regression_cycle import rfq_taker_regression, esp_mm_regression, esp_taker_regression, \
    mm_positions_regression, fx_mm_rfq_regression, fx_mm_AH_regression
from stubs import Stubs, ROOT_DIR
from xml.etree import ElementTree
import logging
from custom import basic_custom_actions as bca


def test_run(parent_id=None):
    report_id = bca.create_event('Regression', parent_id)
    try:
        logging.getLogger().setLevel(logging.WARN)
        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()

        if eval(root.find(".//component[@name='ESP_MM']").attrib["run"]):
            esp_mm_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='ESP_Taker']").attrib["run"]):
            esp_taker_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='RFQ_MM']").attrib["run"]):
            fx_mm_rfq_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='RFQ_Taker']").attrib["run"]):
            rfq_taker_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='Position']").attrib["run"]):
            mm_positions_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='AutoHedger']").attrib["run"]):
            fx_mm_AH_regression.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='FX_Acceptance_list']").attrib["run"]):
            fx_acceptance_list.test_run(parent_id=report_id)
        if eval(root.find(".//component[@name='Synthetic']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='FX_Smoke_list']").attrib["run"]):
            pass

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
