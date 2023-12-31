from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID


class FixManager:

    def __init__(self, TraderConnectivity, case_id):
        self.TraderConnectivity = TraderConnectivity
        self.case_id = case_id
        self.act = Stubs.fix_act
        self.simulator = Stubs.simulator

    def get_case_id(self):
        return self.case_id

    def Send_NewOrderSingle_FixMessage(self, fix_message, message_name='Send NewOrderSingle', case=None):
        if case == None:
            case = self.case_id

        response = self.act.placeOrderFIX(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                case,
                bca.message_to_grpc('NewOrderSingle', fix_message.get_parameters(), self.TraderConnectivity)
            ))

        return response

    def Send_OrderCancelRequest_FixMessage(self, fix_message, message_name='Cancel order', case=None):
        if case == None:
            case = self.case_id

        response = self.act.placeOrderCancelFIX(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                case,
                bca.message_to_grpc('OrderCancelRequest', fix_message.get_parameters(), self.TraderConnectivity)
            ))
        return response

    def Send_OrderCancelReplaceRequest_FixMessage(self, fix_message, message_name='Replace order', case=None):
        if case == None:
            case = self.case_id

        response = self.act.placeOrderReplaceFIX(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                case,
                bca.message_to_grpc('OrderCancelReplaceRequest', fix_message.get_parameters(), self.TraderConnectivity)
            ))
        return response

    def Send_MarketDataFullSnapshotRefresh_FixMessage(self, fix_message, symbol, message_name='Send MarketData'):
        MDReqID = self.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=str(symbol),
            connection_id=ConnectionID(session_alias=self.TraderConnectivity)
        )).MDRefID

        # fix_message.add_tag({'Instrument': {'Symbol': symbol}})
        fix_message.add_tag({'MDReqID': MDReqID})

        response = self.act.sendMessage(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                self.case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', fix_message.get_parameters(),
                                    self.TraderConnectivity)
            ))
        return response

    def Send_MarketDataIncrementalRefresh_FixMessage(self, fix_message, symbol,
                                                     message_name='Send Incremental MarketData'):
        MDReqID = self.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=self.TraderConnectivity)
        )).MDRefID
        fix_message.add_tag({'MDReqID': MDReqID})
        response = self.act.sendMessage(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                self.case_id,
                bca.message_to_grpc('MarketDataIncrementalRefresh', fix_message.get_parameters(),
                                    self.TraderConnectivity)
            ))
        return response

    def Send_MarketDataRequest_FixMessage(self, fix_message, message_name='Send MarketDataRequest'):
        response = self.act.sendMessage(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', fix_message.get_parameters(), self.TraderConnectivity)
            ))
        return response

    def Send_NewOrderList_FixMessage(self, fix_message, message_name='Send NewOrderList', case=None):
        if case == None:
            case = self.case_id

        response = self.act.placeOrderListFIX(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                case,
                bca.message_to_grpc_test('NewOrderList', fix_message.get_parameters(), self.TraderConnectivity)
            ))
        return response

    def Send_ListCancelRequest_FixMessage(self, fix_message, message_name='Cancel order list', case=None):
        if case == None:
            case = self.case_id

        response = self.act.placeListCancelRequestFIX(
            request=bca.convert_to_request(
                message_name,
                self.TraderConnectivity,
                case,
                bca.message_to_grpc('ListCancelRequest', fix_message.get_parameters(), self.TraderConnectivity)
            ))
        return response

    def CheckSubscription(self, MDSymbol):
        # TODO Need Update
        simulator = Stubs.simulator
        allMDRefID = simulator.getAllMDRefID(request=RequestMDRefID(
            connection_id=ConnectionID(session_alias=self.TraderConnectivity)
        ))
        for i in allMDRefID.PairsMDRefID:
            print({i.symbol: i.MDRefID}, type({i.symbol: i.MDRefID}))
