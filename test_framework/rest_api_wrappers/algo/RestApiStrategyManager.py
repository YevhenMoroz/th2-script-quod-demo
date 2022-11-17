import time
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.algo.RestApiAlgoPolicyMessages import RestApiAlgoPolicyMessages
from custom import basic_custom_actions as bca

class RestApiAlgoManager(RestApiManager):

    def __init__(self, session_alias, case_id=None):
        super().__init__(session_alias, case_id)

    def modify_strategy_parameter(self, strategy_name: str, parameter_name: str, new_parameter_value: str):
        # region send get request
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
            strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
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
        self.send_post_request(modify_algo_policy)
        # endregion
        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = self.send_get_request(find_all_algo_policy2)
        try:
            strategy_updated = self.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
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
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
            strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
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
        self.send_post_request(modify_algo_policy)
        # endregion
        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = self.send_get_request(find_all_algo_policy2)
        try:
            strategy_updated = self.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
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
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
            strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
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
        self.send_post_request(modify_algo_policy)
        # endregion

        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = self.send_get_request(find_all_algo_policy2)
        try:
            strategy_updated = self.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        for param in strategy_updated["algoPolicyParameter"]:
            if param['scenarioParameterName'] in parameters_name:
                raise ValueError(f"Not all scenarioParameterName removed")

        # endregion

    def add_parameter(self, strategy_name: str, new_parameter: dict):
        # region send get request
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
            strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        # endregion

        for parameter in strategy["algoPolicyParameter"]:
            if parameter["scenarioParameterName"] == new_parameter["scenarioParameterName"]:
                raise ValueError(f"Parameter already exist")

        strategy.pop("alive")
        strategy["algoPolicyParameter"].append(new_parameter)

        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        self.send_post_request(modify_algo_policy)


        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = self.send_get_request(find_all_algo_policy2)
        try:
            strategy_updated = self.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        triggered = False
        for param in strategy_updated["algoPolicyParameter"]:
            if param["scenarioParameterName"] == new_parameter["scenarioParameterName"]:
                triggered = True
        if not triggered:
            raise ValueError(f"Parameter haven't been added")
        # endregion

    def add_criteria(self, strategy_name: str, passive_criterias: list = [], aggresive_criterias: list = []):
        # region send get request
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
            strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        # endregion

        if "algoPolicyPassCriteria" in strategy:
            for parameter in strategy["algoPolicyPassCriteria"]:
                if parameter["bestExecCriteria"] in passive_criterias:
                    raise ValueError(f"Passive criteria already exist")
            for criteria in passive_criterias:
                strategy["algoPolicyPassCriteria"].append(dict(bestExecCriteria=criteria))
        else:
            temp_list = list()
            for criteria in passive_criterias:
                temp_list.append(dict(bestExecCriteria=criteria))
            strategy["algoPolicyPassCriteria"] = temp_list


        if "algoPolicyAggrCriteria" in strategy:
            for parameter in strategy["algoPolicyAggrCriteria"]:
                if parameter["bestExecCriteria"] in aggresive_criterias:
                    raise ValueError(f"Aggressive criteria already exist")
            for criteria in aggresive_criterias:
                strategy["algoPolicyAggrCriteria"].append(dict(bestExecCriteria=criteria))
        else:
            temp_list = list()
            for criteria in aggresive_criterias:
                temp_list.append(dict(bestExecCriteria=criteria))
            strategy["algoPolicyAggrCriteria"] = temp_list

        strategy.pop("alive")

        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        self.send_post_request(modify_algo_policy)

        time.sleep(1)
        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = self.send_get_request(find_all_algo_policy2)
        try:
            strategy_updated = self.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        triggered = 0
        if "algoPolicyPassCriteria" in strategy:
            for param in strategy_updated["algoPolicyPassCriteria"]:
                if param["bestExecCriteria"] in passive_criterias:
                    triggered += 1
            if triggered != len(passive_criterias):
                raise ValueError(f"Not all passive criteria have been found at updated strategy")

        triggered = 0
        if "algoPolicyAggrCriteria" in strategy:
            for param in strategy_updated["algoPolicyAggrCriteria"]:
                if param["bestExecCriteria"] in aggresive_criterias:
                    triggered += 1
            if triggered != len(aggresive_criterias):
                raise ValueError(f"Not all aggresive criteria have been found at updated strategy")
        # endregion

    def remove_criteria(self, strategy_name: str, passive_criterias: list = [], aggresive_criterias: list = []):
        # region send get request
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
            strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        # endregion

        # region modification
        strategy.pop("alive")
        if "algoPolicyPassCriteria" in strategy.keys():
            temp = list()
            for parameter in strategy["algoPolicyPassCriteria"]:
                if parameter['bestExecCriteria'] not in passive_criterias:
                    temp.append(parameter)
            strategy["algoPolicyPassCriteria"] = temp

        if "algoPolicyAggrCriteria" in strategy.keys():
            temp = list()
            for parameter in strategy["algoPolicyAggrCriteria"]:
                if parameter['bestExecCriteria'] not in aggresive_criterias:
                    temp.append(parameter)
            strategy["algoPolicyAggrCriteria"] = temp

        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        self.send_post_request(modify_algo_policy)
        # endregion

        time.sleep(1)

        # region check is modify confirmed
        find_all_algo_policy2 = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply2 = self.send_get_request(find_all_algo_policy2)
        try:
            strategy_updated = self.parse_response_details(grpc_reply2, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        if "algoPolicyPassCriteria" in strategy_updated.keys():
            for param in strategy_updated["algoPolicyPassCriteria"]:
                if param["bestExecCriteria"] in passive_criterias:
                    raise ValueError(f"Passive criteria haven't been removed")

        if "algoPolicyAggrCriteria" in strategy_updated.keys():
            for param in strategy_updated["algoPolicyAggrCriteria"]:
                if param["bestExecCriteria"] in aggresive_criterias:
                    raise ValueError(f"Aggressive criteria haven't been removed")
        # endregion

    def update_criteria(self, strategy_name: str, passive_criterias: list = [], aggresive_criterias: list = []):
        # region send get request
        find_all_algo_policy = RestApiAlgoPolicyMessages().find_all_algo_policies()
        grpc_reply = self.send_get_request(find_all_algo_policy)
        try:
             strategy = self.parse_response_details(grpc_reply, {"algoPolicyName": strategy_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        # endregion

        # region modification
        strategy.pop("alive")
        if "algoPolicyPassCriteria" in strategy.keys():
            temp = list()
            for parameter in passive_criterias:
                temp.append(dict(bestExecCriteria=parameter))
            strategy["algoPolicyPassCriteria"] = temp

        if "algoPolicyAggrCriteria" in strategy.keys():
            temp = list()
            for parameter in aggresive_criterias:
                temp.append(dict(bestExecCriteria=parameter))
            strategy["algoPolicyAggrCriteria"] = temp

        modify_algo_policy = RestApiAlgoPolicyMessages().modify_algo_policy(strategy)
        self.send_post_request(modify_algo_policy)
        # endregion

        time.sleep(1)

    def modify_trading_phase_profile(self, trading_phase_name: str, trading_phase_sequence: list=[]):
        find_all_trading_phase_profile = RestApiAlgoPolicyMessages().find_all_trading_phase_profile()
        grpc_reply = self.send_get_request(find_all_trading_phase_profile)
        try:
            trading_phase_profile = self.parse_response_details(grpc_reply, {"tradPhaseProfileDesc": trading_phase_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        trading_phase_profile.pop("alive")
        trading_phase_profile["tradingPhaseSequence"] = trading_phase_sequence


        for index, phase in enumerate(trading_phase_profile["tradingPhaseSequence"]):
            trading_phase_profile["tradingPhaseSequence"][index]['beginTime'] = str(AlgoFormulasManager.change_time_from_normal_to_epoch(phase['beginTime']))
            trading_phase_profile["tradingPhaseSequence"][index]['endTime'] = str(AlgoFormulasManager.change_time_from_normal_to_epoch(phase['endTime']))
            trading_phase_profile["tradingPhaseSequence"][index]['submitAllowed'] = phase['submitAllowed'].lower()

        modifyTradingPhaseProfile = RestApiAlgoPolicyMessages().modify_trading_phase_profile(parameters=trading_phase_profile)
        self.send_post_request(modifyTradingPhaseProfile)

        time.sleep(1)
        find_all_trading_phase_profile2 = RestApiAlgoPolicyMessages().find_all_trading_phase_profile()
        grpc_reply2 = self.send_get_request(find_all_trading_phase_profile2)
        try:
            trading_phase_profile_updated = self.parse_response_details(grpc_reply2, {"tradPhaseProfileDesc": trading_phase_name})
        except Exception as e:
            bca.create_event(f"Fail test event - can't handle rest api reply",
                             status='FAILED',
                             parent_id=self.case_id,
                             body=str(e))
            return
        trading_phase_profile_updated.pop("alive")

        if not [i for i in trading_phase_profile_updated["tradingPhaseSequence"] if i not in trading_phase_sequence] == []:
            raise ValueError(f"Trading phase profile doesn't update")