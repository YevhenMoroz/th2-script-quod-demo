import logging
from xml.etree import ElementTree
from stubs import Stubs, ROOT_DIR
from custom import basic_custom_actions as bca
from regression_cycle.retail_regression_cycle.rest_api_regression.trading_rest_api import trading_rest_api_dma, \
    trading_rest_api_market_data, trading_rest_api_risk_limits, trading_rest_api_buying_power, trading_rest_api_others
from regression_cycle.retail_regression_cycle.rest_api_regression.web_admin_rest_api import web_admin_rest_api_site, \
    web_admin_rest_api_users, web_admin_rest_api_client_accounts, web_admin_rest_api_risk_limits, web_admin_rest_api_positions


def test_run(parent_id=None):
    try:
        report_id = bca.create_event('Retail regression_cycle', parent_id)
        tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
        root = tree.getroot()
        version = root.find(".//version").text
        cycle_name_rest_api = 'RET_AutomationAnalisis'
        cycle_report_rest_api = bca.create_event(f"{cycle_name_rest_api}" if version is None else f"{cycle_name_rest_api} | {version}", report_id)
        logging.getLogger().setLevel(logging.WARN)

        # region __TradingRestApi__ block
        if eval(root.find(".//component[@name='Trading_REST_API_Dma']").attrib["run"]):
            trading_rest_api_dma.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='Trading_REST_API_MarketData']").attrib["run"]):
            trading_rest_api_market_data.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='Trading_REST_API_Positions']").attrib["run"]):
            pass
        if eval(root.find(".//component[@name='Trading_REST_API_RiskLimits']").attrib["run"]):
            trading_rest_api_risk_limits.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='Trading_REST_API_BuyingPower']").attrib["run"]):
            trading_rest_api_buying_power.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='Trading_REST_API_Others']").attrib["run"]):
            trading_rest_api_others.test_run(cycle_report_rest_api)
        # endregion

        # region __WebAdminRestApi__ block
        if eval(root.find(".//component[@name='WA_REST_API_Site']").attrib["run"]):
            web_admin_rest_api_site.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='WA_REST_API_Users']").attrib["run"]):
            web_admin_rest_api_users.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='WA_REST_API_Client_Accounts']").attrib["run"]):
            web_admin_rest_api_client_accounts.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='WA_REST_API_Risk_Limits']").attrib["run"]):
            web_admin_rest_api_risk_limits.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='WA_REST_API_Positions']").attrib["run"]):
            web_admin_rest_api_positions.test_run(cycle_report_rest_api)
        if eval(root.find(".//component[@name='WA_REST_API_Others']").attrib["run"]):
            pass
        # endregion

        # TODO: Add additional blocks for WebTrading and MobileTrading

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
