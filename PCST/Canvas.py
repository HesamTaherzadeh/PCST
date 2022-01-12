from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Canvas_it():
    def __init__(self, window, figure):
        self.window = window
        self.figure = figure

    def locate(self, x, y, *args):
        shape = FigureCanvasTkAgg(self.figure, self.window)
        return shape.get_tk_widget().place(x=x, y=y, *args)
    def destroy(self):
        self.figure.clear()

