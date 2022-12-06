import turtle


class LSystem2D:
    def __init__(self, axiom, width, length, angle):
        self.axiom = axiom
        self.state = axiom
        self.width = width
        self.length = length
        self.angle = angle
        self.rules = {}
        self.t = turtle.Turtle()
        self.t.ht()
        self.t.pensize(self.width)

    def add_rules(self, *rules):
        for key, value in rules:
            self.rules[key] = value

    def generate_path(self, n_iter):
        for n in range(n_iter):
            for key, value in self.rules.items():
                self.state = self.state.replace(key, value.lower())

            self.state = self.state.upper()

    def set_turtle(self, my_tuple):
        self.t.up()
        self.t.goto(my_tuple[0], my_tuple[1])
        self.t.seth(my_tuple[2])
        self.t.down()

    def draw_turtle(self, start_pos, start_angle):
        turtle.tracer(1, 0)
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        turtle_stack = []

        for move in self.state:
            if move == "F":
                self.t.forward(self.length)
            elif move == "S":
                self.t.up()
                self.t.forward(self.length)
                self.t.down()
            elif move == "+":
                self.t.left(self.angle)
            elif move == "-":
                self.t.right(self.angle)
            elif move == "[":
                turtle_stack.append((self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
            elif move == "]":
                xcor, ycor, head, w = turtle_stack.pop()
                self.set_turtle((xcor, ycor, head))
                self.width = w
                self.t.pensize(self.width)

        turtle.done()


def draw_snowflake():
    pen_width = 2
    f_len = 8
    angle = 60
    axiom = "F--F--F"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "F+F--F+F"))
    l_sys.generate_path(4)
    l_sys.draw_turtle((-300, 200), 0)


def draw_dragon():
    pen_width = 2
    f_len = 8
    angle = 90
    axiom = "FX"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("FX", "FX+FY+"), ("FY", "-FX-FY"))
    l_sys.generate_path(12)
    l_sys.draw_turtle((200, -100), 0)


def draw_carpet():
    pen_width = 2
    f_len = 8
    angle = 60
    axiom = "FXF--FF--FF"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "FF"), ("X", "--FXF++FXF++FXF--"))
    l_sys.generate_path(5)
    l_sys.draw_turtle((200, -200), -180)


def draw_gilbert():
    pen_width = 2
    f_len = 7
    angle = 90
    axiom = "X"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("X", "-YF+XFX+FY-"), ("Y", "+XF-YFY-FX+"))
    l_sys.generate_path(6)
    l_sys.draw_turtle((200, -200), -180)


def draw_tree1():
    pen_width = 2
    f_len = 7
    angle = 25.7
    axiom = "F"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "F[+F]F[-F]F"))
    l_sys.generate_path(4)
    l_sys.draw_turtle((0, -300), 90)


def draw_tree2():
    pen_width = 2
    f_len = 15
    angle = 20
    axiom = "F"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "F[+F]F[-F][F]"))
    l_sys.generate_path(4)
    l_sys.draw_turtle((0, -300), 90)


def draw_tree3():
    pen_width = 2
    f_len = 5
    angle = 25.7
    axiom = "X"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "FF"), ("X", "F[+X][-X]FX"))
    l_sys.generate_path(6)
    l_sys.draw_turtle((0, -300), 90)


def draw_tree4():
    pen_width = 2
    f_len = 50
    angle = 20
    axiom = "F"

    l_sys = LSystem2D(axiom, pen_width, f_len, angle)
    l_sys.add_rules(("F", "-F[-F+F-F]+[+F-F-F]"))
    l_sys.generate_path(3)
    l_sys.draw_turtle((0, -300), 150)


if __name__ == "__main__":
    width = 1400
    height = 900
    screen = turtle.Screen()
    screen.setup(width, height, 0, 0)

    draw_tree4()
