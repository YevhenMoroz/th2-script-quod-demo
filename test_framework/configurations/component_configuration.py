from xml.etree import ElementTree

# region import data_sets
from test_framework.data_sets.web_admin_data_set.web_admin_data_set import WebAdminDataSet
from test_framework.data_sets.web_trading_data_set.web_trading_data_set import WebTradingDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.data_sets.algo_data_set.algo_data_set import AlgoDataSet
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.data_sets.ret_data_set.ret_data_set import RetDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
# endregion

from stubs import ROOT_DIR


class ComponentConfiguration:
    xpath = f"{ROOT_DIR}/regression_run_config.xml"

    def __init__(self, component_name: str):
        tree = ElementTree.parse(ComponentConfiguration.xpath)
        root = tree.getroot()
        try:
            self.name = root.find(f".//component[@name='{component_name}']").attrib["name"]
        except Exception:
            print(f"Can not find component with name {component_name}")

        self.run = eval(root.find(f".//component[@name='{component_name}']").attrib["run"])
        self.data_set = eval(root.find(f".//component[@name='{component_name}']/data_set").text)()

        component_environment = root.find(f".//component[@name='{self.name}']/environments").getchildren()
        self.environment = FullEnvironment(component_environment)
