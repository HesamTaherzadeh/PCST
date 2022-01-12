from tkinter import ttk
from tkinter.ttk import Treeview, Combobox, Style
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sympy as sp
from sklearn.cluster import KMeans
import itertools
from IPython.display import Math, display
from tkinter import *
from global_poly import Regression
from io import BytesIO
from Canvas import Canvas_it


class Globalpolynomial():
    def __init__(self, df_gcp, df_icp, root,obj, imagei, utmi):
        self.utmi = utmi
        self.imagei = imagei
        self.obj = obj
        self.root = root
        self.df_gcp = df_gcp
        self.df_icp = df_icp
        self.main_window = Frame(self.root, bg='#2874a1', width=920, height=700, relief=SUNKEN)
        self.main_window.grid(row=0, column=0, sticky=S)
        self.n = None
        self.bcommand()
        comp = Button(self.main_window, text="compute", width=10, height=5, bg="powder blue",command=self.compute)
        comp.place(x=0, y=0)

    def bcommand(self):
        ttk.Label(self.main_window, text="Select the order :",
                  font=("Times New Roman", 10)).place(x=(920/2) - 100, y=240)
        n = StringVar()
        self.order = Combobox(self.main_window, width=27, textvariable = n)
        self.order['values'] = list(map(str, range(20)))
        self.order.place(x=(920/2) - 100, y=258)
        self.order.current()


    def compute(self):
        self.n = self.order.get()
        digitized, utm = self.df_gcp.iloc[:, :2], self.df_gcp.iloc[:, 2:]
        x_utm = np.array(utm['E']).T
        y_utm = np.array(utm['N']).T
        x_digitized = np.array(digitized['x']).T
        y_digitized = np.array(digitized['y']).T
        a, b = self.obj.create_A(int(self.n), np.vstack([x_digitized,y_digitized]).T)
        x_coeff, y_coeff, df_coef = self.obj.least_square(a, x_utm, y_utm)
        exprx, expry = self.obj.expression(x_coeff,y_coeff)
        funcx, funcy = self.obj.numpyit(exprx, expry)
        self.functionx, self.functiony = funcx, funcy
        xscom = funcx(self.imagei['x'],self.imagei['y'])
        yscom = funcy(self.imagei['x'],self.imagei['y'])
        self.xcalc, self.ycalc = xscom, yscom
        calc = np.vstack([xscom, yscom]).T
        rm,_,_,mae, fig = self.obj.rmse(calc, np.array(self.utmi))
        result_gw = Toplevel(self.main_window)
        result_gw.title("Residual vector map")
        result_gw.geometry("1000x800")
        canvas_object = Canvas_it(result_gw, fig)
        canvas_object.locate(0,0)
        result_gw.resizable(False, False)
        result_gw.mainloop()

    def pass_out(self):
        return self.functionx, self.functiony, self.df_gcp['x'],\
               self.df_gcp['y'], self.df_gcp['E'], self.df_gcp['N'], self.xcalc, self.ycalc



