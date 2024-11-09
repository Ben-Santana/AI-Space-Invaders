class Obstacle:
    # @params
    #  - draw_function : a function that takes in screen and the obstacle and draws it
    #  - update_function : a function that takes in the obstacle and updates it
    
    def __init__(self, x, y, draw_function, update_function):
        self.x = x
        self.y = y

        self.draw_function = draw_function
        self.update_function = update_function
    
    def draw(self):
        try:
            self.draw_function(self)
        except Exception as e:
            pass

    def update(self):
        try:
            self.update_function(self)
        except Exception as e:
            pass      