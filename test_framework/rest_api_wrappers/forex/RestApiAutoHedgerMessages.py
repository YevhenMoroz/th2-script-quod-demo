from datetime import datetime, timedelta

from test_cases.fx.fx_wrapper.common_tools import generate_schedule
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiAutoHedgerMessages(RestApiMessages):

    def set_default_params(self):
        self.parameters = {
            "autoHedgerName": "OsmiumAH",
            "hedgeAccountGroupID": "QUOD3",
            "autoHedgerID": '1400008',
            "alive": "true",
            "hedgedAccountGroup": [
                {
                    "accountGroupID": "Osmium1"
                }
            ],
            "autoHedgerInstrSymbol": [
                {
                    "instrSymbol": "EUR/USD",
                    "longUpperQty": '2000000',
                    "longLowerQty": '0',
                    "maintainHedgePositions": "true",
                    "crossCurrPairHedgingPolicy": "DIR",
                    "useSameLongShortQty": "true",
                    "hedgingStrategy": "POS",
                    "algoPolicyID": '400018',
                    "shortLowerQty": '0',
                    "shortUpperQty": '0',
                    "timeInForce": "DAY",
                    "sendHedgeOrders": 'true',
                    "exposureDuration": '120',
                    "hedgeOrderDestination": "EXT"
                }
            ]
            }
        return self

    def find_all_auto_hedger(self):
        """
        Default message to get all auto hedgers
        """
        # TODO: Add message to dictionary
        self.message_type = 'FindAllAutoHedger'
        return self

    def add_auto_hedger_instrument(self, symbol, long_upper_qty='1000000', long_lower_qty='0', short_lower_qty='0',
                                   short_upper_qty='0', policy_id=None, use_same_qty='true', time_in_force='DAY',
                                   send_hedge_orders='true', exposure_duration='120', market='EXT', cross_policy='DIR',
                                   maintain_positions='true'):
        instrumet = {
                    "instrSymbol": str(symbol),
                    "longUpperQty": str(long_upper_qty),
                    "longLowerQty": str(long_lower_qty),
                    "maintainHedgePositions": str(maintain_positions),
                    "crossCurrPairHedgingPolicy": str(cross_policy),
                    "useSameLongShortQty": str(use_same_qty),
                    "hedgingStrategy": "POS",
                    "algoPolicyID": str(policy_id) if policy_id is not None else policy_id,
                    "shortLowerQty": str(short_lower_qty),
                    "shortUpperQty": str(short_upper_qty),
                    "timeInForce": str(time_in_force),
                    "sendHedgeOrders": str(send_hedge_orders),
                    "exposureDuration": str(exposure_duration),
                    "hedgeOrderDestination": str(market)
                }
        self.parameters["autoHedgerInstrSymbol"].append(instrumet)

    def modify_auto_hedger(self):
        """
        This method sets up an default dictionary for most used AH in forex test-cases
        """
        self.message_type = 'ModifyAutoHedger'
        return self

    def create_auto_hedger(self):
        """
        This method sets up and default dictionary required to create new AutoHedger
        """
        # TODO: Add message to dictionary
        if 'autoHedgerID' in self.parameters.keys():
            self.remove_parameter('autoHedgerID')
        self.message_type = 'CreateAutoHedger'
        return self

    def add_schedule(self, hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                     minutes_to_time=None, day: str = None):
        """
        Method is designed to add working schedule for auto hedger
        In default usage sets current day with current from time and to time
        Time difference and day is configurable parameters
        """
        schedule_dict = generate_schedule(hours_from_time, hours_to_time, minutes_from_time, minutes_to_time, day)
        self.update_parameters({'autoHedgerSchedule': schedule_dict, 'enableSchedule': 'true'})
        return self

    def delete_auto_hedger(self):
        """
        Default message to get all auto hedgers
        """
        # TODO: Add message to dictionary
        self.message_type = 'DeleteAutoHedger'
        return self

    def send_hedge_orders_true(self):
        params = {
            "sendHedgeOrders": "true",
            "autoHedgerStatusID": "1"
        }
        self.set_params(params)
        self.message_type = "ModifyAutoHedgerStatus"
        return self

    def send_hedge_orders_false(self):
        params = {
            "sendHedgeOrders": "false",
            "autoHedgerStatusID": "1"
        }
        self.set_params(params)
        self.message_type = "ModifyAutoHedgerStatus"
        return self
