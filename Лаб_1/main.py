import tkinter
import math


class BezierLines(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self.centerWindow()

    def initUI(self):
        self.master.title("Кривые Безье")
        self.points = []
        self.brush_size = 3
        self.color = "black"

        self.canvas_height = 600
        self.canvas_width = 1000
        self.cnv = tkinter.Canvas(self, bg="white", width=self.canvas_width, height=self.canvas_height,
                                  relief="raised", selectborderwidth=10)
        self.cnv.pack(fill=tkinter.BOTH, expand=True)

        self.pack(fill=tkinter.BOTH, expand=True)

        clear_button = tkinter.Button(self, text="Clear", command=self.clearAll)
        clear_button.pack(side=tkinter.RIGHT, padx=5, pady=5)

        draw_button = tkinter.Button(self, text="Draw", command=self.drawLines)
        draw_button.pack(side=tkinter.RIGHT)

        self.cnv.bind("<Button-1>", self.drawPoint)

    def centerWindow(self):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        window_height = 700

        x = (sw - self.canvas_width) / 2
        y = (sh - window_height) / 2

        self.parent.geometry('%dx%d+%d+%d' % (self.canvas_width, window_height, x, y))

    def drawPoint(self, event):

        self.points.append((event.x, event.y))

        x1 = event.x - self.brush_size
        x2 = event.x + self.brush_size
        y1 = event.y - self.brush_size
        y2 = event.y + self.brush_size

        self.cnv.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)

    def drawLine(self, p1, p2, p3, p4):
        t = 0.001
        while t <= 1:
            point = (self.calcBezierCoordinate(p1[0], p2[0], p3[0], p4[0], t),
                     self.calcBezierCoordinate(p1[1], p2[1], p3[1], p4[1], t))
            x1 = point[0] - self.brush_size + 2
            x2 = point[0] + self.brush_size - 2
            y1 = point[1] - self.brush_size + 2
            y2 = point[1] + self.brush_size - 2

            self.cnv.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)

            t += 0.001

            self.after(1)
            self.update()

    def drawLines(self):
        next_p = self.points[0]
        for i in range(len(self.points) - 2):  # должно быть 2
            aj1 = ((self.points[i][0] + self.points[i + 1][0]) / 2, (self.points[i][1] + self.points[i + 1][1]) / 2)
            aj2 = (
            (self.points[i + 1][0] + self.points[i + 2][0]) / 2, (self.points[i + 1][1] + self.points[i + 2][1]) / 2)

            lam = self.ratioOfSegments(self.points[i], self.points[i + 1], self.points[i + 2])
            bj = ((aj1[0] + lam * aj2[0]) / (1 + lam), (aj1[1] + lam * aj2[1]) / (1 + lam))

            pi1 = (aj1[0] - bj[0] + self.points[i + 1][0], aj1[1] - bj[1] + self.points[i + 1][1])
            pi2 = (aj2[0] - bj[0] + self.points[i + 1][0], aj2[1] - bj[1] + self.points[i + 1][1])

            self.drawLine(self.points[i], next_p, pi1, self.points[i + 1])

            next_p = pi2

            self.cnv.create_oval(aj1[0] - 3, aj1[1] - 3, aj1[0] + 3, aj1[1] + 3, fill="blue", outline="blue")
            self.cnv.create_oval(aj2[0] - 3, aj2[1] - 3, aj2[0] + 3, aj2[1] + 3, fill="blue", outline="blue")
            self.cnv.create_oval(bj[0] - 3, bj[1] - 3, bj[0] + 3, bj[1] + 3, fill="green", outline="green")
            self.cnv.create_oval(pi1[0] - 3, pi1[1] - 3, pi1[0] + 3, pi1[1] + 3, fill="purple", outline="purple")
            self.cnv.create_oval(pi2[0] - 3, pi2[1] - 3, pi2[0] + 3, pi2[1] + 3, fill="purple", outline="purple")

            self.cnv.create_line(aj1, aj2, fill="green", width=self.brush_size - 2)
            self.cnv.create_line(pi1, pi2, fill="purple", width=self.brush_size - 2)
            self.cnv.create_line(self.points[i], self.points[i + 1], fill="blue", width=self.brush_size - 2)

        self.drawLine(self.points[-2], next_p, self.points[-1], self.points[-1])
        self.cnv.create_line(self.points[-2], self.points[-1], fill="blue", width=self.brush_size - 2)

    def clearAll(self):
        self.cnv.delete("all")
        self.points = []

    def ratioOfSegments(self, p1, p2, p3):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / math.hypot(p3[0] - p2[0], p3[1] - p2[1])

    def calcBezierCoordinate(self, c1, c2, c3, c4, t):
        return t ** 3 * (c4 - 3 * c3 + 3 * c2 - c1) + t ** 2 * (3 * c1 - 6 * c2 + 3 * c3) + t * (3 * c2 - 3 * c1) + c1


if __name__ == '__main__':
    root = tkinter.Tk()
    app = BezierLines(root)
    root.mainloop()
