# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grpc_modules import quod_simulator_pb2 as quod__simulator__pb2
from grpc_modules import simulator_pb2 as simulator__pb2


class TemplateSimulatorServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.createRule_FIX = channel.unary_unary(
                '/th2.simulator.template.TemplateSimulatorService/createRule_FIX',
                request_serializer=quod__simulator__pb2.TemplateFixCreate.SerializeToString,
                response_deserializer=simulator__pb2.RuleID.FromString,
                )
        self.createKotlinRule_FIX = channel.unary_unary(
                '/th2.simulator.template.TemplateSimulatorService/createKotlinRule_FIX',
                request_serializer=quod__simulator__pb2.TemplateFixCreate.SerializeToString,
                response_deserializer=simulator__pb2.RuleID.FromString,
                )
        self.createQuodNOSRule = channel.unary_unary(
                '/th2.simulator.template.TemplateSimulatorService/createQuodNOSRule',
                request_serializer=quod__simulator__pb2.TemplateQuodNOSRule.SerializeToString,
                response_deserializer=simulator__pb2.RuleID.FromString,
                )
        self.createQuodOCRRule = channel.unary_unary(
                '/th2.simulator.template.TemplateSimulatorService/createQuodOCRRule',
                request_serializer=quod__simulator__pb2.TemplateQuodOCRRule.SerializeToString,
                response_deserializer=simulator__pb2.RuleID.FromString,
                )
        self.createTemplateQuodDemoRule = channel.unary_unary(
                '/th2.simulator.template.TemplateSimulatorService/createTemplateQuodDemoRule',
                request_serializer=quod__simulator__pb2.TemplateQuodDemoRule.SerializeToString,
                response_deserializer=simulator__pb2.RuleID.FromString,
                )
        self.createQuodMDRRule = channel.unary_unary(
                '/th2.simulator.template.TemplateSimulatorService/createQuodMDRRule',
                request_serializer=quod__simulator__pb2.TemplateQuodMDRRule.SerializeToString,
                response_deserializer=simulator__pb2.RuleID.FromString,
                )


class TemplateSimulatorServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def createRule_FIX(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createKotlinRule_FIX(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createQuodNOSRule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createQuodOCRRule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createTemplateQuodDemoRule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def createQuodMDRRule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TemplateSimulatorServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'createRule_FIX': grpc.unary_unary_rpc_method_handler(
                    servicer.createRule_FIX,
                    request_deserializer=quod__simulator__pb2.TemplateFixCreate.FromString,
                    response_serializer=simulator__pb2.RuleID.SerializeToString,
            ),
            'createKotlinRule_FIX': grpc.unary_unary_rpc_method_handler(
                    servicer.createKotlinRule_FIX,
                    request_deserializer=quod__simulator__pb2.TemplateFixCreate.FromString,
                    response_serializer=simulator__pb2.RuleID.SerializeToString,
            ),
            'createQuodNOSRule': grpc.unary_unary_rpc_method_handler(
                    servicer.createQuodNOSRule,
                    request_deserializer=quod__simulator__pb2.TemplateQuodNOSRule.FromString,
                    response_serializer=simulator__pb2.RuleID.SerializeToString,
            ),
            'createQuodOCRRule': grpc.unary_unary_rpc_method_handler(
                    servicer.createQuodOCRRule,
                    request_deserializer=quod__simulator__pb2.TemplateQuodOCRRule.FromString,
                    response_serializer=simulator__pb2.RuleID.SerializeToString,
            ),
            'createTemplateQuodDemoRule': grpc.unary_unary_rpc_method_handler(
                    servicer.createTemplateQuodDemoRule,
                    request_deserializer=quod__simulator__pb2.TemplateQuodDemoRule.FromString,
                    response_serializer=simulator__pb2.RuleID.SerializeToString,
            ),
            'createQuodMDRRule': grpc.unary_unary_rpc_method_handler(
                    servicer.createQuodMDRRule,
                    request_deserializer=quod__simulator__pb2.TemplateQuodMDRRule.FromString,
                    response_serializer=simulator__pb2.RuleID.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'th2.simulator.template.TemplateSimulatorService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TemplateSimulatorService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def createRule_FIX(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/th2.simulator.template.TemplateSimulatorService/createRule_FIX',
            quod__simulator__pb2.TemplateFixCreate.SerializeToString,
            simulator__pb2.RuleID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createKotlinRule_FIX(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/th2.simulator.template.TemplateSimulatorService/createKotlinRule_FIX',
            quod__simulator__pb2.TemplateFixCreate.SerializeToString,
            simulator__pb2.RuleID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createQuodNOSRule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/th2.simulator.template.TemplateSimulatorService/createQuodNOSRule',
            quod__simulator__pb2.TemplateQuodNOSRule.SerializeToString,
            simulator__pb2.RuleID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createQuodOCRRule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/th2.simulator.template.TemplateSimulatorService/createQuodOCRRule',
            quod__simulator__pb2.TemplateQuodOCRRule.SerializeToString,
            simulator__pb2.RuleID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createTemplateQuodDemoRule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/th2.simulator.template.TemplateSimulatorService/createTemplateQuodDemoRule',
            quod__simulator__pb2.TemplateQuodDemoRule.SerializeToString,
            simulator__pb2.RuleID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def createQuodMDRRule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/th2.simulator.template.TemplateSimulatorService/createQuodMDRRule',
            quod__simulator__pb2.TemplateQuodMDRRule.SerializeToString,
            simulator__pb2.RuleID.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
