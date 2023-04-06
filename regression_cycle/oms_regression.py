import logging
from xml.etree import ElementTree

from custom import basic_custom_actions as bca
from regression_cycle.eq_regression_cycle import counterparts_regression, dma_regression, post_trade_regression, \
    commission_regression, care_regression, basket_regression, gateway_regression, gating_rule_regression, \
    positions_regression, bag_regression
from stubs import Stubs, ROOT_DIR


def test_run(parent_id=None):
    try:
        logging.getLogger().setLevel(logging.WARN)
        report_id = bca.create_event('OMS regression_cycle', parent_id)

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text

        if eval(root.find(".//component[@name='DMA']").attrib["run"]):
            dma_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='Care']").attrib["run"]):
            care_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='Counterparts']").attrib["run"]):
            counterparts_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='PostTrade']").attrib["run"]):
            post_trade_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='Commissions']").attrib["run"]):
            commission_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='BasketTrading']").attrib["run"]):
            basket_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='Gateway']").attrib["run"]):
            gateway_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='Positions']").attrib["run"]):
            positions_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='GatingRules']").attrib["run"]):
            gating_rule_regression.test_run(report_id, version, skip_ssh=True)
        if eval(root.find(".//component[@name='Bag']").attrib["run"]):
            bag_regression.test_run(report_id, version, skip_ssh=True)

    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()