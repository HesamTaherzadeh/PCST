"""
A multi-purpose application designed in python Tkinter
To model different photogrametry models """
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
from Multiquad import Multiquadric
from Conformal import Conformal
from Pointwise import Pointwise
from Affine import Affine
from tkinter.ttk import Treeview, Combobox, Style
import webbrowser



def extractdf(root, mode):
    global df_gcp, df_icp, digitizedg, utmg, digitizedi, utmi
    if mode=='gcp':
        tempobj = Open(root)
        df_gcp = tempobj.extract()
        digitizedg, utmg = df_gcp.iloc[:, :2], df_gcp.iloc[:, 2:]
    elif mode == 'icp':
        tempobj = Open(root)
        df_icp = tempobj.extract()
        digitizedi, utmi = df_icp.iloc[:, :2], df_icp.iloc[:, 2:]

def show_map():
    global fig,obj2
    fig,ax = plt.subplots(2, 1, figsize=(8, 7.5), facecolor='#2874a1')
    obj1 = Regression(digitizedg)
    obj2 = Regression(utmg)
    obj3 = Regression(digitizedi)
    obj4 = Regression(utmi)
    obj1.text="Image space"
    obj2.text = "Ground space"
    obj3.text = "Image space"
    obj4.text = "Ground space"
    obj1.scatterplot(ax[0], mode="gcp")
    obj2.scatterplot(ax[1], mode="gcp")
    obj3.scatterplot(ax[0], mode="icp")
    obj4.scatterplot(ax[1], mode="icp")
    global canvas_map
    canvas_map = Canvas_it(main_window, fig)
    canvas_map.locate(0, -20)

def destroy():
    main_window.destroy()

def ghandle():
    global objgp
    destroy()
    objgp = Globalpolynomial(df_gcp, df_icp, root, obj2, digitizedi, utmi)

def mqhandle():
    destroy()
    *newout, xicp, yicp = objgp.pass_out()
    Multiquadric(root, xicp, yicp, digitizedi, utmi, df_gcp, newout)

def confor_handle():
    destroy()
    obj = Conformal(df_gcp, df_icp, root)
    conlabel = Label(obj.main_window, text="Enter the spreadsheet of \n"
                                       "New image coordinates ")
    conlabel.place(x=(920/2) - 100, y=258)
    conlabel.configure(font=("Times New Roman", 12), bg='#2874a1', fg="#000b6e")
    btn = Button(obj.main_window, bg='#2874a1', image=img)
    btn.place(x=(920 / 2) - 50, y=310)


def pointhandle():
    destroy()
    *newout, xicp, yicp = objgp.pass_out()
    Pointwise(df_gcp, df_icp, root, newout, xicp, yicp)

def affine_handle():
    destroy()
    Affine(df_gcp, df_icp, root)

def openweb():
    webbrowser.open('https://github.com/HesamTaherzadeh/PCST', new=1)

def stepbfrcluster():
    global clu, gcp, figof,numberofclassint
    def get():
        var.set(int(numberofclass.get()))

    combostyle = Style()

    combostyle.theme_create('combostyle', parent='alt',
                            settings={'TCombobox':
                                          {'configure':
                                               {'selectbackground': '#42c5f5',
                                                'fieldbackground': '#07b5f5',
                                                'background': '#0a485e'
                                                }}}
                            )
    combostyle.theme_use('combostyle')
    result_cl = Toplevel(root)
    result_cl.title("Residual vector map")
    result_cl.geometry("1000x800")
    framecluster = Frame(result_cl, bg='#2874a1', width=1000, height=800, relief=SUNKEN)
    framecluster.grid(row=0, column=0, sticky=S)
    clu = Open(framecluster)
    gcp = clu.extract()
    figof, ax = plt.subplots(figsize=(10, 8), facecolor='#5f95a1')
    newobj = Regression(gcp)
    newobj.text = 'Clustered data through K-Means method'
    l1 = Label(framecluster, text="Number of clusters:")
    l1.place(x=(920 / 2) - 90, y=100)
    l1.configure(font=("Times New Roman", 12), bg='#2874a1', fg="#0e2245")
    numberofclass = Combobox(framecluster, width=27)
    numberofclass['values'] = list(map(str, range(gcp.shape[0])))
    numberofclass.place(x=(920 / 2) - 100, y=130)
    var = IntVar()
    buttonincluster = Button(framecluster, text="Cluster", width=10, height=5, bg="powder blue",command=get)
    buttonincluster.place(x=0, y=0)
    buttonincluster.wait_variable(var)
    newobj.cluster(ax, gcp, int(var.get()))
    canvas_cl = Canvas_it(framecluster, figof)
    canvas_cl.locate(0, 0)

