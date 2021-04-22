from datetime import datetime

from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    case_name = "QAP-2409"

    symbol = "3631"
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
                        'MDEntrySize': '10000',
                        'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                        'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                    }
                ]
        }
    }
    mdfr_params_1 = {
        'MDReportID': "1",
        'MDReqID': MDRefID_1,
        'Instrument': {
            'Symbol': symbol
        },
        # 'LastUpdateTime': "",
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '650'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
                'MDEntrySize': '600'
            }
        ]
    }
    #
    # act.sendMessage(
    #     request=bca.convert_to_request(
    #         'Send MarketDataSnapshotFullRefresh',
    #         "fix-fh-eq-paris",
    #         case_id,
    #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1, "fix-fh-eq-paris")
    #     )
    # )
    #
    act.sendMessage(
        request=bca.convert_to_request(
            'Send MarketDataIncrementalRefresh',
            "fix-fh-eq-trqx",
            case_id,
            bca.message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade_2, "fix-fh-eq-trqx")
        )
    )


    mdir_params_trade = Message()
    mdir_params_trade.metadata.message_type = "MarketDataSnapshotFullRefresh"
    mdir_params_trade.metadata.id.connection_id.session_alias = "fix-fh-eq-trqx"
    mdir_params_trade.fields['MDReqID'].simple_value = MDRefID
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryType'].simple_value = "0"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryPx'].simple_value = "30"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntrySize'].simple_value = "5000"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDUpdateAction'].simple_value = "0"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryType'].simple_value = "1"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntryPx'].simple_value = "40"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDEntrySize'].simple_value = "5000"
    mdir_params_trade.fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values.add().message_value.fields['MDUpdateAction'].simple_value = "0"


    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_fh)
    ))
