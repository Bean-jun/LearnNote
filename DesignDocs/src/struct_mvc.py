# 模型-视图-控制器模式
class Model:

    def __init__(self):
        self.data = []

    def get(self):
        return self.data
    
    def add(self, data):
        self.data.append(data)
        return self.data

class View:

    def show(self, data):
        for i in data:
            print(f"view: {i}")

class Controller:

    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            i = input("please input to view! input q exit:\n")
            i = i.rstrip("\n")
            if i == "q":
                break
            self.model.add(i)
            data = self.model.get()
            self.view.show(data)


if __name__ == "__main__":
    c = Controller()
    c.run()