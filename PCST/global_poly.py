import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sympy as sp
from sklearn.cluster import KMeans
import itertools
from IPython.display import Math, display

csfont = {'fontname':'Times New Roman', 'color':'white'}
class Regression:
    def __init__(self, dataframe):
        self.df = dataframe

    def __setitem__(self, txt):
        self.text = txt

    def scatterplot(self, ax,mode):
        self.count = self.df.shape[0]
        colors = mpl.cm.rainbow(np.linspace(0, 1, self.count))
        ax.scatter(np.array(self.df.iloc[:, 0]), np.array(self.df.iloc[:, 1]), color=colors)
        if mode=='gcp':
            for i in range(self.count):
                ax.annotate(str(i), (self.df.iloc[i, :][0], self.df.iloc[i, :][1]), fontsize=12, family='serif')
        else:
            for i in range(self.count):
                ax.annotate("icp " + str(i), (self.df.iloc[i, :][0], self.df.iloc[i, :][1]), fontsize=12, family='serif')
            self._grid(ax)

    def _grid(self, ax):
        ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        ax.xaxis.set_minor_locator(mpl.ticker.MaxNLocator(10))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        ax.yaxis.set_minor_locator(mpl.ticker.MaxNLocator(10))
        ax.grid(color="#911440", which='major', axis='x')
        ax.grid(color="grey", which='minor', axis='x', linestyle="--")
        ax.grid(color="#911440", which='major', axis='y')
        ax.grid(color="grey", which='minor', axis='y', linestyle="--")
        ax.set_title(self.text, **csfont)

    def cluster(self, ax, df, count=3):
        kmeans = KMeans(count)
        label = kmeans.fit_predict(df)
        u_labels = np.unique(label)
        temp = np.array(df)
        for i in u_labels:
            ax.scatter(temp[label == i, 0], temp[label == i, 1], label=i)
        for i in range(df.shape[0]):
            ax.annotate(str(i), (df.iloc[i, :][0], df.iloc[i, :][1]), fontsize=12, family='serif')
        self._grid(ax)
        ax.legend()

    def create_A(self, term, im):
        pows = np.array(list(itertools.product(range(0, term + 1), repeat=2)))
        pows = pows[np.sum(pows, axis=1) <= term]
        self.power = pows
        powsravel = pows.copy().ravel()
        dictkey = []
        for i in range(0, 2 * len(pows), 2):
            dictkey.append(f"x^{str(powsravel[i])}y^{str(powsravel[i + 1])}")
        b = im[0]
        pow_row = b[0] ** pows[:, 0] * b[1] ** pows[:, 1]
        for j in range(1, self.count):
            b = im[j]
            row = b[0] ** pows[:, 0] * b[1] ** pows[:, 1]
            pow_row = np.vstack([pow_row, row])
        self.key = dictkey
        return pow_row, pd.DataFrame(pow_row, columns=dictkey)

    def least_square(self, gcp, x, y, freedom=np.inf):

        if freedom != 0:
            X = np.linalg.inv(gcp.T @ gcp) @ gcp.T @ x
            Y = np.linalg.inv(gcp.T @ gcp) @ gcp.T @ y
            Xdf = pd.DataFrame(X, index=self.key, columns=['X'])
            Ydf = pd.DataFrame(Y, index=self.key, columns=['Y'])
            answer = pd.concat([Xdf, Ydf], axis=1)
            return X, Y, answer
        else:
            X = np.linalg.inv(gcp) @ x
            Y = np.linalg.inv(gcp) @ y
            Xdf = pd.DataFrame(X, index=self.key, columns=['X'])
            Ydf = pd.DataFrame(Y, index=self.key, columns=['Y'])
            answer = pd.concat([Xdf, Ydf], axis=1)
            return X, Y, answer

    def expression(self, x_coeff, y_coeff):
        x_, y_, = sp.symbols("x y")
        exprx = 0
        expry = 0
        for i, cx, cy in zip(self.power, range(len(x_coeff)), range(len(y_coeff))):
            exprx += float(x_coeff[cx]) * x_ ** i[0] * y_ ** i[1]
            expry += float(y_coeff[cy]) * x_ ** i[0] * y_ ** i[1]
        return exprx, expry

    def numpyit(self, X_, Y_):
        x_, y_ = sp.symbols("x y")
        functionx = sp.lambdify((x_, y_), X_, "numpy")
        functiony = sp.lambdify((x_, y_), Y_, "numpy")
        return functionx, functiony

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
                ax.set_title(self.text, **csfont)
            ax.legend()
        ax.set_xticks([])
        columns = ["$RMSE$","$MAE$"]
        values = np.array([[np.float64(rmse_), np.float64(mae)]])
        colors=[['#5f95a1', '#5f95a1']]
        table = ax.table(cellText=values, colLabels=columns, colLoc='center',
                         cellColours=colors, loc='bottom')
        return rmse_, theta, distance, mae, fig