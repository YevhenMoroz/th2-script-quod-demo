from datetime import datetime, timedelta

from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiAutoHedgerMessages(RestApiMessages):

    def find_all_auto_hedger(self):
        self.message_type = 'FindAllAutoHedger'
        return self

    def modify_auto_hedger(self):
        '''
        This method sets up an default dictionary for most used AH in forex test-cases
        '''
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
        self.message_type = 'ModifyAutoHedger'
        return self

    def create_auto_hedger(self):
        '''
        This method sets up and default dictionary required to create new AutoHedger
        '''
        self.parameters = {
            "autoHedgerName": "test",
            "hedgeAccountGroupID": "QUOD",
            "alive": 'true',
            "hedgedAccountGroup": [
                {
                  "accountGroupID": "QUOD2"
                },
                {
                  "accountGroupID": "CLIENT1"
                }
            ],
            "autoHedgerInstrSymbol": [
              {
                "instrSymbol": "EUR/USD",
                "longUpperQty": '1000000',
                "longLowerQty": '0',
                "maintainHedgePositions": 'true',
                "crossCurrPairHedgingPolicy": "DIR",
                "useSameLongShortQty": 'true',
                "hedgingStrategy": "POS",
                "algoPolicyID": '400019',
                "shortLowerQty": '0',
                "shortUpperQty": '0',
                "timeInForce": "DAY",
                "sendHedgeOrders": 'true',
                "exposureDuration": '120',
                "hedgeOrderDestination": "EXT"
              }
            ]
            }
        self.message_type = 'createAutoHedger'
        return self

    def add_schedule(self, hours_from_time, hours_to_time, minutes_from_time, minutes_to_time):
        timestamp = str(datetime.now().timestamp())
        timestamp = timestamp.split(".", 1)
        timestamp = timestamp[0]
        schedule_dict = {
            'scheduleFromTime': str((datetime.now() - timedelta(hours=hours_from_time)).timestamp()).split(".", 1)[0] + '000',
            'scheduleToTime': str((datetime.now() + timedelta(hours=hours_to_time)).timestamp()).split(".", 1)[0] + '000',
            'weekDay': datetime.now().strftime("%a").upper()
        }


