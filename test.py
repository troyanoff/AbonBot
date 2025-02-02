
import orjson

from pydantic import BaseModel

class test_child(BaseModel):
    name: str

class test(BaseModel):
    name: str
    child: test_child

m = test_child(name='3432')
v = test(name='124', child=m)

l = orjson.dumps(v.model_dump_json())

print(l)

l_ = orjson.loads(l)

print(l_)
