# For something like top-k sampling, you may find yourself in need of sorting a list
# based on a another value than the entry itself.

# That is, you have a situation that looks a bit like this

a_dict = {"a": 1, "b": 2, "c": 4, "d": 3}

# To get the key-value pairs a list-like object, you can do
print(a_dict.items())

# To sort such a list-like object of tuples, you can do the following
print(sorted(a_dict.items()))

# To sort it by the value, you can do like this
print(sorted(a_dict.items(), key=lambda x: x[1]))

# To reverse sort it, set the reverse argument to True
print(sorted(a_dict.items(), key=lambda x: x[1], reverse=True))
