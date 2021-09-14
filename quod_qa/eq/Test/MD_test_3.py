from datetime import datetime

from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction, Message

from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):


    MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="953",
        connection_id=ConnectionID(session_alias="fix-feed-handler-316-ganymede")
    )).MDRefID


    # Вариант 1
    mdir_params_trade = {
        'MDReqID': MDRefID_1,
        'NoMDEntriesIR': [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '20',
                'MDEntrySize': '100',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh', "fix-feed-handler-316-ganymede", report_id,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-feed-handler-316-ganymede")
    ))
    #
    # # # Вариант 2
    # mdir_params_trade = Message()
    # mdir_params_trade.metadata.message_type = "MarketDataIncrementalRefresh"
    # mdir_params_trade.metadata.id.connection_id.session_alias = "fix-fh-310-columbia"
    # mdir_params_trade.fields['MDReqID'].simple_value = MDRefID_1
    # mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDUpdateAction'].simple_value = "0"
    # mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryType'].simple_value = "2"
    # mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryPx'].simple_value = "36"
    # mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntrySize'].simple_value = "10000"
    # mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryDate'].simple_value = datetime.utcnow().date().strftime("%Y%m%d")
    # mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryTime'].simple_value = datetime.utcnow().time().strftime("%H:%M:%S")
    #
    # Stubs.fix_act.sendMessage(request=convert_to_request(
    #     'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", report_id,
    #     mdir_params_trade
    # ))