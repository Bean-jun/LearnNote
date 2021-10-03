try:
    from greenlet import getcurrent as get_ident
except Exception as e:
    from threading import get_ident


class MyLocal():

    def __init__(self):
        super().__setattr__("storage", {})

    def __setattr__(self, name, value):
        id = get_ident()
        if id in self.storage:
            self.storage[id][name] = value
        else:
            self.storage[id] = {name: value}

    def __getattr__(self, name):
        id = get_ident()
        return self.storage[id][name]
