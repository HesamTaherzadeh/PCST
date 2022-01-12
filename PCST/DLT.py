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
from numpy import matlib
csfont = {'fontname':'Times New Roman', 'color':'white'}


class Dlt():
    def __init__(self, gcp, icp, root):
        self.root = root
        self.main_window = Frame(self.root, bg='#2874a1', width=920, height=700, relief=SUNKEN)
        self.main_window.grid(row=0, column=0, sticky=S)
        self.gcpx = gcp.T.iloc[0]
        self.gcpy = gcp.T.iloc[1]
        self.gcpe = gcp.T.iloc[2]
        self.gcpn = gcp.T.iloc[3]
        self.icpx = icp.T.iloc[0]
        self.icpy = icp.T.iloc[1]
        self.icpe = icp.T.iloc[2]
        self.icpn = icp.T.iloc[3]

    def create_A(self, mode):
        x, y, c = self.x, self.y, self.c
        X, Y, Z = self.X, self.Y, self.Z
        count = self.count
        zero = np.zeros_like(X)
        one = np.ones_like(X)
        temp_mat1 = np.vstack([X, Y, Z, one,
                               zero, zero,
                               zero, zero]).T
        temp_mat2 = np.vstack([zero, zero, zero, zero,
                               X, Y, Z, one]).T
        temp_mat3 = np.zeros((2 * count, 11))
        temp_mat3[::2, :8] = temp_mat1
        temp_mat3[1::2, :8] = temp_mat2
        col8e, col8o = -x * X, -y * X
        col9e, col9o = -x * Y, -y * Y
        col10e, col10o = -x * Z, -y * Z
        temp_mat3[::2, 8], temp_mat3[1::2, 8] = col8e, col8o
        temp_mat3[::2, 9], temp_mat3[1::2, 9] = col9e, col9o
        temp_mat3[::2, 10], temp_mat3[1::2, 10] = col10e, col10o
        # temp_mat3[::2, 11],temp_mat3[1::2, 11] = x, y
        return temp_mat3

    def compute(self, A):
        l = np.zeros((self.count * 2, 1))
        l[::2] = np.array(self.x).reshape(self.count, 1)
        l[1::2] = np.array(self.y).reshape(self.count, 1)
        self.xcap = np.linalg.inv(A.T @ A) @ A.T @ l
        return self.xcap

    def new_coord_image(self):
        x, y, c = self.xicp, self.yicp, self.cicp
        X, Y, Z = self.Xicp, self.Yicp, self.Zicp
        count = self.counticp
        xnew_num = self.xcap[0, 0] * X + self.xcap[1, 0] * Y + self.xcap[2, 0] * Z + self.xcap[3, 0]
        denum = self.xcap[8, 0] * X + self.xcap[9, 0] * Y + self.xcap[10, 0] * Z + 1
        ynew_num = self.xcap[4, 0] * X + self.xcap[5, 0] * Y + self.xcap[6, 0] * Z + self.xcap[7, 0]
        newcoord = np.vstack([xnew_num / denum, ynew_num / denum]).T
        return newcoord

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
                     head_width=0.002, length_includes_head=False, color='#6e5615', linewidth=0.2)

        if only_rmse == False:
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='#5f95a1')
            for i in zip(ob, cal):
                ax.scatter(*i[0], label="observed_" + str(k))
                ax.scatter(*i[1], label="computed_" + str(k))
                drawArrow(i[0], i[1])
                k += 1
            if text:
                ax.set_title("Residual vector map", **csfont)
            ax.legend(bbox_to_anchor=(1, 1.01), loc='upper left', ncol=1)
        ax.set_xticks([])
        columns = ["$RMSE$", "$MAE$"]
        values = np.array([[np.float64(rmse_), np.float64(mae)]])
        colors = [['#5f95a1', '#5f95a1']]
        table = ax.table(cellText=values, colLabels=columns, colLoc='center',
                         cellColours=colors, loc='bottom')
        return rmse_, theta, distance, mae, fig