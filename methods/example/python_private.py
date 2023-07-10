from faker import Faker

faker = Faker()

class FakerTestClass:
    def instance_method(self) -> dict:
        return {
            "firstname": "Revan",
            "lastname":"More"
        }
    def __fullname(self) -> str:
        dict_data: dict = self.instance_method()
        fullname: str = str(dict_data.get('firstname', None)+" "+dict_data.get("lastname", None))
        return fullname


obj = FakerTestClass()

obj_ = obj._FakerTestClass__fullname()
print(obj_)


         