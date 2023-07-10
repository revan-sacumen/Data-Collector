"""Utility file holds common help functions which will be used in test cases."""
import sys
import logging
import requests  # type: ignore
import responses

from .test_data.data import test_data


def get_test_input_data(func_name=''):
    """Get the input data for test cases from test_data file.

    :param func_name: name of the key (function)
    :return: data with key input under function name key
    """
    code = sys._getframe(1).f_code
    if not func_name:
        func_name = code.co_name
    return test_data[func_name]['input']


def get_test_output_data(func_name=''):
    """Get the output data for test cases from test_data file.

    :param func_name: name of the key (function)
    :return: data with key output under function name key
    """
    code = sys._getframe(1).f_code
    if not func_name:
        func_name = code.co_name
    return test_data[func_name]['output']


def get_logger():
    """Create the logger object.

    :return: looger object
    """
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    return logging.getLogger('test_cb')


def set_responses(method, url, content, status):
    """For the given url http_method sets the json response and status code as per input."""
    responses.add(method, url, json=content, status=status)
    # responses.add(method, url, body=content, status=status)
