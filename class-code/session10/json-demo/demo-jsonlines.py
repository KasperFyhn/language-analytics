import jsonlines
import pandas as pd

# we create a Reader object for the JSONL file such that we can loop over them
with jsonlines.open('examples.jsonl') as reader:
    for obj in reader:
        # do something with obj
        print(obj)

print()

# the reader object is a generator, not a list.
# this means that it gives you one object, then moves on to the next.
# therefore, it will be "exhausted" after having looped over all.
# to store them, you can convert the generator to a list
print("Saving all entries in a list variable")
with jsonlines.open('examples.jsonl') as reader:
    objs = list(reader)
    print("Objects in list:", len(objs))

print()

# pandas also knows how to work with JSON
df = pd.read_json('/work/examples.jsonl', lines=True)
print(df.head())

print()

# but the layout of pandas as a "table" and the nesting options in JSON do not mix well, especially with deep nesting
df = pd.read_json('examples-nested.jsonl', lines=True)
print(df.head())