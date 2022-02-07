from datetime import datetime, timedelta

from test_cases.fx.fx_wrapper.common_tools import generate_schedule
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiClientTierMessages(RestApiMessages):

    def find_all_client_tier(self):
        self.clear_message_params()
        self.message_type = 'FindAllClientTier'
        return self

    def modify_client_tier(self):
        self.message_type = 'ModifyClientTier'
        return self

    def set_defeault_params(self):
        self.parameters = {
            'TODTimeZone': "Europe/Kiev",
            'alive': 'true',
            'clientTierID': '',
            'clientTierName': '',
            'enableSchedule': 'false',
            'pricingMethod': "VWP"
        }
        return self

    def add_schedule_day(self, hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                         minutes_to_time=None, day: str = None):
        result = list(map(lambda x: day == x['weekDay'], self.parameters['clientTierSchedule']))
        schedule_day = generate_schedule(hours_from_time, hours_to_time, minutes_from_time,
                                         minutes_to_time, day)
        if True not in result:
            self.parameters['clientTierSchedule'].append(schedule_day)
        else:
            self.parameters['clientTierSchedule'].pop(result.index(True))
            self.parameters['clientTierSchedule'].append(schedule_day)

    def add_schedule_days(self, hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                          minutes_to_time=None, day: list = None):
        pass

    def remove_schedule_day(self, day: str = None):
        result = list(map(lambda x: day == x['weekDay'], self.parameters['clientTierSchedule']))
        if True in result:
            self.parameters['clientTierSchedule'].pop(result.index(True))

    def remove_schedule_days(self, day: list = None):
        pass

    def set_schedule_day(self, hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                         minutes_to_time=None, day: str = None):
        pass

    def set_schedule_days(self, hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                          minutes_to_time=None, day: list = None):
        pass
