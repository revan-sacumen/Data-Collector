import logging

import pytest
import requests
import responses
from .utility import get_logger, get_test_input_data, get_test_output_data, set_responses
import sys

sys.path.append('..')
from snipe_it_app.snipe_it_functions import SnipeitClient, get_assets, get_users, get_locations, \
    get_companies, PER_PAGE

from noetic_connector_api import MoreDataManager, NO_MORE_DATA

# from snipe_it.snipe_it_app.snipe_it_functions import SnipeitClient, get_assets, get_users, get_locations, \
#     get_companies, PER_PAGE

logger = get_logger()


def test_snipe_client():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url=input_data.url,auth_token=input_data.auth_token)
    assert isinstance(sc.log, logging.Logger)
    assert sc.more_data == more_data
    assert isinstance(sc.session, requests.Session)
    assert sc.session.headers.get('Authorization') == output_data.auth
    assert sc.base_url == input_data.url


def test_snipe_client_no_url():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    with pytest.raises(ValueError):
        SnipeitClient(log=logger, more_data=more_data, base_url="",
                      auth_token="abcd")


def test_snipe_client_no_auth():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    with pytest.raises(ValueError):
        SnipeitClient(log=logger, more_data=more_data, base_url="abcd",
                      auth_token="")


def test_snipe_client_invalid_url():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    # with pytest.raises(ValueError):
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="abcd",
                       auth_token="abcd")
    assert sc.base_url == '://'
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd",
                       auth_token="abcd")
    assert sc.base_url == 'http://abcd'


def test_create_session():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd",
                       auth_token="abcd")
    assert sc.session.headers.get("Authorization") == "Bearer abcd"
    session = sc.create_session(auth_token="abcdef")
    assert session.headers.get("Authorization") == "Bearer abcdef"


def test_create_session_empty_auth():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    with pytest.raises(requests.HTTPError):
        SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd",
                      auth_token="   ")


def test_get_complete_url():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd",
                       auth_token="hdcb")
    url = sc.get_complete_url(paths="efgh", args={"a": 1, "b": 236})
    assert url == "http://abcd/efgh?a=1&b=236"


def test_get_complete_url_no_input():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd",
                       auth_token="hdcb")
    url = sc.get_complete_url()
    assert url == "http://abcd"


@responses.activate
def test_make_https_get_request():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.url, content=dict(input_data.content), status=200)
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url=input_data.url, auth_token="hdcb")
    result = sc.make_https_get_request(url=input_data.url)
    assert result == dict(output.result)


def test_validate_result():
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd", auth_token="hdcb")
    with pytest.raises(requests.HTTPError):
        sc.validate_result(result={"status": 405, "messages": "Method Not Allowed"})


def test_set_new_offset():
    # default
    result1 = {"total": 6, "rows": [{"a": "b"}, {"a": "b"}, {"a": "b"}]}
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd", auth_token="hdcb")
    sc.set_new_offset(result=result1)
    assert sc.more_data.get(default=0) == 3
    # next run
    sc.set_new_offset(result=result1)
    assert sc.more_data.get(default=0) == -1


def test_create_items():
    input_data = get_test_input_data()
    output_data = get_test_output_data()
    more_data = MoreDataManager(logger, more_data={}, key="test")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url="http://abcd", auth_token="hdcb")
    items = sc.create_items(result=input_data.result, type_name=input_data.type_name)
    assert items == list(output_data.item)


@responses.activate
def test_get_assets():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.full_url1, content=dict(input_data.content1), status=200)
    set_responses(method="GET", url=input_data.full_url2, content=dict(input_data.content2), status=200)
    more_data = MoreDataManager(logger, more_data={}, key="test_get_assets")
    sc = SnipeitClient(log=logger, more_data=more_data, base_url=input_data.url, auth_token="hdcb")
    items = sc.get_assets()
    assert items == output.items1
    items = sc.get_assets()
    assert items == output.items2


@responses.activate
def test_get_assets():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.full_url1, content=dict(input_data.content1), status=200)
    set_responses(method="GET", url=input_data.full_url2, content=dict(input_data.content2), status=200)
    result = get_assets(__user_log=logger, more_data={}, snipe_it_base_url=input_data.url, snipe_it_auth_token="hdcb")
    assert result['items'] == list(output.items1)
    if result['more_flag']:
        result = get_assets(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                            snipe_it_auth_token="hdcb")
        assert result['items'] == output.items2
        assert not result['more_flag']
        assert result.get("more_data").get("snipe_it_app.snipe_it_functions:get_assets") == NO_MORE_DATA
    else:
        assert False


