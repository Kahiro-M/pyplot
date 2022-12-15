import random
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# 日時処理
import datetime as dt

# ---------要インストール---------
# 表形式データ処理
import pandas as pd
# 数学処理
import numpy as np
# エンコード判定
from chardet.universaldetector import UniversalDetector
# --------------------------------


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
        sinPlotButton = tk.Button(self.master, text='sin Draw Graph', command=self.sin_plot)
        cosPlotButton = tk.Button(self.master, text='cos Draw Graph', command=self.cos_plot)
        showDataButton = tk.Button(self.master, text='show data', command=lambda:self.show_data(inFilePathEditBox))

        # ファイル読み込み関係のUI
        inFilePathEditBox = tk.Entry(self.master, width=80)
        inFileButton = tk.Button(self.master, text='ファイル選択', command=lambda:self.open_file_command(inFilePathEditBox, [('CSVファイル', '*.csv'), ('TEXTファイル', '*.txt')]))

        # 余白
        leftMarginSpace  = tk.Canvas(width=1, height=1)

        # 配置
        inFileButton.pack(side=tk.LEFT)
        inFilePathEditBox.pack(side=tk.LEFT)
        leftMarginSpace.pack(side=tk.LEFT, expand=True)
        sinPlotButton.pack(side=tk.BOTTOM)
        cosPlotButton.pack(side=tk.BOTTOM)
        showDataButton.pack(side=tk.BOTTOM)

        #-----------------------------------------------

    #  [FILE]ボタン押下時に呼び出し。選択したファイルのパスをテキストボックスに設定する。
    def open_file_command(self, inFilePathEditBox, inFileTypeList):
        filePath = filedialog.askopenfilename(filetypes = inFileTypeList)
        inFilePathEditBox.delete(0, tk.END)
        inFilePathEditBox.insert(tk.END, filePath)

    # データ参照
    def show_data(self, inFilePathEditBox):
        filePath = inFilePathEditBox.get()

        # ファイルのエンコードを確認
        try:  # 以下の処理を実行
            with open(filePath, 'rb') as f:
                print('a')
                detector = UniversalDetector()
                for line in f:
                    detector.feed(line)
                    if detector.done:
                        break
                detector.close()
                result = detector.result
        except FileNotFoundError as err:  # Errorが発生した場合、以下の処理を実行
            tk.messagebox.showerror('ファイルオープンエラー','ファイルが開けません。\n{0}'.format(err))
            return
        except Exception as err:  # Errorが発生した場合、以下の処理を実行
            tk.messagebox.showerror('エラー','エラーが発生しました。\n{0}'.format(err))
            return

        enc = 'utf-8'
        if result['encoding'] == 'SHIFT_JIS':
            enc = 'CP932'

        # 1行目のヘッダーを無視して読み込む
        df = pd.read_csv(filePath, encoding=enc, header=None, index_col=0, skiprows=1) 
        print(df)

    # sinカーブを描画（動作確認用）
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

    # cosカーブを描画（動作確認用）
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