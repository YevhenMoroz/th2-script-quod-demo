import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T11632(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_qfQuod_any_client_sell_FIXSELLTH2TEST.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/quickfix/client_qfQuod_any_client_sell_FIXSELLTH2TEST.xml"

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        element = ET.fromstring(
            '<miscs enabled="true" fromFix="true" toFix="true"><misc name="Misc0" header="false" tags="10000"/></miscs>')
        quod.append(element)
        quod.find('connectivity/quickfix').append(
            ET.fromstring('<ValidateUserDefinedFields>N</ValidateUserDefinedFields>'))
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.FIXSELLTH2TEST")
        time.sleep(50)
        # endregion

        # region step 1: create DMA  order with ConvertibleBond Instrument
        # part 1: Create DMA order
        instrument: dict = self.data_set.get_fix_instrument_by_name('instrument_convt_bond_paris')
        self.new_order_single.set_default_dma_limit('instrument_convt_bond_paris')
        self.new_order_single.update_fields_in_component('Instrument', {'CouponRate': '15'})
        self.new_order_single.change_parameters({'tag10000': 'BondOnly'})
        cl_ord_id = self.new_order_single.get_parameter('ClOrdID')
        price = self.new_order_single.get_parameter('Price')
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client, self.mic, float(price))
            self.fix_manager.send_message_fix_standard(self.new_order_single)
        except Exception as e:
            logger.error(f'Something go wrong: {e}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)

        self.fix_manager.compare_values({"OrdMiscBlockIsPresent": 'OrdrMiscBlock={ OrdrMisc0="BondOnly" }'},
                                        {"OrdMiscBlockIsPresent": self._get_logs_from_ors(cl_ord_id)[0]},
                                        'Verify that block is present in Fix_NewOrderSingle message from ORS (step 1)',
                                        VerificationMethod.CONTAINS)
        # endregion

        # region step 2: Verify 35=8 message on SellSide
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate', 'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'MaxPriceLevels', 'Parties',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'OrderAvgPx',
                                  'tag11245', 'ExecAllocGrp', 'SettlCurrFxRate', 'ConfirmType', 'SettlCurrFxRateCalc',
                                  'MatchStatus', 'ConfirmStatus', 'SettlCurrAmt', 'CpctyConfGrp', 'ConfirmTransType',
                                  'SettlCurrency', 'AllocSettlCurrAmt', 'TradeReportingIndicator', 'OrigClOrdID',
                                  'SettlType', 'Text', 'ReplyReceivedTime']
        execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        time.sleep(10)
        execution_report_fix.set_default_new(self.new_order_single)
        instrument.pop('CouponRate')
        execution_report_fix.change_parameters({'Instrument': instrument, 'tag10000': 'BondOnly'})
        self.fix_verifier.check_fix_message_fix_standard(execution_report_fix,
                                                         ignored_fields=list_of_ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.FIXSELLTH2TEST")
        time.sleep(50)
        os.remove("temp.xml")
        self.ssh_client.close()

    def _get_logs_from_ors(self, cl_ord_id):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command(
            f'egrep "incoming fix NewOrderSingle.*.ClOrdID=.{cl_ord_id}." QUOD.ORS.log > logs.txt')
        self.ssh_client.get_file('/Logs/quod317/logs.txt', './logs.txt')
        with open("./logs.txt") as file:
            values = file.readlines()
        file.close()
        os.remove('./logs.txt')
        return values
