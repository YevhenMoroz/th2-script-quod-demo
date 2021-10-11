from stubs import Stubs
from th2_grpc_act_gui_quod.act_ui_win_pb2 import ApplicationDetails, LoginDetails, CloseApplicationRequest
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest
from th2_grpc_hand.rhbatch_pb2 import RhSessionID, RhTargetServer
from .application_wrappers import OpenApplicationRequest, LoginDetailsRequest, FEDetailsRequest
import logging
from custom.basic_custom_actions import create_event


def set_session_id():
    if Stubs.session_id is None:
        Stubs.session_id = Stubs.win_act.register(
            RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    return Stubs.session_id


def call(method, args):
    logging.debug("Executing RPC %s", method)
    result = method(args)
    logging.debug("RPC %s:\n%s", method, result)
    # parse result ...
    return result.data


def get_base_request(session_id: RhSessionID, event_id):
    return EmptyRequest(sessionID=session_id, parentEventId=event_id)


def prepare_fe(main_event, session, working_dir: str, username: str, password: str):
    stub = Stubs.win_act
    init_event = create_event("Initialization", parent_id=main_event)
    app_details = ApplicationDetails(
        sessionID=session,
        parentEventId=init_event,
        workDir=working_dir,
        applicationFile=Stubs.custom_config['qf_trading_fe_exec'])
    logging.debug("RPC open_application:\n%s", stub.openApplication(app_details))

    login_details = LoginDetails(
        sessionID=session,
        parentEventId=init_event,
        username=username,
        password=password,
        mainWindowName=Stubs.custom_config['qf_trading_fe_main_win_name'],
        loginWindowName=Stubs.custom_config['qf_trading_fe_login_win_name'])
    logging.debug("RPC login:\n%s", stub.login(login_details))
    Stubs.frontend_is_open = False


def prepare_fe303(main_event, session, working_dir: str, username: str, password: str):
    stub = Stubs.win_act
    init_event = create_event("Initialization", parent_id=main_event)
    app_details = ApplicationDetails(
        sessionID=session,
        parentEventId=init_event,
        workDir=working_dir,
        applicationFile=Stubs.custom_config['qf_trading_fe_exec'])
    logging.debug("RPC open_application:\n%s", stub.openApplication(app_details))

    login_details = LoginDetails(
        sessionID=session,
        parentEventId=init_event,
        username=username,
        password=password,
        mainWindowName=Stubs.custom_config['qf_trading_fe_main_win_name'],
        loginWindowName=Stubs.custom_config['qf_trading_fe_login_win_name'])
    logging.debug("RPC login:\n%s", stub.login(login_details))
    Stubs.frontend_is_open = False


def close_fe(main_event, session):
    stub = Stubs.win_act
    disposing_event = create_event("Disposing", main_event)
    try:
        stub.closeApplication(CloseApplicationRequest(
            base=EmptyRequest(sessionID=session, parentEventId=disposing_event)))
    except Exception as e:
        logging.error("Error disposing application", exc_info=True)
    stub.unregister(session)
    Stubs.frontend_is_open = False


def prepare_fe_2(main_event, session,
                 fe_dir: str = 'qf_trading_fe_folder',
                 fe_user: str = 'qf_trading_fe_user',
                 fe_pass: str = 'qf_trading_fe_password'):
    stub = Stubs.win_act
    init_event = create_event("Initialization", parent_id=main_event)

    open_app_req = OpenApplicationRequest()
    open_app_req.set_session_id(session)
    open_app_req.set_parent_event_id(init_event)
    open_app_req.set_work_dir(Stubs.custom_config[fe_dir])
    open_app_req.set_application_file(Stubs.custom_config['qf_trading_fe_exec'])
    stub.openApplication(open_app_req.build())

    login_details_req = LoginDetailsRequest()
    login_details_req.set_session_id(session)
    login_details_req.set_parent_event_id(init_event)
    login_details_req.set_username(Stubs.custom_config[fe_user])
    login_details_req.set_password(Stubs.custom_config[fe_pass])
    login_details_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name'])
    login_details_req.set_login_window_name(Stubs.custom_config['qf_trading_fe_login_win_name'])
    stub.login(login_details_req.build())


def get_opened_fe(main_event, session, fe_dir: str = 'qf_trading_fe_folder'):
    stub = Stubs.win_act
    init_event = create_event("Initialization", parent_id=main_event)

    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session)
    search_fe_req.set_parent_event_id(init_event)
    search_fe_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name'])
    stub.findOpenedFE(search_fe_req.build())


def get_opened_fe_303(main_event, session):
    stub = Stubs.win_act
    init_event = create_event("Initialization", parent_id=main_event)
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session)
    search_fe_req.set_parent_event_id(init_event)
    search_fe_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name_303'])
    stub.findOpenedFE(search_fe_req.build())


def close_fe_2(main_event, session):
    stub = Stubs.win_act
    disposing_event = create_event("Disposing", main_event)
    try:
        stub.closeApplication(CloseApplicationRequest(
            base=EmptyRequest(sessionID=session, parentEventId=disposing_event)))
    except Exception as e:
        logging.error("Error disposing application", exc_info=True)
    stub.unregister(session)
    Stubs.frontend_is_open = False
