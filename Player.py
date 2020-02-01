
class Player:

    def __init__(self):
        pass

    def move(self, state):
        split = input("Input Move: ").split(",")
        return (int(split[0]), int(split[1]))
