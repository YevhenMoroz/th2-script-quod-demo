from xml.etree import ElementTree

from regression_cycle import oms_acceptance_list
from regression_cycle.eq_regression_cycle import counterparts_regression, dma_regression, post_trade_regression, \
    commission_regression, care_regression, basket_regression, gateway_regression
from stubs import Stubs, ROOT_DIR
import logging
from custom import basic_custom_actions as bca


def test_run(parent_id=None):
    try:
        logging.getLogger().setLevel(logging.WARN)
        report_id = bca.create_event('OMS regression_cycle', parent_id)

        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        if eval(root.find(".//component[@name='DMA']").attrib["run"]):
            dma_regression.test_run(report_id)
        if eval(root.find(".//component[@name='Care']").attrib["run"]):
            care_regression.test_run(report_id)
        if eval(root.find(".//component[@name='Counterparts']").attrib["run"]):
            counterparts_regression.test_run(report_id)
        if eval(root.find(".//component[@name='PostTrade']").attrib["run"]):
            post_trade_regression.test_run(report_id)
        if eval(root.find(".//component[@name='Commissions']").attrib["run"]):
            commission_regression.test_run(report_id)
        if eval(root.find(".//component[@name='BasketTrading']").attrib["run"]):
            basket_regression.test_run(report_id)
        if eval(root.find(".//component[@name='Gateway']").attrib["run"]):
            gateway_regression.test_run(report_id)
        if eval(root.find(".//component[@name='AcceptanceList']").attrib["run"]):
            oms_acceptance_list.test_run(report_id)

    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()