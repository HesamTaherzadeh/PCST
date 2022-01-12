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


class Affine():
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
        mat, l = self.create()
        coeffs = np.linalg.inv(mat.T@mat) @ mat.T @ l
        new_coord = self.compute(coeffs)
        new = np.hstack([new_coord[::2], new_coord[1::2]])
        print(new.shape)
        *_ , fig = self.rmse(new, np.vstack([self.icpe, self.icpn]).T)
        result_confor = Toplevel(self.main_window)
        result_confor.title("Residual vector map")
        result_confor.geometry("1000x800")
        canvas_object = Canvas_it(result_confor, fig)
        canvas_object.locate(0, 0)

    def create(self, mode='gcp'):
        if mode == 'gcp':
            x, y = self.gcpx, self.gcpy
            l = np.zeros((2 * x.shape[0], 1))
            l[::2] = np.array(self.gcpe).reshape(x.shape[0], 1)
            l[1::2] = np.array(self.gcpn).reshape(x.shape[0], 1)
        else:
            x, y = self.icpx, self.icpy
            l = None
        erows = np.vstack([x, y, np.zeros_like(x), np.zeros_like(x), np.ones_like(x) , np.zeros_like(x)]).T
        orows = np.vstack([np.zeros_like(x), np.zeros_like(x), x, y, np.zeros_like(x), np.ones_like(x)]).T
        lfsidemat = np.zeros((x.shape[0]*2, 6))
        lfsidemat[::2,:] = erows
        lfsidemat[1::2,:] = orows
        return lfsidemat, l

    def compute(self, coeffs):
        maticp, _ = self.create(mode="icp")
        newcoords = maticp @ coeffs
        return newcoords

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
                ax.set_title("residual vector map", **csfont)
            ax.legend()
        ax.set_xticks([])
        columns = ["$RMSE$","$MAE$"]
        values = np.array([[np.float64(rmse_), np.float64(mae)]])
        colors=[['#5f95a1', '#5f95a1']]
        table = ax.table(cellText=values, colLabels=columns, colLoc='center',
                         cellColours=colors, loc='bottom')
        return rmse_, theta, distance, mae, fig