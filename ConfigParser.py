from __future__ import print_function

import logging
import time
import os
import xml.etree.ElementTree as ET
from datetime import datetime

timeouts = False

def ParseConfig():
    #PATH to configuration file
    config_home = os.path.dirname(os.path.abspath(__file__))
    config_name = 'Config.xml'
    config_path = os.path.join(config_home, config_name)

    #Configuration file parsing
    # try:
    config_data = {}
    config_tree = ET.parse(config_path)
    config_root = config_tree.getroot()
    for config_elem in config_root:
        print("Parsing {}".format(config_root.tag))
        for config_subelem in config_elem:
            if config_elem.tag == 'TH2Components':
                config_data[config_subelem.tag] = config_subelem.text
            else:
                pass
    if not config_data:
        raise ValueError("Config is empty")
    return config_data
