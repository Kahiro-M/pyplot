import random
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

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

        # データ
        self.indf = pd.DataFrame()
        self.df = pd.DataFrame()
        self.dailySumDf = pd.DataFrame()
        self.monthlySumDf = pd.DataFrame()

        # plot設定
        self.itemNum = 0
        self.cmap = plt.get_cmap("tab10")

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
        dailyPlotButton = tk.Button(self.master, text='Daily Line Draw Graph', command=self.daily_plot)
        monthlyBarPlotButton = tk.Button(self.master, text='Monthly Bar Draw Graph', command=self.monthly_bar_plot)

        # ファイル読み込み関係のUI
        inFilePathEditBox = tk.Entry(self.master, width=80)
        inFileButton = tk.Button(self.master, text='ファイル選択', command=lambda:self.open_file_command(inFilePathEditBox, [('CSVファイル', '*.csv'), ('TEXTファイル', '*.txt')]))

        # 余白
        leftMarginSpace  = tk.Canvas(width=1, height=1)

        # 配置
        inFileButton.pack(side=tk.LEFT)
        inFilePathEditBox.pack(side=tk.LEFT)
        leftMarginSpace.pack(side=tk.LEFT, expand=True)
        # sinPlotButton.pack(side=tk.BOTTOM)    # 描画処理のサンプル
        # cosPlotButton.pack(side=tk.BOTTOM)    # 描画処理のサンプル
        monthlyBarPlotButton.pack(side=tk.BOTTOM)
        dailyPlotButton.pack(side=tk.BOTTOM)

        #-----------------------------------------------

    #  [FILE]ボタン押下時に呼び出し。選択したファイルのパスをテキストボックスに設定する。
    def open_file_command(self, inFilePathEditBox, inFileTypeList):
        filePath = filedialog.askopenfilename(filetypes = inFileTypeList)
        inFilePathEditBox.delete(0, tk.END)
        inFilePathEditBox.insert(tk.END, filePath)
        self.load_data(filePath)

    # データ参照
    def load_data(self, filePath):
        # ファイルのエンコードを確認
        try:  # 以下の処理を実行
            with open(filePath, 'rb') as f:
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

        try:  # 以下の処理を実行
            # 1行目のヘッダーを無視して読み込む
            indf = pd.read_csv(filePath, encoding=enc, header=0) 
            self.df = indf.set_axis(['date','uid','name','value','note'],axis='columns')
            self.df['uid'] = self.df['uid'].astype('str')
            self.df['value'] = self.df['value'].astype('float')
            self.df['name'] = self.df['name'].astype('str')
            self.df['note'] = self.df['note'].astype('str')
            self.df['date'] = self.df['date'].apply(pd.to_datetime)

            # 集計（日次）
            self.dailySumDf = pd.crosstab(index=self.df['date'], columns=self.df['uid'],values=self.df['value'],aggfunc='sum')
            self.dailySumDf = self.dailySumDf.reset_index()

            # 集計（月次）
            self.monthlySumDf = self.dailySumDf.set_index('date').resample('M').sum()
            print(self.monthlySumDf.head())

            # 凡例ラベル用データ作成
            self.uidNameDf = pd.crosstab(index=self.df['date'], columns=[self.df['uid'],self.df['name']])
            self.uidNameDf = pd.DataFrame(self.uidNameDf.columns.levels[1], index=self.uidNameDf.columns.levels[0])

            tk.messagebox.showinfo('データ読み込み完了','データ読み込みが完了しました。\nグラフ描画の準備ができました。')
        except Exception as err:  # Errorが発生した場合、以下の処理を実行
            tk.messagebox.showerror('エラー','エラーが発生しました。\n{0}'.format(err))
            return

    # 日毎の折れ線グラフ
    def daily_plot(self):
        tmp = self.dailySumDf.set_index('date')
        for col in list(tmp.columns):
            x = self.dailySumDf['date']
            y = self.dailySumDf[col]

            # グラフの描画
            self.ax.plot(x, y, label=self.uidNameDf.loc[col][0], color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.itemNum+1

    # 月毎の棒グラフ
    def monthly_bar_plot(self):
        tmp = self.monthlySumDf
        barWidth = 5
        length = len(list(tmp.columns)) * barWidth * (-1)
        for col in list(tmp.columns):
            x = tmp.index + dt.timedelta(days=length)
            y = tmp[col]

            # グラフの描画
            rects = self.ax.bar(x, y, width=barWidth, label=self.uidNameDf.loc[col][0], color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            length = length+barWidth
            # self.autolabel(rects)

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.itemNum+1

    # 各点のラベル付与
    def autolabel(self, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            self.ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    # sinカーブを描画（動作確認用）
    def sin_plot(self):
        # 表示するデータの作成
        rand = random.random()
        x = np.arange(-np.pi, np.pi, 0.1)
        y = np.sin(x) * rand

        # グラフの描画
        self.ax.plot(x, y, label='sin x {:.3f}'.format(rand))
        self.ax.legend(prop={"family":"MS Gothic"})

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
        self.ax.legend(prop={"family":"MS Gothic"})

        # 表示
        self.figCanvas.draw()

root = tk.Tk()
app = Application(master=root)
app.mainloop()