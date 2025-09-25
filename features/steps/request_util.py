# pylint: disable=missing-module-docstring
# pylint: disable=undefined-variable
# pylint: disable=broad-exception-raised
# pylint: disable=too-many-locals
# pylint: disable=line-too-long
# pylint: disable=missing-timeout
# pylint: disable=too-many-branches
# pylint: disable=unused-variable
import base64
import json

import requests
import logger


def set_api_endpoint(context, text):
    """This method sets the API endpoint URL in the context
    and logs the URL in each step message."""
    context.api_url = text
    logger.info(context, context.api_url)


def set_api_method(context, text):
    """This method sets the API request method type in the context."""
    context.method_type = text
    logger.info(context, context.method_type)


def set_api_parameter(context, text):
    """This method sets the API parameter in the context."""
    context.api_parameter = text
    logger.info(context, context.api_parameter)


def set_api_basic_auth(context, text):
    """This method sets the API Basicauth in the context."""
    context.api_basic_auth = text
    logger.info(context, context.api_basic_auth)


def set_request_payload(context, text):
    """This method sets the API request payload in the context."""
    context.request_payload = text
    logger.info(context, context.request_payload)


def set_api_headers(context, header):
    """This method sets the API request headers in the context."""
    my_dict = {}
    input_parameters = str(header).split(',')
    for parameter in input_parameters:
        header_text = parameter.split(':')
        if len(header_text) > 1:
            header_value = str(header_text[1])
            if '@colon' in str(header_value):
                header_value = header_value.replace('@colon', ':')
            my_dict[header_text[0]] = header_value
    context.api_header = my_dict
    logger.info(context, str(context.api_header))


def set_api_response_dictionary(context, text, key):
    """This method extracts values from the API response and
    stores them in a dictionary using a specified key."""
    split_text = text.split(",")
    data = json.loads(context.api_response)
    if not hasattr(context.config, 'userdata_dict_api_response'):
        context.config.userdata_dict_api_response = {}
    local_dict_api_response = {}

    for i in range(len(split_text)):
        value = ""
        if '.' in split_text[i]:
            split_dot = split_text[i].split(".")
            if len(split_dot) == 2:
                value = data[split_dot[0]][split_dot[1]]
            elif len(split_dot) == 3:
                value = data[split_dot[0]][split_dot[1]][split_dot[2]]
            elif len(split_dot) == 4:
                value = data[split_dot[0]][split_dot[1]][split_dot[2]][split_dot[3]]
        else:
            value = data.get(split_text[i], None)
        dict_key = key + "." + split_text[i]
        local_dict_api_response[dict_key] = value
        logger.info(context, "key: " + str(dict_key) + ",value: " + str(value))
    context.dict_api_response = local_dict_api_response
    context.config.userdata_dict_api_response.update(local_dict_api_response)


def get_api_response_value(context, text):
    """This method replaces placeholders in a text with corresponding values from the API response dictionary."""
    try:
        combined_dict = {}
        if hasattr(context.config, 'userdata_dict_api_response'):
            combined_dict.update(context.config.userdata_dict_api_response)
        combined_dict.update(context.dict_api_response)

        for key, value in combined_dict.items():
            if f"@{key}" in text:
                try:
                    int(value)
                    if f'"@{key}"' in text:
                        text = text.replace(f'"@{key}"', value)
                    else:
                        text = text.replace(f"@{key}", value)
                except ValueError:
                    text = text.replace(f"@{key}", value)
        return text
    except Exception:
        return text


def execute_api_and_verify_response(context, verification_criteria):
    """This method executes an API request and verifies the response based on the method type and expected status codes."""
    verified = False
    content = ""
    api_url, method_type, request_parameter, api_headers = None, None, None, None
    oauth2, basic_auth = None, None
    if context.api_url is not None:
        api_url = context.api_url
    if context.method_type is not None:
        method_type = context.method_type
    try:
        if context.request_payload is not None:
            request_parameter = context.request_payload
    except AttributeError:
        print()
    if context.api_header is not None:
        api_headers = context.api_header
    response = requests.request('GET', api_url, headers=api_headers)
    if api_headers is not None and 'IMAGE / PNG' in api_headers and method_type.upper() == 'GET':
        try:
            res_code = response.status_code
            if res_code in (200, 201, 202):
                verified = True
                print('Refer to the attached image to check output.')
            image = response.content
            base64_string = base64.b64encode(image).decode('utf-8')
        except Exception as e:
            print('Error------------', e)
            verified = False
        return verified
    else:
        requests.packages.urllib3.disable_warnings()
        headers = {}
        if basic_auth is not None:
            basic_auth_split = basic_auth.split(',')
            auth = (basic_auth_split[0], basic_auth_split[1])
            headers['Authorization'] = 'Basic ' + (basic_auth_split[0] + ':' + basic_auth_split[1]).encode(
                'base64').rstrip()
        if str(method_type.lower()) == 'post':
            response = requests.post(api_url, data=request_parameter, headers=api_headers)
        elif str(method_type.lower()) == 'get':
            response = requests.get(api_url, headers=api_headers)
        elif str(method_type.lower()) == 'put':
            response = requests.put(api_url, data=request_parameter, headers=api_headers)
        elif str(method_type.lower()) == 'delete':
            response = requests.delete(api_url, headers=api_headers)
        elif str(method_type.lower()) == 'patch':
            response = requests.patch(api_url, data=request_parameter, headers=api_headers)
        numeric_status_code = response.status_code
        content = "Status code: " + str(numeric_status_code) + "  Response: " + response.text
        all_headers = str(response.headers)
        context.api_all_headers = all_headers
        context.api_response = response.text
        logger.info(context, context.api_response)
        if verification_criteria.upper() == 'VERIFY_NEGATIVE'.upper() and numeric_status_code in [400, 500,
                                                                                                        401, 415,
                                                                                                        000]:
            logger.info(context, str(numeric_status_code))
            verified = True
        elif numeric_status_code in [201, 200, 202, 204]:
            logger.info(context, str(numeric_status_code))
            verified = True
        else:
            print('Unsuccessful response. Status code:', numeric_status_code)
            verified = False
        if isinstance(verification_criteria, str):
            split_array = verification_criteria.split(",")
            for item in split_array:
                if item in content:
                    verified = True
                    logger.info(context, f"{item} is verified in API output.")
                else:
                    verified = False
                    logger.info(context, f"{item} is not verified in API output.")
                    break
        return verified


def verify_response_header(context, param):
    try:
        header_list = context.api_header
        param = param.split(':')
        for item in param:
            if item in header_list or item in header_list.values():
                logger.info(context, "Verified response header : " + str(item))
                return True
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False


def verify_api_response(context, param):
    api_url, method_type, request_parameter, api_headers = None, None, None, None
    if context.api_url is not None:
        api_url = context.api_url
    if context.method_type is not None:
        method_type = context.method_type
    if context.api_header is not None:
        api_headers = context.api_header
    try:
        response = requests.request(method_type, api_url, headers=api_headers)
        res_code = response.status_code
        if param == res_code:
            return True
        elif res_code in (200, 201, 202):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False