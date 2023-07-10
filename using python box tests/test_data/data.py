from box import Box
import sys

sys.path.append('...')
from snipe_it_app.snipe_it_functions import PER_PAGE

test_data = {"test_snipe_client": {"input": {"url": "http://127.0.0.1:8000",
                                             "auth_token": "abcdefghijk"},
                                   "output": {"auth": 'Bearer abcdefghijk',
                                              }},
             "test_make_https_get_request": {"input": {"url": "http://abcd",
                                                       "content": {"total": 123, "row": [{"a": "b"}, {"c": "d"}]}},
                                             "output": {"result": {"total": 123, "row": [{"a": "b"}, {"c": "d"}]}}
                                             },
             "test_create_items": {"input": {"result": {"total": 6, "rows": [{"a": "b"}, {"c": "d"}, {"e": "f"}]},
                                             "type_name": "Assets"},
                                   "output": {"item": [{"type": "Assets", "content": {"a": "b"}},
                                                       {"type": "Assets", "content": {"c": "d"}},
                                                       {"type": "Assets", "content": {"e": "f"}}]}},
             "test_get_assets": {"input": {"full_url1": f"http://abcd.io/api/v1/hardware?limit={PER_PAGE}&offset=0",
                                           "full_url2": f"http://abcd.io/api/v1/hardware?limit={PER_PAGE}&offset=2",
                                           "content1": {"total": 3, "rows": [{"a": "b"}, {"c": "d"}]},
                                           "content2": {"total": 3, "rows": [{"a": "b"}]},
                                           "url": "http://abcd.io"},
                                 "output": {"items1": [{'type': 'SnipeitAsset', 'content': {'a': 'b'}},
                                                       {'type': 'SnipeitAsset', 'content': {'c': 'd'}}],
                                            "items2": [{'type': 'SnipeitAsset', 'content': {'a': 'b'}}]
                                            }},
             "test_get_companies": {"input": {"full_url1": f"http://abcd.io/api/v1/companies?limit={PER_PAGE}&offset=0",
                                              "full_url2": f"http://abcd.io/api/v1/companies?limit={PER_PAGE}&offset=2",
                                              "content1": {"total": 4, "rows": [{"a": "b"}, {"c": "d"}]},
                                              "content2": {"total": 4, "rows": [{"a": "b"}, {"c": "d"}]},
                                              "url": "http://abcd.io"},
                                    "output": {"items1": [{'type': 'SnipeitCompany', 'content': {'a': 'b'}},
                                                          {'type': 'SnipeitCompany', 'content': {'c': 'd'}}],
                                               "items2": [{'type': 'SnipeitCompany', 'content': {'a': 'b'}},
                                                          {'type': 'SnipeitCompany', 'content': {'c': 'd'}}]
                                               }},
             "test_get_locations": {"input": {"full_url1": f"http://abcd.io/api/v1/locations?limit={PER_PAGE}&offset=0",
                                              "full_url2": f"http://abcd.io/api/v1/locations?limit={PER_PAGE}&offset=3",
                                              "content1": {"total": 5, "rows": [{"a": "b"}, {"a": "b"}, {"c": "d"}]},
                                              "content2": {"total": 5, "rows": [{"a": "b"}, {"c": "d"}]},
                                              "url": "http://abcd.io"},
                                    "output": {"items1": [{'type': 'SnipeitLocation', 'content': {'a': 'b'}},
                                                          {'type': 'SnipeitLocation', 'content': {'a': 'b'}},
                                                          {'type': 'SnipeitLocation', 'content': {'c': 'd'}},
                                                          ],
                                               "items2": [{'type': 'SnipeitLocation', 'content': {'a': 'b'}},
                                                          {'type': 'SnipeitLocation', 'content': {'c': 'd'}}]
                                               }},
             "test_get_users": {"input": {"full_url1": f"http://abcd.io/api/v1/users?limit={PER_PAGE}&offset=0",
                                          "full_url2": f"http://abcd.io/api/v1/users?limit={PER_PAGE}&offset=1",
                                          "content1": {"total": 2, "rows": [{"a": "b"}]},
                                          "content2": {"total": 2, "rows": [{"a": "b"}]},
                                          "url": "http://abcd.io"},
                                "output": {"items1": [{'type': 'SnipeitUser', 'content': {'a': 'b'}}
                                                      ],
                                           "items2": [{'type': 'SnipeitUser', 'content': {'a': 'b'}}]
                                           }},
             "test_connection_positive": {"input": {"full_url":f"http://abcd.io/api/v1/hardware?limit={PER_PAGE}&offset=0",
                                                    "url":"http://abcd.io"},
                                          "output": {}},

             "test_connection_negative": {
                 "input": {"full_url": f"http://abcd.io/api/v1/hardware?limit={PER_PAGE}&offset=0",
                           "url": "http://abcd.io"},
                 "output": {}}
             }
test_data = Box(test_data)
