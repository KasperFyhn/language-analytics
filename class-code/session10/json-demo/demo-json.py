import json

# you can load a full file
print("Loading JSON with json.load()")
with open("example.json") as f:
    json_object = json.load(f)
    print("Type:", type(json_object))
    print(json_object)
    # they are dicts, so you can access values by looking up the key
    print("Value of 'anInteger' in the dict:", json_object["anInteger"])

print()

# you can also load it from a string, e.g. if you do not get it from a file
print("Loading JSON with json.loads()")
with open("example.json") as f:
    json_str = f.read()
    json_object = json.loads(json_str)
    print("Type:", type(json_object))
    print(json_object)

print()

# you can also dump the json object to a string or file
print("Dumping with json.dumps()")
dumped_str = json.dumps(json_object)
print("Type:", type(dumped_str))
print(dumped_str)

print()

# or directly to a file
print("Dumping with json.dump(); example_dumped.json should appear in the folder")
with open("example_dumped.json", "w+") as f:
    json.dump(json_object, f)