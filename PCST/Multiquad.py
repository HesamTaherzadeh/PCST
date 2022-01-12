import numpy as np
from tkinter import *
from global_poly import Regression
from Canvas import Canvas_it
import matplotlib.pyplot as plt
from tkinter.ttk import Treeview
from tkinter import filedialog
from open_excel import Open
from PIL import Image, ImageTk
from gpoly import Globalpolynomial
from IPython.display import Math, display

csfont = {'fontname':'Times New Roman', 'color':'white'}

class Multiquadric(Globalpolynomial):
    def __init__(self, root, icpx, icpy, digitizedi, utmi, df_gcp,  tuple_it):
        self.root = root
        self.main_window = Frame(self.root, bg='#2874a1', width=920, height=700, relief=SUNKEN)
        self.main_window.grid(row=0, column=0, sticky=S)
        self.x_digitized_ = digitizedi['x']
        self.y_digitized_ = digitizedi['y']
        print(df_gcp)
        self.x_digitized = df_gcp['x']
        self.y_digitized = df_gcp['y']
        dx, dy = self.residual_gcp(*tuple_it)
        matrix = self.distance_matrix('a')
        coef_x, coef_y = self.calc_coef(matrix)
        self.res_icp(coef_x, coef_y, icpx, icpy,  nicp=3)
        a, b = self.adjust(icpx, icpy)
        cal = np.vstack([a,b]).T
        *_,fig = self.rmse(cal, np.array(utmi), text=True, only_rmse=False)
        result_mq = Toplevel(self.main_window)
        result_mq.title("Residual vector map")
        result_mq.geometry("1000x800")
        canvas_object = Canvas_it(result_mq, fig)
        canvas_object.locate(0, 0)




    def residual_gcp(self, funcx, funcy, x_digitized, y_digitized, x_utm, y_utm):
        self.x_digitized, self.y_digitized = x_digitized, y_digitized
        self.xutm, self.yutm = x_utm, y_utm
        self.gcpx_calc = funcx(x_digitized, y_digitized)
        self.gcpy_calc = funcy(x_digitized, y_digitized)
        dx_gcp = self.gcpx_calc - x_utm
        dy_gcp = self.gcpy_calc - y_utm
        self.quantity = dx_gcp.shape[0]
        self.dx_gcp, self.dy_gcp = np.array(dx_gcp), np.array(dx_gcp)
        return dx_gcp, dy_gcp

    def distance_matrix(self, mode):
        if mode == 'utm':
            a = np.vstack([np.array(self.xutm), np.array(self.yutm)]).T
        else:
            a = np.vstack([np.array(self.x_digitized), np.array(self.y_digitized)]).T

        dmatrix = np.zeros((self.quantity, self.quantity))
        for i in range(self.quantity):
            dmatrix[:, i] = np.sqrt(np.sum((a[i, :] - a[:, :]) ** 2, axis=1))
        return dmatrix

    def calc_coef(self, matrix):
        coef_x = np.linalg.inv(matrix.T @ matrix) @ matrix.T @ self.dx_gcp
        coef_y = np.linalg.inv(matrix.T @ matrix) @ matrix.T @ self.dy_gcp
        return coef_x, coef_y

    def res_icp(self, coef_x, coef_y,icpx, icpy,  nicp=3):
        icp_dist = np.zeros((nicp, coef_x.shape[0]))
        icpx_ = icpx[:, np.newaxis].copy()
        icpy_ = icpy[:, np.newaxis].copy()
        for i in range(nicp):
            dx = icpx_[i, 0] - np.array(self.x_digitized_)
            dy = icpy_[i,0] - np.array(self.y_digitized_)
            a = np.sqrt(dx ** 2 + dy ** 2)
            icp_dist[:, i] = a
        self.dX = icp_dist @ coef_x
        self.dY = icp_dist @ coef_y
        return icp_dist, self.dX, self.dY

    def adjust(self, icp_x, icp_y):
        return icp_x + self.dX, icp_y + self.dY

    def rmse(self, cal, ob, text=True, only_rmse=False):
        plt.style.use('ggplot')
        difference = (cal - ob).copy()
        distance = np.sqrt(difference[:, 0] ** 2 + difference[:, 1] ** 2)
        theta = np.arctan(difference[:, 1] / difference[:, 0])
        rmse_ = np.sqrt(sum(distance ** 2 / (cal.shape[0] - 1)))
        mae = np.sqrt(sum(abs(difference[:, 0]) + abs(difference[:, 1])) / (cal.shape[0] - 1))
        k = 0

        def drawArrow(A, B):
            ax.arrow(A[0], A[1], B[0] - A[0], B[1] - A[1],
                     head_width=3, length_includes_head=False, color='#6e5615', linewidth=2)

        if only_rmse == False:
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='#5f95a1')
            for i in zip(ob, cal):
                ax.scatter(*i[0], label="observed_" + str(k))
                ax.scatter(*i[1], label="computed_" + str(k))
                drawArrow(i[0], i[1])
                k += 1
            if text:
                ax.set_title("Multi quadric adjusted coordinates", **csfont)
            ax.legend()
        ax.set_xticks([])
        columns = ["$RMSE$","$MAE$"]
        values = np.array([[np.float64(rmse_), np.float64(mae)]])
        colors=[['#5f95a1', '#5f95a1']]
        table = ax.table(cellText=values, colLabels=columns, colLoc='center',
                         cellColours=colors, loc='bottom')
        return rmse_, theta, distance, mae, fig