root = Tk()
root.geometry("1000x680")
root.title("Photogrammetric coordinate system transformer")
root.iconbitmap('main.ico') # Frame logo


bar = Frame(root, bg='#496d82', width=80, height=700, relief=SUNKEN)
bar.grid(row=0, column = 1, sticky = W)

main_window = Frame(root, bg='#2874a1', width=920, height=700, relief=SUNKEN)
main_window.grid(row=0, column = 0, sticky=S)


m = Menu(root)
root.config(menu=m)
file_menu = Menu(m, tearoff=False)
m.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Open Spreadsheet of Ground control points", command=lambda :extractdf(root, 'gcp'))
file_menu.add_command(label="Open Spreadsheet of Independent check points", command=lambda :extractdf(root, 'icp'))
file_menu_help = Menu(m, tearoff=False)
m.add_cascade(label="Help", menu=file_menu_help)
file_menu_help.add_command(label="About", command=lambda :extractdf(root, 'gcp'))
file_menu_help.add_command(label="Documentation", command=openweb)


barb1 = Button(bar, text="show", width=10, height=5, bg="powder blue", command=show_map)
barb1.place(x=0, y=0)

barb0 = Button(bar,text="Conformal \n"
                        "Transformation", width=10,height=5, bg="powder blue", command=confor_handle)
barb0.place(x=0, y=1*85)

barbz1 = Button(bar,text="Affine \n"
                        "Transformation", width=10,height=5, bg="powder blue", command=affine_handle)
barbz1.place(x=0, y=2*85)

barb2 = Button(bar,text="Global \n"
                        "Polynomial", width=10,height=5, bg="powder blue", command=ghandle)
barb2.place(x=0, y=3*85)

barb3 = Button(bar,text="Multi \n"
                        "Quadric", width=10,height=5, bg="powder blue", command=mqhandle)
barb3.place(x=0, y=4*85)

barb4 = Button(bar,text="Point \n"
                        "Wise", width=10,height=5, bg="powder blue", command=pointhandle)
barb4.place(x=0, y=5*85)

barb5 = Button(bar,text="DLT", width=10,height=5, bg="powder blue")
barb5.place(x=0, y=6*85)

barb7 = Button(bar,text="Cluster", width=10,height=5, bg="powder blue", command=stepbfrcluster)
barb7.place(x=0, y=7*85)


img = PhotoImage(file = "icon1.png").subsample(10,10)
btn2 = Button(main_window, bg='#2874a1', image=img,
              relief=RAISED, command =lambda :extractdf(root, 'gcp'))
btn2.place(x=(920/2) - 40, y=180)

l1 = Label(main_window, text="Open Ground \n"
                             " control points spreadsheet")
l1.place(x=(920/2) - 100, y= 120)
l1.configure(font=("Times New Roman", 12),bg='#2874a1', fg="#000b6e")

btn3 = Button(main_window, bg='#2874a1', image=img,
              command =lambda :extractdf(root, 'icp'))
btn3.place(x=(920/2) - 40, y=310)

l2 = Label(main_window, text="Open Independent \n"
                             "check points spreadsheet")
l2.configure(font=("Times New Roman", 12), bg='#2874a1',fg="#000b6e")

l2.place(x=(920/2) - 100, y=258)

root.resizable(False, False)
root.mainloop()