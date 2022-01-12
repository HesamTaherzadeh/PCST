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
from tkinter.ttk import Treeview, Combobox, Style
csfont = {'fontname':'Times New Roman', 'color':'white'}


class Pointwise():
    def __init__(self, gcp, icp, root, tuple_it, xg, yg):
        self.tuple_it = tuple_it
        self.root = root
        self.main_window = Frame(self.root, bg='#2874a1', width=920, height=700, relief=SUNKEN)
        self.main_window.grid(row=0, column=0, sticky=S)
        self.x_digitized_ = gcp.T.iloc[0][:, np.newaxis]
        self.y_digitized_ = gcp.T.iloc[1][:, np.newaxis]
        self.x_utm_ = gcp.T.iloc[2][:, np.newaxis]
        self.y_utm_ = gcp.T.iloc[3][:, np.newaxis]
        self.checks_img_x = icp.T.iloc[0][:, np.newaxis].T
        self.checks_img_y = icp.T.iloc[1][:, np.newaxis].T
        self.checks_utm_x = icp.T.iloc[2][:, np.newaxis].T
        self.checks_utm_y = icp.T.iloc[3][:, np.newaxis].T
        self.dx, self.dy = self.residual_gcp(*tuple_it)
        self.xg, self.yg = xg, yg
        self.bcommand()
        comp = Button(self.main_window, text="compute", width=10, height=5, bg="powder blue", command=self.compute)
        comp.place(x=0, y=0)

    def compute(self):
        method = str(self.method.get())
        mode = str(self.mode.get())
        self.ord = Combobox(self.main_window, width=27)
        self.ord['values'] = list(map(str, range(20)))
        self.ord.place(x=(920 / 2) - 100, y=250)
        num = int(self.pnum.get())
        obj1 = self.adjust_pw(num, method, mode, self.dx, self.dy, 2)
        calc = obj1[0].reshape(self.checks_utm_y.shape[1], 2) + np.vstack([self.xg, self.yg]).T
        *_, fig = self.rmse(calc, np.vstack([self.checks_utm_x, self.checks_utm_y]).T)
        result_pw = Toplevel(self.main_window)
        result_pw.title("Residual vector map(Pointwise)")
        result_pw.geometry("1000x800")
        canvas_pw = Canvas_it(result_pw, fig)
        canvas_pw.locate(0, 0)

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
                ax.set_title("Pointwise adjusted coordinates", **csfont)
            ax.legend()
        ax.set_xticks([])
        columns = ["$RMSE$","$MAE$"]
        values = np.array([[np.float64(rmse_), np.float64(mae)]])
        colors=[['#5f95a1', '#5f95a1']]
        table = ax.table(cellText=values, colLabels=columns, colLoc='center',
                         cellColours=colors, loc='bottom')
        return rmse_, theta, distance, mae, fig
    def bcommand(self):
        l0 = Label(self.main_window, text="Select the method to choose the points:")
        l0.place(x=(920 / 2) - 95, y=70)
        l0.configure(font=("Times New Roman", 12), bg='#2874a1', fg="#000b6e")
        n = StringVar()

        self.method = Combobox(self.main_window, width=27, textvariable=n)
        self.method['values'] = ['Quadrants', 'nearest']
        self.method.place(x=(920 / 2) - 100, y=100)

        l1 = Label(self.main_window, text="Select the mode to choose the points:")
        l1.place(x=(920 / 2) - 95, y=140)
        l1.configure(font=("Times New Roman", 12), bg='#2874a1', fg="#000b6e")

        n2 = StringVar()
        self.mode = Combobox(self.main_window, width=27, textvariable=n2)
        self.mode['values'] = ['Moving average', 'Weighted distance']
        self.mode.place(x=(920 / 2) - 100, y=170)

        n4 = StringVar()
        l4 = Label(self.main_window, text="Choose number of effective points:")
        l4.place(x=(920 / 2) - 95, y=210)
        l4.configure(font=("Times New Roman", 12), bg='#2874a1', fg="#000b6e")
        self.pnum = Combobox(self.main_window, width=27, textvariable=n4)
        self.pnum['values'] = list(map(str, range(3, self.x_digitized_.shape[0])))
        self.pnum.place(x=(920 / 2) - 100, y=240)

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


    def _distance(self):
        """
        private method to find distance
        """
        yd = np.power(self.checks_utm_y - self.y_utm_, 2)
        xd = np.power(self.checks_utm_x - self.x_utm_, 2)
        xdyd = np.sqrt(np.abs(yd + xd))
        return xdyd

    def choose_point(self, n, mode, dx, dy):
        """
        choosing the points ==> 2 modes
        mode 1 : "closest":
        will find the closest points to the effected points without considering further constraints
        mode 2:
        executing another private method _list_nquads
        returning the indices and the adjustments and the distances
        """
        if mode == 'nearest':
            dist = self._distance()
            points = np.sort(dist, axis=1)[:n, :].copy().T
            near = {}
            for i in range(self.checks_utm_y.shape[1]):
                k = []
                for j in range(n):
                    k.append(np.array(np.where(np.round(points[i, j] - dist) == 0)[1]))
                near[i] = np.array(k), np.array(dx)[[k]].reshape(n, 1), np.array(dy)[[k]].reshape(n, 1)
            return near, points
        elif mode == 'Quadrants':
            near, points = self._list_nquad(n, dx, dy)
            return near, points

    def _list_nquad(self, n, dx, dy):
        """
        its a private method calculate and actually choose the points in the quadrant mode
        also will return the distance's, index of the chosen points in a dictionary
        """
        dic = self.find_quad()
        total = {}
        dist_of_p = []
        for picp in range(3):
            lis_sort = []
            dis_sort = []
            no_inquad = []
            for i in range(4):
                tem = dic[picp][i][0]
                no_inquad.append(dic[picp][i][1])
                tem = tem[:, tem[1, :].argsort()]
                lis_sort.append(tem[0])
                dis_sort.append(tem[1])
            mio = max(no_inquad)
            for i in range(4):
                lis_sort[i] = np.hstack([lis_sort[i], np.inf * np.ones((mio - len(lis_sort[i])))])
                dis_sort[i] = np.hstack([dis_sort[i], np.inf * np.ones((mio - len(dis_sort[i])))])
            kh = []
            dd = []
            lis_sort = np.array(lis_sort)
            dis_sort = np.array(dis_sort)
            for j in range(lis_sort.shape[1]):
                for i in range(lis_sort.shape[0]):
                    if lis_sort[i, j] != np.inf:
                        kh.append(lis_sort[i, j])
                        dd.append(dis_sort[i][j])
            total[picp] = [np.array(kh[:n])[:, np.newaxis], dx[np.array(kh[:n], np.int8)],
                           dy[np.array(kh[:n], np.int8)]]
            dist_of_p.append(dd[:n])
        return total, np.vstack(dist_of_p)

    def find_quad(self):
        """
        it will decide the quadrant of each point and will compute its distance and returning results as a dictionary
        """
        utms = np.vstack([self.x_utm_.copy(), self.y_utm_.copy()]).T.reshape(-1, 2)
        utm_checks = np.hstack([self.checks_utm_x.copy(), self.checks_utm_y.copy()]).T
        quads = [[True, True],
                 [True, False],
                 [False, True],
                 [False, False]]
        ps = []
        dists = self._distance().copy()
        for i in range(3):
            x = utms > utm_checks[i]
            f = lambda x: quads.index(x)
            ps.append(list(map(f, list(map(list, x)))))
        temp = []
        ps = np.array(ps)
        dists = dists.T
        dic_of_points = {}
        for p in range(3):
            mn = np.vstack([np.arange(10), np.array(list(zip(dists[p], ps[p]))).T])
            ll = []
            for k in range(4):
                ll.append([mn[:, mn[2] == k], (mn[:, mn[2] == k]).shape[1]])
            dic_of_points[p] = ll
        return dic_of_points

    def adjust_pw(self, n, mode, method, dx, dy, k):
        """
        the actuall executing function which will adjust the dx and dy's
        to be added to the Global polynomial results
        having 2 methods for adjusting:
        1: "weighted distance"
        will return the adjusted dx and dy
        and the adjust values
        2 : "moving average"
        will return the adjusted dx and dy
        and the adjust values
        and the coeffients of the adjustment equation
        """
        dic, dist = self.choose_point(n, mode, dx, dy)
        if method == 'Weighted distance':
            adjs = {}
            for i in range(self.checks_utm_y.shape[1]):
                dx, dy = np.ravel(dic[i][1]), np.ravel(dic[i][2])
                w = 1 / np.power(dist[i, :], k)
                adjs[i] = [np.sum(w * dx) / np.sum(w), np.sum(w * dy) / np.sum(w)]
            return np.array(list(adjs.values())), adjs

        elif method == 'Moving average':
            coeffs = {}
            res = []
            res_dic = {}
            for i in range(self.checks_utm_y.shape[0]):
                indices = dic[i][0]
                dx, dy = np.ravel(dic[i][1]), np.ravel(dic[i][2])
                xs = self.x_utm_[np.array([indices], np.int8)].copy()
                ys = self.y_utm_[[np.array([indices], np.int8)]].copy()
                Ax = np.hstack([np.ones_like(xs), xs, ys]).reshape(n, self.checks_utm_y.shape[1])
                Ay = np.hstack([np.ones_like(ys), xs, ys]).reshape(n, self.checks_utm_y.shape[1])
                cx = np.linalg.inv(Ax.T @ Ax) @ Ax.T @ dx
                cy = np.linalg.inv(Ay.T @ Ay) @ Ay.T @ dy
                coeffs[i] = [np.hstack([cx, cy])]
                Acheckx = np.vstack([np.ones_like(self.checks_utm_x), self.checks_utm_x, self.checks_utm_y]).T
                Achecky = np.vstack([np.ones_like(self.checks_utm_x), self.checks_utm_x, self.checks_utm_y]).T
                resx = Acheckx @ cx
                resy = Achecky @ cy
                temp = np.vstack([resx, resy])
                res.append(temp.T)
                res_dic[i] = temp
            return np.array(res), coeffs, res_dic