from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from th2_common.schema.factory.common_factory import CommonFactory
from th2_grpc_act_template.act_template_service import ActService
from th2_grpc_check1.check1_service import Check1Service
from channels import Channels


class Stubs:
    factory = CommonFactory(
        grpc_router_config_filepath="./configs/grpc.json",
        rabbit_mq_config_filepath="./configs/rabbit.json",
        mq_router_config_filepath="./configs/mq.json"
    )
    fix_act = factory.grpc_router.get_service(ActService)
    event_store = factory.event_batch_router
    verifier = factory.grpc_router.get_service(Check1Service)

    # fix_act = ActFixStub(Channels.fix_act_channel)
    # event_store = EventStoreServiceStub(Channels.event_store_channel)
    # verifier = VerifierStub(Channels.verifier_channel)
    # simulator = TemplateSimulatorServiceStub(Channels.simulator_channel)
    # sim = ServiceSimulatorStub(Channels.simulator_channel)
