import logging
import time
from datetime import timedelta
from xml.etree import ElementTree

from custom import basic_custom_actions as bca
from regression_cycle.web_admin_cycle.run_client_accounts import RunClientsAccounts
from regression_cycle.web_admin_cycle.run_general import RunGeneral
from regression_cycle.web_admin_cycle.run_market_making import RunMarketMaking
from regression_cycle.web_admin_cycle.run_middle_office import RunMiddleOffice
from regression_cycle.web_admin_cycle.run_order_management import RunOrderManagement
from regression_cycle.web_admin_cycle.run_positions import RunPositions
from regression_cycle.web_admin_cycle.run_reference_data import ReferenceData
from regression_cycle.web_admin_cycle.run_risk_limits import RunRiskLimits
from regression_cycle.web_admin_cycle.run_price_cleansing import RunPriceCleansing
from regression_cycle.web_admin_cycle.run_site import RunSite
from regression_cycle.web_admin_cycle.run_users import RunUsers
from regression_cycle.web_admin_cycle.run_other import RunOthers
from stubs import Stubs, ROOT_DIR

logging.basicConfig(format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.WARN)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('WebAdmin | 5.1.161.174', parent_id)
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    try:
        start_time = time.monotonic()
        if eval(root.find(".//component[@name='WA_General']").attrib["run"]):
            RunGeneral(report_id).execute()
        if eval(root.find(".//component[@name='WA_Site']").attrib["run"]):
            RunSite(report_id).execute()
        if eval(root.find(".//component[@name='WA_Users']").attrib["run"]):
            RunUsers(report_id).execute()
        if eval(root.find(".//component[@name='WA_Reference_Data']").attrib["run"]):
            ReferenceData(report_id).execute()
        if eval(root.find(".//component[@name='WA_Client_Accounts']").attrib["run"]):
            RunClientsAccounts(report_id).execute()
        if eval(root.find(".//component[@name='WA_Order_Management']").attrib["run"]):
            RunOrderManagement(report_id).execute()
        if eval(root.find(".//component[@name='WA_Middle_Office']").attrib["run"]):
            RunMiddleOffice(report_id).execute()
        if eval(root.find(".//component[@name='WA_Market_Making']").attrib["run"]):
            RunMarketMaking(report_id).execute()
        if eval(root.find(".//component[@name='WA_Price_Cleansing']").attrib["run"]):
            RunPriceCleansing(report_id).execute()
        if eval(root.find(".//component[@name='WA_Risk_Limits']").attrib["run"]):
            RunRiskLimits(report_id).execute()
        if eval(root.find(".//component[@name='WA_Positions']").attrib["run"]):
            RunPositions(report_id).execute()
        if eval(root.find(".//component[@name='WA_Others']").attrib["run"]):
            RunOthers(report_id).execute()
        end_time = time.monotonic()
        print("Test cases completed\n" +
              "~Total elapsed execution time~ = " + str(timedelta(seconds=end_time - start_time)))

    except Exception as e:
        print(e.__class__.__name__)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
