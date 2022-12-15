import random
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('plot graph')

        #-----------------------------------------------

        # matplotlib配置用フレーム
        frame = tk.Frame(self.master)
        
        # matplotlibの描画領域の作成
        fig = Figure()
        # 座標軸の作成
        self.ax = fig.add_subplot(1, 1, 1)
        # matplotlibの描画領域とウィジェット(Frame)の関連付け
        self.figCanvas = FigureCanvasTkAgg(fig, frame)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.figCanvas, frame)
        # matplotlibのグラフをフレームに配置
        self.figCanvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # フレームをウィンドウに配置
        frame.pack(fill=tk.BOTH, expand=True)

        # ボタンの作成
        sinPlotButton = tk.Button(self.master, text = "sin Draw Graph", command = self.sin_plot)
        cosPlotButton = tk.Button(self.master, text = "cos Draw Graph", command = self.cos_plot)

        # 配置
        sinPlotButton.pack(side = tk.BOTTOM)
        cosPlotButton.pack(side = tk.BOTTOM)

        #-----------------------------------------------

    def sin_plot(self):
        # 表示するデータの作成
        rand = random.random()
        x = np.arange(-np.pi, np.pi, 0.1)
        y = np.sin(x) * rand

        # グラフの描画
        self.ax.plot(x, y, label='sin x {:.3f}'.format(rand))
        self.ax.legend()

        # 表示
        self.figCanvas.draw()

    def cos_plot(self):
        # 表示するデータの作成
        rand = random.random()
        x = np.arange(-np.pi, np.pi, 0.1)
        y = np.cos(x) * rand

        # グラフの描画
        self.ax.plot(x, y, label='cos x {:.3f}'.format(rand))
        self.ax.legend()

        # 表示
        self.figCanvas.draw()

root = tk.Tk()
app = Application(master=root)
app.mainloop()