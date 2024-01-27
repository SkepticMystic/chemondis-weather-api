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


def err(data: any):
    return Result(False, data)


def ok(data: any):
    return Result(True, data)
