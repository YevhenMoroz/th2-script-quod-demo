from grpc_modules import rhbatch_pb2
from channels import Channels
from grpc_modules.common_pb2 import BaseRequest
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.win_act_pb2_grpc import HandWinActStub
from grpc_modules.win_act_pb2 import ApplicationDetails, LoginDetails
import logging
from configuration import *
from grpc_modules.rhbatch_pb2 import RhTargetServer
from custom.basic_custom_actions import create_event_id, create_store_event_request


def set_session_id():
    application_service = HandWinActStub(Channels.ui_act_channel)
    return application_service.register(RhTargetServer(target=target_server_win)).sessionID


def call(method, args):
    logging.debug("Executing RPC %s", method._method)
    result = method(args)
    logging.debug("RPC %s:\n%s", method._method, result)
    # parse result ...
    return result.data


def get_base_request(session_id: rhbatch_pb2.RhSessionID, event_id):
    return BaseRequest(sessionID=session_id, parentEventId=event_id)


def prepare_fe(main_event, session):
    event_store = EventStoreServiceStub(Channels.event_store_channel)
    init_event = create_event_id()
    event_store.StoreEvent(request=create_store_event_request("Initialization", init_event, main_event))

    stub = HandWinActStub(Channels.ui_act_channel)

    app_details = ApplicationDetails(
        sessionID=session,
        parentEventId=init_event,
        workDir=qf_trading_fe_folder,
        applicationFile=qf_trading_fe_exec)
    logging.debug("RPC open_application:\n%s", stub.openApplication(app_details))

    login_details = LoginDetails(
        sessionID=session,
        parentEventId=init_event,
        username=qf_trading_fe_user,
        password=qf_trading_fe_password,
        mainWindowName="Quod Financial - Quod site",
        loginWindowName=qf_trading_fe_login_win_name)
    logging.debug("RPC login:\n%s", stub.login(login_details))


def close_fe(main_event, session):
    event_store = EventStoreServiceStub(Channels.event_store_channel)
    stub = HandWinActStub(Channels.ui_act_channel)
    disposing_event = create_event_id()
    event_store.StoreEvent(request=create_store_event_request("Disposing", disposing_event, main_event))
    try:
        stub.closeApplication(BaseRequest(sessionID=session, parentEventId=disposing_event))
    except Exception as e:
        logging.error("Error disposing application", exc_info=True)
    stub.unregister(session)
