PI = 22 / 7  # estimation of pi

# A stateful variable to be used by sample_function.
# This is dangerous and not considered good practice, but possible nonetheless.
_prev_arg = None

def sample_function(some_arg):
    print("Hello there from the file samplemodule.py! Here is your argument as a string:", some_arg)
    global _prev_arg
    if _prev_arg is not None:
        print("This was the previous argument:", _prev_arg)
    _prev_arg = some_arg


class SampleClass:
    def __init__(self, value):
        self.value = value

    def print_value(self):
        print(self.value)

    def _hidden_method(self):
        """Not to be used outside this class and module!"""
        print("Did you just call the hidden method?")
