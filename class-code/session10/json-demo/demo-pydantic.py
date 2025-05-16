from pydantic import BaseModel

# pydantic

class NestedObject(BaseModel):
    """Definition of the nested object of an entry in examples-nested.jsonl."""
    key: str

class Entry(BaseModel):
    """Definition of an entry in examples-nested.jsonl."""
    id: int
    name: str
    someObject: NestedObject
    someList: list[int]


entries = []
with open("examples-nested.jsonl") as f:
    for line in f:
        # an object can be load from a JSON string
        entry = Entry.model_validate_json(line)
        entries.append(entry)

print("Number of entries:", len(entries))

print()

# they are now as any other object (with some special properties), so you can access attributes
first_entry = entries[0]
print("First entry:\n", first_entry)
print("ID of first entry:", first_entry.id)
print("Name of first entry:", first_entry.name)

print()

# all names
print("All names:", [entry.name for entry in entries])
