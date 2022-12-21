from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ReadLogMessageType
from test_framework.read_log_wrappers.ReadLogMessage import ReadLogMessage


class ReadLogMessageAlgo(ReadLogMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=ReadLogMessageType.Csv_Message.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_compare_message_for_check_the_currency_rate(self) -> ReadLogMessage:
        base_parameters = {
            "Currency": 'SEK',
            "Rate": '9.960000000'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_the_lis_amount(self) -> ReadLogMessage:
        base_parameters = {
            "Amount1": '1500',
            "Amount2": '1992000.000000000',
            "Venue": 'CHIXLIS'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_quote_request_status(self) -> ReadLogMessage:
        base_parameters = {
            "Venue": '*',
            "Status": '*',
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_other_quote_requests_terminated(self) -> ReadLogMessage:
        base_parameters = {
            "OrderID": '*',
            "Venue": '*',
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_the_skips_lis_phase(self) -> ReadLogMessage:
        base_parameters = {
            "OrderID": '*',
            "Text": 'skipping LIS phase'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_the_venue_was_suspended(self) -> ReadLogMessage:
        base_parameters = {
            "OrderID": "*",
            "VenueName": "Euronext Paris",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_tags_5052_and_207_mapping(self) -> ReadLogMessage:
        base_parameters = {
            "SecurityExchange": "QDL1",
            "ClOrdID": "*",
            "ExternalStrategyName": "QA_Auto_SORPING_1",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info(self) -> ReadLogMessage:
        base_parameters = {
            "PartyID": "TestCLIENTACCOUNT",
            "MiscNumber": "OrdrMisc0",
            "OrdrMisc": "TestCLIENTACCOUNT",
            "ClOrdID": '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_updating_status(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*",
            "OldStatus": "Open",
            "NewStatus": "Cancelled"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_primary_listing(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*",
            "PrimaryListingID": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_more_than_one_group(self) -> ReadLogMessage:
        base_parameters = {
            "CountOfGroups": "3",
            "GroupNumber": "1",
            "PartyID": "TestClientID",
            "PartyIDSource": "D",
            "PartyRole": "3",
            "ClOrdID": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_for_three_groups_sell_side(self) -> ReadLogMessage:
        base_parameters = {
            "CountOfGroups": "3",
            "PartyID1": "1",
            "PartyIDSource1": "TestClientID",
            "PartyRole1": "D",
            "PartyID2": "TestTraderID",
            "PartyIDSource2": "Proprietary",
            "PartyRole2": "OrderOriginator",
            "PartyID3": "TestTraderName",
            "PartyIDSource3": "OrderOriginator",
            "PartyRole3": "ExecutingTrader",
            "ClOrdID": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_for_three_groups_buy_side(self) -> ReadLogMessage:
        base_parameters = {
            "CountOfGroups": "3",
            "PartyID1": "1",
            "PartyIDSource1": "TestClientID",
            "PartyRole1": "D",
            "PartyID2": "TestTraderID",
            "PartyIDSource2": "Proprietary",
            "PartyRole2": "OrderOriginator",
            "PartyID3": "TestTraderName",
            "PartyIDSource3": "OrderOriginator",
            "PartyRole3": "ExecutingTrader"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_for_the_one_group_sell_side(self) -> ReadLogMessage:
        base_parameters = {
            "PartyID": "TestClientID",
            "PartyIDSource": "D",
            "PartyRole": "3",
            "ClOrdID": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_for_the_one_group_buy_side(self) -> ReadLogMessage:
        base_parameters = {
            "PartyID": "TestClientID",
            "PartyIDSource": "D",
            "PartyRole": "3",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_tag_5047(self) -> ReadLogMessage:
        base_parameters = {
            "AlgoPolicyName": "testTag5047",
            "ClOrdID": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_tag_5048(self) -> ReadLogMessage:
        base_parameters = {
            "ClOrdID": "*",
            "ClientAlgoPolicyID": "QA_Auto_ICEBERG"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_tag_1(self) -> ReadLogMessage:
        base_parameters = {
            "ClOrdID": "*",
            "ClientAccountGroupID": "KEPLER"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_order_event(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*",
            "Text": "no suitable liquidity"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_transact_time_for_child(self) -> ReadLogMessage:
        base_parameters = {
            "TransactTime": "*",
            "ClOrdID": '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_settl_date_part_1(self) -> ReadLogMessage:
        base_parameters = {
            "InstrType": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_settl_date_part_2(self) -> ReadLogMessage:
        base_parameters = {
            "CountOfDays": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_settl_date_part_3(self) -> ReadLogMessage:
        base_parameters = {
            "ClOrdID": "*",
            "SettlDate": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_sell_side(self) -> ReadLogMessage:
        base_parameters = {
            "MiscNumber": "OrdrMisc1",
            "OrdrMisc": "test tag 5001",
            "ClOrdID": '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_party_info_buy_side(self) -> ReadLogMessage:
        base_parameters = {
            "MiscNumber": "OrdrMisc1",
            "OrdrMisc": "test tag 5001",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_not_crossing_mid_price(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*",
            "MidPrice": "27",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_starting_mid_price_monitoring(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_market_event_for_venue(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*",
            "Text": "27",
            "AdditionalParameter": "QUODLIT1",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_skipping_dark_phase_when_primary_suspended(self) -> ReadLogMessage:
        base_parameters = {
            "OrderId": "*"
        }
        super().change_parameters(base_parameters)
        return self


