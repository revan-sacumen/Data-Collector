import sys

sys.path.extend("./methods/example")
from methods.example.python_private import FakerTestClass

obj = FakerTestClass()
def test_faker_name():
    actul_name = obj._FakerTestClass__fullname()
    assert actul_name == "Revan More"

