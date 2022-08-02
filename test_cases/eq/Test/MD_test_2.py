from datetime import datetime, timedelta

from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction, Message
from stubs import Stubs

timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    case_name = "QAP_T5074"

    symbol = "3166"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
    )).MDRefID

    # mdir_params_trade = {
    #     'MDReqID': MDRefID_1,
    #     'NoMDEntries': [
    #
    #         {
    #             'MDUpdateAction': '0',
    #             'MDEntryType': '2',
    #             'MDEntryPx': '1.2',
    #             'MDEntrySize': '10000',
    #             'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
    #             'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
    #         }
    #     ]
    # }

    mdir_params_trade_2 = {
        'MDReqID': MDRefID_1,
        'NoMDEntriesIR': {
            "NoMDEntriesIR_NoMDEntriesIRIDs ":
                [
                    {
                        'MDUpdateAction': '0',
                        'MDEntryType': '2',
                        'MDEntryPx': '1.2',
                        'MDEntrySize': '5000',
                        'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                        'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                    }
                ]
        }
    }

    mdir_params_trade = Message()
    mdir_params_trade.metadata.message_type = "MarketDataIncrementalRefresh"
    mdir_params_trade.metadata.id.connection_id.session_alias = "fix-fh-eq-trqx"
    mdir_params_trade.fields['MDReqID'].simple_value = MDRefID_1
    mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDUpdateAction'].simple_value = "0"
    mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryType'].simple_value = "B"
    mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryPx'].simple_value = "35"
    mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntrySize'].simple_value = "3000"
    mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields[
        'NoMDEntries'].list_value.values.add().message_value.fields[
        'MDEntryDate'].simple_value = datetime.utcnow().date().strftime("%Y%m%d")
    mdir_params_trade.fields['NoMDEntriesIR'].message_value.fields[
        'NoMDEntries'].list_value.values.add().message_value.fields[
        'MDEntryTime'].simple_value = (datetime.utcnow() + timedelta(seconds=1)).time().strftime("%H:%M:%S")

    act.sendMessage(
        request=bca.convert_to_request(
            'Send MarketDataIncrementalRefresh',
            "fix-fh-eq-trqx",
            case_id,
            mdir_params_trade
        )
    )
