import random
import tkinter as tk
from tkinter import filedialog

# 日時処理
import datetime as dt

# ---------要インストール---------
# グラフ
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import seaborn as sns
# 表形式データ処理
import pandas as pd
# 数学処理
import numpy as np
# エンコード判定
from chardet.universaldetector import UniversalDetector
import chardet
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
        self.yearlySumDf = pd.DataFrame()

        # plot設定
        self.itemNum = 0
        self.cmap = plt.get_cmap("tab10")
        sns.set()

        #-----------------------------------------------

        # matplotlib配置用フレーム
        frame = tk.Frame(self.master)
        
        # matplotlibの描画領域の作成
        self.fig = Figure()
        # 座標軸の作成
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.grid()  # グリッドを表示
        # matplotlibの描画領域とウィジェット(Frame)の関連付け
        self.figCanvas = FigureCanvasTkAgg(self.fig, frame)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.figCanvas, frame)
        # matplotlibのグラフをフレームに配置
        self.figCanvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # フレームをウィンドウに配置
        frame.pack(fill=tk.BOTH, expand=True)

        # 各UIを格納するFrame
        row1Frame = tk.Frame(self.master)
        row2Frame = tk.Frame(self.master)

        # ボタンの作成
        sinPlotButton = tk.Button(self.master, text='sin Draw Graph', command=self.sin_plot)
        cosPlotButton = tk.Button(self.master, text='cos Draw Graph', command=self.cos_plot)
        plotClearButton = tk.Button(row2Frame, text='clear', command=self.plot_clear)
        dailyPlotButton = tk.Button(row2Frame, text='日次　折れ線', command=self.daily_line_plot)
        weeklyPlotButton = tk.Button(row2Frame, text='週次　折れ線', command=self.weekly_line_plot)
        # weeklyBarPlotButton = tk.Button(row2Frame, text='週次　棒', command=self.weekly_bar_plot)
        monthlyBarPlotButton = tk.Button(row2Frame, text='月次　折れ線', command=self.monthly_line_plot)
        yearlyBarPlotButton = tk.Button(row2Frame, text='年次　折れ線', command=self.yearly_line_plot)
        dailyBoxPlotButton = tk.Button(row2Frame, text='年毎　日次　箱ひげ', command=self.daily_box_by_year_plot)
        weeklyBoxPlotButton = tk.Button(row2Frame, text='年毎　週次　箱ひげ', command=self.weekly_box_by_year_plot)
        monthlyBoxPlotButton = tk.Button(row2Frame, text='年毎　月次　箱ひげ', command=self.monthly_box_by_year_plot)
        # yearlyBoxPlotButton = tk.Button(row2Frame, text='年次　箱ひげ', command=self.yearly_box_plot)

        # ファイル読み込み関係のUI
        inFilePathEditBox = tk.Entry(row1Frame, width=80)
        inFileButton = tk.Button(row1Frame, text='ファイル選択', command=lambda:self.open_file_command(inFilePathEditBox, [('CSVファイル', '*.csv'), ('TEXTファイル', '*.txt')]))

        # 配置
        inFileButton.pack(side=tk.LEFT)
        inFilePathEditBox.pack(side=tk.LEFT)

        row1Frame.pack(side=tk.TOP)
        row2Frame.pack(side=tk.TOP)

        # sinPlotButton.pack(side=tk.BOTTOM)    # 描画処理のサンプル
        # cosPlotButton.pack(side=tk.BOTTOM)    # 描画処理のサンプル
        # yearlyBoxPlotButton.pack(side=tk.LEFT)
        monthlyBoxPlotButton.pack(side=tk.LEFT)
        weeklyBoxPlotButton.pack(side=tk.LEFT)
        dailyBoxPlotButton.pack(side=tk.LEFT)

        yearlyBarPlotButton.pack(side=tk.LEFT)
        monthlyBarPlotButton.pack(side=tk.LEFT)
        # weeklyBarPlotButton.pack(side=tk.LEFT)
        weeklyPlotButton.pack(side=tk.LEFT)
        dailyPlotButton.pack(side=tk.LEFT)
        plotClearButton.pack(side=tk.LEFT)

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
                # 先頭1kB読み込んで、エンコード判定
                encRet = self.getencoding(f.read(1024))
        except FileNotFoundError as err:  # Errorが発生した場合、以下の処理を実行
            tk.messagebox.showerror('ファイルオープンエラー','ファイルが開けません。\n{0}'.format(err))
            return
        except Exception as err:  # Errorが発生した場合、以下の処理を実行
            tk.messagebox.showerror('エラー','エラーが発生しました。\n{0}'.format(err))
            return

        enc = 'utf-8'
        if encRet == 'SHIFT_JIS':
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
            self.dailySumDf = self.setDateLabeling(self.dailySumDf)

            # 集計（週次）（日曜日に記載されている金額は先週月曜～当週日曜の実績の合計）
            self.weeklySumDf = self.dailySumDf.resample('W').sum()
            self.weeklySumDf = self.setDateLabeling(self.weeklySumDf)

            # 集計（月次）
            self.monthlySumDf = self.dailySumDf.resample('M').sum()
            self.monthlySumDf = self.setDateLabeling(self.monthlySumDf)

            # 集計（年次）
            self.yearlySumDf = self.dailySumDf.resample('Y').sum()
            self.yearlySumDf = self.setDateLabeling(self.yearlySumDf)

            # 凡例ラベル用データ作成
            # self.uidNameDf = pd.crosstab(index=self.df['date'], columns=[self.df['uid'],self.df['name']])
            # self.uidNameDf = pd.DataFrame(self.uidNameDf.columns.levels[1], index=self.uidNameDf.columns.levels[0])

            tk.messagebox.showinfo('データ読み込み完了','データ読み込みが完了しました。\nグラフ描画の準備ができました。')
        except Exception as err:  # Errorが発生した場合、以下の処理を実行
            tk.messagebox.showerror('エラー','エラーが発生しました。\n{0}'.format(err))
            return

    # 日付関係のラベリング
    def setDateLabeling(self, indf):
        indf = indf.reset_index()
        # 日付型から年部分だけラベリング
        indf = indf.assign(year=indf['date'].dt.strftime('%Y').astype('int'))
        # 日付型から曜日をラベリング
        indf = indf.assign(weekdayName=indf['date'].dt.strftime('%A'))
        indf = indf.assign(weekdayNum=indf['date'].apply(lambda x:x.weekday()))
        # 同じ年で日付を先頭からカウント（各年を連番で比較表示するため）
        indf = indf.assign(days=indf.groupby('year').cumcount())
        # 同じ年で1月の初回月曜からカウント（各年を連番で比較表示するため）
        dfBaseday = indf.query('days == 0')[['date','year','weekdayName','weekdayNum','days']]
        for i in range(dfBaseday['year'].min(), dfBaseday['year'].max()+1):
            strI = str(i)
            indf.loc[indf[indf['year'] == i].index, 'bdays'] = indf['days'] - dfBaseday.query('year == @i')['weekdayNum'].iloc[0]
        return indf.set_index('date')

    # 日付関係のラベリングを削除
    def removeDateLabeling(self, indf):
        return indf.drop(['year', 'weekdayName', 'weekdayNum', 'days', 'bdays'], axis='columns')

    # 任意の日付がその年で第何週目かを取得
    def getyearNthWeek(inDate):
        return inDate.isocalendar()[1]

    def getencoding(self, dat:bytes):
        return chardet.detect(dat)["encoding"]

    # 任意の日付がカレンダー上の第何週目かを取得
    def getNthWeek2Datetime(inDate, firstweekday=0):
        first_dow = dt.date(inDate.year, inDate.month, 1).weekday()
        offset = (first_dow - firstweekday) % 7
        return (inDate.day + offset - 1) // 7 + 1

    # グラフ初期化
    def plot_clear(self):
        self.fig.clf()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.grid()  # グリッドを表示
        self.figCanvas.draw()
        self.itemNum = 0

    # 日毎の折れ線グラフ
    def daily_line_plot(self):
        tmp = self.removeDateLabeling(self.dailySumDf)
        for col in list(tmp.columns):
            x = tmp.index
            y = tmp[col]

            # グラフの描画
            self.ax.plot(x, y, label=col, color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.updateItemNum()

    # 週毎の折れ線グラフ
    def weekly_line_plot(self):
        tmp = self.removeDateLabeling(self.weeklySumDf)
        for col in list(tmp.columns):
            x = tmp.index
            y = tmp[col]

            # グラフの描画
            rects = self.ax.plot(x, y, label=col, color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.updateItemNum()

    # 週毎の棒グラフ
    def weekly_bar_plot(self):
        tmp = self.removeDateLabeling(self.weeklySumDf)
        barWidth = 1
        length = len(list(tmp.columns)) * barWidth * (-1)
        for col in list(tmp.columns):
            x = tmp.index + dt.timedelta(days=length)
            y = tmp[col]

            # グラフの描画
            rects = self.ax.bar(x, y, width=barWidth, label=col, color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            length = length+barWidth

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.updateItemNum()

    # 月毎の折れ線
    def monthly_line_plot(self):
        tmp = self.removeDateLabeling(self.monthlySumDf)
        for col in list(tmp.columns):
            x = tmp.index
            y = tmp[col]

            # グラフの描画
            rects = self.ax.plot(x, y, label=col, color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.updateItemNum()

    # 年毎の折れ線
    def yearly_line_plot(self):
        tmp = self.removeDateLabeling(self.yearlySumDf)
        for col in list(tmp.columns):
            x = tmp.index
            y = tmp[col]

            # グラフの描画
            rects = self.ax.plot(x, y, label=col, color=self.cmap(self.itemNum))
            self.ax.legend(prop={"family":"MS Gothic"})

            # 表示
            self.figCanvas.draw()

            # カウンター更新
            self.itemNum = self.updateItemNum()

    # 年毎の日次箱ひげ
    def daily_box_by_year_plot(self):
        tmp = self.removeDateLabeling(self.dailySumDf)
        tmpDf = pd.DataFrame()
        for col in list(tmp.columns):
            addDf = pd.DataFrame({
                'value' : tmp[col],
                'year' : self.dailySumDf['year'],
                'label' : col
                })
            tmpDf = pd.concat([tmpDf, addDf])
        tmp = tmpDf
        sns.boxplot(tmp, ax=self.ax, x='year', y='value', hue='label')
        self.figCanvas.draw()

        # カウンター更新
        self.itemNum = self.updateItemNum()

    # 年毎の週次箱ひげ
    def weekly_box_by_year_plot(self):
        tmp = self.removeDateLabeling(self.weeklySumDf)
        tmpDf = pd.DataFrame()
        for col in list(tmp.columns):
            addDf = pd.DataFrame({
                'value' : tmp[col],
                'year' : self.weeklySumDf['year'],
                'label' : col
                })
            tmpDf = pd.concat([tmpDf, addDf])
        tmp = tmpDf
        sns.boxplot(tmp, ax=self.ax, x='year', y='value', hue='label')
        self.figCanvas.draw()

        # カウンター更新
        self.itemNum = self.updateItemNum()

    # 年毎の月次箱ひげ
    def monthly_box_by_year_plot(self):
        tmp = self.removeDateLabeling(self.monthlySumDf)
        tmpDf = pd.DataFrame()
        for col in list(tmp.columns):
            addDf = pd.DataFrame({
                'value' : tmp[col],
                'year' : self.monthlySumDf['year'],
                'label' : col
                })
            tmpDf = pd.concat([tmpDf, addDf])
        tmp = tmpDf
        sns.boxplot(tmp, ax=self.ax, x='year', y='value', hue='label')
        self.figCanvas.draw()

        # カウンター更新
        self.itemNum = self.updateItemNum()

    # 年毎の年次箱ひげ
    def yearly_box_plot(self):
        tmp = self.removeDateLabeling(self.yearlySumDf)
        tmpDf = pd.DataFrame()
        for col in list(tmp.columns):
            addDf = pd.DataFrame({
                'value' : tmp[col],
                'year' : self.yearlySumDf['year'],
                'label' : col
                })
            tmpDf = pd.concat([tmpDf, addDf])
        tmp = tmpDf
        sns.boxplot(tmp, ax=self.ax, x='year', y='value', hue='label')
        self.figCanvas.draw()

        # カウンター更新
        self.itemNum = self.updateItemNum()

    # カラーマップ用のカウンター更新
    def updateItemNum(self):
        if self.itemNum < self.cmap.N-1:
            return self.itemNum+1
        else:
            return 0

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