@responses.activate
def test_get_assets():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.full_url1, content=dict(input_data.content1), status=200)
    set_responses(method="GET", url=input_data.full_url2, content=dict(input_data.content2), status=200)
    result = get_assets(__user_log=logger, more_data={}, snipe_it_base_url=input_data.url, snipe_it_auth_token="hdcb")
    assert result['items'] == list(output.items1)
    if result['more_flag']:
        result = get_assets(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                            snipe_it_auth_token="hdcb")
        assert result['items'] == output.items2
        assert not result['more_flag']
        assert result.get("more_data").get("snipe_it_app.snipe_it_functions:get_assets") == NO_MORE_DATA
        result = get_assets(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                            snipe_it_auth_token="hdcb")
        assert result['items'] == []
    else:
        assert False


@responses.activate
def test_get_companies():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.full_url1, content=dict(input_data.content1), status=200)
    set_responses(method="GET", url=input_data.full_url2, content=dict(input_data.content2), status=200)
    result = get_companies(__user_log=logger, more_data={}, snipe_it_base_url=input_data.url,
                           snipe_it_auth_token="hdcb")
    assert result['items'] == list(output.items1)
    if result['more_flag']:
        result = get_companies(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                               snipe_it_auth_token="hdcb")
        assert result['items'] == output.items2
        assert not result['more_flag']
        assert result.get("more_data").get("snipe_it_app.snipe_it_functions:get_companies") == NO_MORE_DATA
        result = get_companies(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                               snipe_it_auth_token="hdcb")
        assert result['items'] == []
    else:
        assert False


@responses.activate
def test_get_locations():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.full_url1, content=dict(input_data.content1), status=200)
    set_responses(method="GET", url=input_data.full_url2, content=dict(input_data.content2), status=200)
    result = get_locations(__user_log=logger, more_data={}, snipe_it_base_url=input_data.url,
                           snipe_it_auth_token="hdcb")
    assert result['items'] == list(output.items1)
    if result['more_flag']:
        result = get_locations(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                               snipe_it_auth_token="hdcb")
        assert result['items'] == output.items2
        assert not result['more_flag']
        assert result.get("more_data").get("snipe_it_app.snipe_it_functions:get_locations") == NO_MORE_DATA
        result = get_locations(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                               snipe_it_auth_token="hdcb")
        assert result['items'] == []
    else:
        assert False


@responses.activate
def test_get_users():
    input_data = get_test_input_data()
    output = get_test_output_data()
    set_responses(method="GET", url=input_data.full_url1, content=dict(input_data.content1), status=200)
    set_responses(method="GET", url=input_data.full_url2, content=dict(input_data.content2), status=200)
    result = get_users(__user_log=logger, more_data={}, snipe_it_base_url=input_data.url, snipe_it_auth_token="hdcb")
    assert result['items'] == list(output.items1)
    if result['more_flag']:
        result = get_users(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                           snipe_it_auth_token="hdcb")
        assert result['items'] == output.items2
        assert not result['more_flag']
        assert result.get("more_data").get("snipe_it_app.snipe_it_functions:get_users") == NO_MORE_DATA
        result = get_users(__user_log=logger, more_data=result["more_data"], snipe_it_base_url=input_data.url,
                           snipe_it_auth_token="hdcb")
        assert result['items'] == []
    else:
        assert False


@responses.activate
def test_connection_positive():
    input_data = get_test_input_data()
    output = get_test_output_data()
    from snipe_it_app.snipe_it_functions import test_connection
    set_responses(method="GET", url=input_data.full_url, content={}, status=200)
    more_data = MoreDataManager(logger, more_data={}, key="test_connection_positive")
    result = test_connection(__user_log=logger, more_data=more_data, snipe_it_base_url=input_data.url,
                             snipe_it_auth_token="hdcb")
    assert result.get("status") == "success"


def test_connection_negative():
    input_data = get_test_input_data()
    from snipe_it_app.snipe_it_functions import test_connection
    set_responses(method="GET", url=input_data.full_url, content={}, status=200)
    more_data = MoreDataManager(logger, more_data={}, key="test_connection_positive")
    with pytest.raises(requests.HTTPError):
        test_connection(__user_log=logger, more_data=more_data, snipe_it_base_url=input_data.url,
                        snipe_it_auth_token="hdcb")
