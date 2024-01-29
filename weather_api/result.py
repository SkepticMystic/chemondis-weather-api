# This file implements a Result class, to build tagged unions.
# See here for more info: https://en.wikipedia.org/wiki/Tagged_union
# In this version, a boolean flag `ok` is used to differentiate
# between the two possible states of `ok` and `err`.

class Result:
    ok: bool
    data: any

    def __init__(self, ok: bool, data: any):
        self.ok = ok
        self.data = data

    def log(self, prefix: str = ""):
        if (self.ok):
            print(prefix, "ok:", self.data)
        else:
            print(prefix, "err:", self.data)

    def json(self):
        return {
            "ok": self.ok,
            "data": self.data
        }


# Helper functions to create particular instances of Result
def err(data: any):
    return Result(False, data)


def ok(data: any):
    return Result(True, data)
