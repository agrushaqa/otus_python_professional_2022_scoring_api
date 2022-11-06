import logging
from http import HTTPStatus

from config import Config
from schema import ClientsInterestsRequest, MethodRequest, OnlineScoreRequest
from scoring import get_interests, get_score
from validator_birthday import ValidatorBirthday
from validator_client_ids import ValidatorClientIds
from validator_date import ValidatorDate
from validator_email import ValidatorEmail
from validator_first_name import ValidatorFirstName
from validator_gender import ValidatorGender
from validator_last_name import ValidatorLastName
from validator_phone import ValidatorPhone


class SelectValidator:
    def __init__(self, request):
        self.request = request

    @staticmethod
    def separate_params_by_group(schema):
        is_group = {}
        for i_param in schema.list_attr:
            current_group = schema.list_attr[i_param]['group']
            if 'group' in schema.list_attr[i_param].keys():
                if current_group not in is_group:
                    is_group[current_group] = []
                is_group[current_group].append(i_param)
        return is_group

    def _check_groups(self, schema, request):
        is_group = self.separate_params_by_group(schema)
        i_group = {}
        for i_key, i_values in is_group.items():
            if i_key in i_group:
                if i_group[i_key] is False:
                    continue
            i_group[i_key] = True
            for i_value in i_values:
                if i_value not in request:
                    i_group[i_key] = False
        return i_group

    def _validator_group_parameter(self, schema, request):
        # аргументы валидны, если валидны все поля по отдельности
        # и если присутствует хоть одна пара
        if not request:
            raise ValueError(f"request {request} is empty")
        if len(request) < 2:
            raise ValueError("request length < 2")

        groups = self._check_groups(schema, request)
        for i_group in groups.values():
            if i_group:
                return i_group
        raise ValueError("one of group parameter should exists")

    @staticmethod
    def _validator_nullable_params(schema, request):
        for i_param in schema.list_attr:
            if 'nullable' in schema.list_attr[i_param].keys():
                if schema.list_attr[i_param]['nullable'] is False:
                    if not request[i_param]:
                        raise ValueError(f"param length {i_param} is 0")

    @staticmethod
    def list_non_empty_params(request):
        result = []
        for i_param in request.keys():
            if request[i_param]:
                result.append(i_param)
            if request[i_param] == 0:
                result.append(i_param)
        return result

    @staticmethod
    def parameters_list_that_are_array(request):
        result = []
        for i_param in request.keys():
            if type(i_param) in [list, tuple, dict]:
                # hasattr(i_param, '__iter__'): failed by str
                result.append(i_param)
        return result

    def list_all_non_empty_params(self, max_depth=5):
        result = self.list_non_empty_params(self.request)
        i_request = self.request
        for i_level in range(max_depth):
            iterable_params = self.parameters_list_that_are_array(i_request)
            if not iterable_params:
                break
            for i_iterable_param in iterable_params:
                result.append(
                    self.list_non_empty_params(i_request[i_iterable_param]))
                self._sub_search_empty_params(i_request, i_iterable_param,
                                              result, max_depth)
        return result

    def _sub_search_empty_params(self, i_request, i_iterable_param, result,
                                 max_depth):
        max_depth -= 1
        if max_depth <= 0:
            return
        j_iterable_params = self.parameters_list_that_are_array(
            i_iterable_param)
        if not j_iterable_params:
            return result
        j_request = i_request[i_iterable_param]
        for j_iterable_param in j_iterable_params:
            result.append(
                self.list_non_empty_params(j_request[j_iterable_param]))
            result.append(
                self._sub_search_empty_params(
                    j_request[j_iterable_param],
                    j_iterable_param,
                    result,
                    max_depth)
            )

    @staticmethod
    def _validator_required_params(schema, request):
        for i_param in schema.list_attr:
            if "required" in schema.list_attr[i_param].keys():
                logging.info(f"'{i_param}' has required parameter")
                if schema.list_attr[i_param]['required'] is True:
                    logging.info(f"parameter is required for '{i_param}'")
                    logging.info("request keys:")
                    logging.info(request.keys())
                    if i_param not in request.keys():
                        raise ValueError(f"required param {i_param} is absent")

    def online_score(self, context, store):
        schema = MethodRequest()
        self._validator_required_params(schema, self.request['body'])
        self._validator_nullable_params(schema, self.request['body'])
        schema = OnlineScoreRequest()
        self._validator_required_params(schema,
                                        self.request['body']['arguments'])
        self._validator_nullable_params(schema,
                                        self.request['body']['arguments'])
        self._validator_group_parameter(schema,
                                        self.request['body']['arguments'])

        first_name = None
        last_name = None
        email = None
        phone = None
        birthday = None
        gender = None
        if 'first_name' in self.request['body']['arguments']:
            first_name = self.request['body']['arguments']['first_name']
            ValidatorFirstName(first_name)
        if 'last_name' in self.request['body']['arguments']:
            last_name = self.request['body']['arguments']['last_name']
            ValidatorLastName(last_name)
        if 'email' in self.request['body']['arguments']:
            email = self.request['body']['arguments']['email']
            ValidatorEmail(email)
        if 'phone' in self.request['body']['arguments']:
            phone = self.request['body']['arguments']['phone']
            ValidatorPhone(phone)
        if 'birthday' in self.request['body']['arguments']:
            birthday = self.request['body']['arguments']['birthday']
            ValidatorBirthday(birthday)
        if 'gender' in self.request['body']['arguments']:
            gender = self.request['body']['arguments']['gender']
            ValidatorGender(gender)
        if self.request['body']["login"] == Config().admin_login:
            score = 42
        else:
            score = get_score("store", phone, email, birthday, gender,
                              first_name, last_name)

        list_non_empty_params = []
        if 'arguments' in self.request['body']:
            list_non_empty_params = sorted(self.list_non_empty_params(
                self.request['body']['arguments']))
        context["has"] = list_non_empty_params
        return {'score': score,
                'has': context["has"]
                }, HTTPStatus.OK

    def clients_interests(self, context, store):
        schema = MethodRequest()
        self._validator_required_params(schema, self.request['body'])
        self._validator_nullable_params(schema, self.request['body'])
        schema = ClientsInterestsRequest()
        self._validator_required_params(schema,
                                        self.request['body']['arguments'])
        self._validator_nullable_params(schema,
                                        self.request['body']['arguments'])
        ValidatorClientIds(self.request['body']['arguments']['client_ids'])
        if 'date' in self.request['body']['arguments']:
            ValidatorDate(self.request['body']['arguments']['date'])
        list_client_ids = self.request['body']['arguments']['client_ids']
        logging.info(list_client_ids)
        dict_response = {}
        for i_client in list_client_ids:
            dict_response[i_client] = get_interests("store", i_client)
        logging.info("response:")
        logging.info(dict_response)
        return dict_response, HTTPStatus.OK
