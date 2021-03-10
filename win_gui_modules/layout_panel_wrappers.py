from th2_grpc_act_gui_quod import layout_panel_pb2


class WorkspaceModificationRequest:
    def __init__(self):
        self.ws_modify_request = layout_panel_pb2.WorkspaceModificationRequest()

    def set_default_params(self, base_request):
        self.ws_modify_request.base.CopyFrom(base_request)

    def set_path(self, path: str):
        self.ws_modify_request.path = path

    def set_filename(self, filename: str):
        self.ws_modify_request.fileName = filename

    def do_import(self):
        self.ws_modify_request.actionType = layout_panel_pb2.WorkspaceModificationRequest.ActionType.IMPORT

    def do_export(self):
        self.ws_modify_request.actionType = layout_panel_pb2.WorkspaceModificationRequest.ActionType.EXPORT

    def build(self):
        return self.ws_modify_request
