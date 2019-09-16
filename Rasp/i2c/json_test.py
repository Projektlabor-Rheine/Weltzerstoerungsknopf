import json
from enum import Enum
from io import StringIO

arr = ["leul", 5]

class Commands(Enum):
    Foo = 1
    Bar = 2

data = {}
data[Commands.Bar.name] = Commands.Bar.value
json_data = json.dumps(data)

print(json_data)

jsonobj = json.loads('{"2":[2,3,"leeil"]}')
print(next(iter(jsonobj), None))
print(next(iter(jsonobj), None))

print("zeilelul")

for item in jsonobj:
    print(item)
    print(jsonobj[item])
    print(jsonobj[item][0])

print(jsonobj)


