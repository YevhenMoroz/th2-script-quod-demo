import time

from stubs import Stubs
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.algo.RestApiAlgoPolicyMessages import RestApiAlgoPolicyMessages


class RestApiAlgoManager(RestApiManager):

    def __init__(self, session_alias, case_id=None):
        super().__init__(session_alias, case_id)

    def modify_strategy_parameter(self, strategy_name: str, parameter_name: str, new_parameter_value: str):
        # region send get request
        rest_manager = RestApiManager("rest_wa319kuiper", self.case_id)
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = rest_manager.send_get_request(find_all_algo_policy)
        strategy = rest_manager.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        # endregion

        # region modify strategy
        strategy.pop("alive")
        if "algoPolicyParameter" in strategy.keys():
            triggered = False
            for param in strategy["algoPolicyParameter"]:
                if param["scenarioParameterName"] == parameter_name:
                    param["algoParameterValue"] = new_parameter_value
                    triggered = True
            if not triggered:
                raise ValueError(f"No scenarioParameterName with name {parameter_name}")
        else:
            raise ValueError("No algoPolicyParameter at current strategy")
        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        rest_manager.send_post_request(modify_algo_policy)
        # endregion
        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = rest_manager.send_get_request(find_all_algo_policy2)
        strategy_updated = rest_manager.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        triggered = False
        for param in strategy_updated["algoPolicyParameter"]:
            if param["scenarioParameterName"] == parameter_name:
                triggered = True
                if param["algoParameterValue"] != new_parameter_value:
                    raise ValueError(f"Strategy didn't modify parameter {parameter_name} with value {new_parameter_value}")
            pass
        if not triggered:
            raise ValueError(f"No scenarioParameterName with name {parameter_name}")
        # endregion

    def modify_strategy_parameters_list(self, strategy_name: str, parameters: dict):
        # region send get request
        rest_manager = RestApiManager("rest_wa319kuiper", self.case_id)
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = rest_manager.send_get_request(find_all_algo_policy)
        strategy = rest_manager.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        # endregion

        # region modify strategy
        strategy.pop("alive")
        if "algoPolicyParameter" in strategy.keys():
            triggered = 0
            for param in strategy["algoPolicyParameter"]:
                if param["scenarioParameterName"] in parameters.keys():
                    param["algoParameterValue"] = parameters[param["scenarioParameterName"]]
                    triggered += 1
            if triggered != len(parameters):
                raise ValueError(f"Not all scenarioParameterName found")
        else:
            raise ValueError("No algoPolicyParameter at current strategy")
        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        rest_manager.send_post_request(modify_algo_policy)
        # endregion
        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = rest_manager.send_get_request(find_all_algo_policy2)
        strategy_updated = rest_manager.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        triggered = 0
        for param in strategy_updated["algoPolicyParameter"]:
            if param["scenarioParameterName"] in parameters.keys():
                triggered += 1
                if param["algoParameterValue"] != parameters[param["scenarioParameterName"]]:
                    raise ValueError(f"Strategy didn't modify parameter {param['algoParameterValue']} with value {parameters[param['scenarioParameterName']]}")
        if triggered != len(parameters):
            raise ValueError(f"Not all scenarioParameterName found at updated strategy")
        # endregion

    def remove_parameters(self, strategy_name: str, *parameters_name: str):
        # region send get request
        rest_manager = RestApiManager("rest_wa319kuiper", self.case_id)
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = rest_manager.send_get_request(find_all_algo_policy)
        strategy = rest_manager.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        # endregion

        # region modification
        strategy.pop("alive")
        if "algoPolicyParameter" in strategy.keys():
            temp = list()
            for parameter in strategy["algoPolicyParameter"]:
                if parameter['scenarioParameterName'] not in parameters_name:
                    temp.append(parameter)

            strategy["algoPolicyParameter"] = temp

        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        rest_manager.send_post_request(modify_algo_policy)
        # endregion

        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = rest_manager.send_get_request(find_all_algo_policy2)
        strategy_updated = rest_manager.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        for param in strategy_updated["algoPolicyParameter"]:
            if param['scenarioParameterName'] in parameters_name:
                raise ValueError(f"Not all scenarioParameterName removed")

        # endregion

    def add_parameter(self, strategy_name: str, new_parameter: dict):
        # region send get request
        rest_manager = RestApiManager("rest_wa319kuiper", self.case_id)
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = rest_manager.send_get_request(find_all_algo_policy)
        strategy = rest_manager.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        # endregion
        print()


        for parameter in strategy["algoPolicyParameter"]:
            if parameter["scenarioParameterName"] == new_parameter["scenarioParameterName"]:
                raise ValueError(f"Parameter already exist")

        strategy.pop("alive")
        strategy["algoPolicyParameter"].append(new_parameter)

        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        rest_manager.send_post_request(modify_algo_policy)


        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = rest_manager.send_get_request(find_all_algo_policy2)
        strategy_updated = rest_manager.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        triggered = False
        for param in strategy_updated["algoPolicyParameter"]:
            if param["scenarioParameterName"] == new_parameter["scenarioParameterName"]:
                triggered = True
        if not triggered:
            raise ValueError(f"Parameter haven't been added")
        # endregion