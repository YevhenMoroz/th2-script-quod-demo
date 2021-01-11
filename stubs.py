from th2_common.schema.factory.common_factory import CommonFactory
# from th2_grpc_act_template.act_template_service import ActService
from th2_grpc_act_quod.act_fix_service import ActFixService
from th2_grpc_check1.check1_service import Check1Service
from th2_grpc_sim_quod.sim_service import TemplateSimulatorServiceService
from th2_grpc_sim.sim_service import SimService


class Stubs:
    factory = CommonFactory(
        grpc_router_config_filepath="./configs/grpc.json",
        rabbit_mq_config_filepath="./configs/rabbit.json",
        mq_router_config_filepath="./configs/mq.json"
    )
    fix_act = factory.grpc_router.get_service(ActFixService)
    event_store = factory.event_batch_router
    verifier = factory.grpc_router.get_service(Check1Service)
    simulator = factory.grpc_router.get_service(TemplateSimulatorServiceService)
    core = factory.grpc_router.get_service(SimService)
