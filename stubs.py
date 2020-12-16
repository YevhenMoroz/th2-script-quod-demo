from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from channels import Channels


class Stubs:
    fix_act = ActFixStub(Channels.fix_act_channel)
    event_store = EventStoreServiceStub(Channels.event_store_channel)
    verifier = VerifierStub(Channels.verifier_channel)
    simulator = TemplateSimulatorServiceStub(Channels.simulator_channel)
    sim = ServiceSimulatorStub(Channels.simulator_channel)
