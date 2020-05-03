#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 15:01:22 2020

@author: kei
"""
import datetime
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
from japanmap import picture


# グラフ作成クラス
class GraphCreator():
    
    # コンストラクタ
    def __init__(self):

        # 都道府県名定義ファイル
        self.convert_path = "./convert_pref_kanji2romaji.txt"
        self.code_type = "utf-8"
        
        # グラフ設定
        self.title = "Cases of Infection in "
        self.title_map = "Infection Heat Map on "
        self.xlabel = "Date"
        self.ylabel = "Cases"
        self.graph_hight = 5.2
        self.graph_hight_map = 5.2
        self.graph_width = 7.8
        self.graph_width_map = 7.8
        self.graph_dpi = 100
        self.daylocate = 10
        
        #/*自動設定の場合不要
#        self.ylim_min = 0
#        self.ylim_max = 10000
#        self.xlim_min = datetime.datetime(2020, 1, 1)
#        self.xlim_max = datetime.datetime.now()
#        self.xlim_max = datetime.datetime(2020, 4, 12)
        #*/自動設定の場合不要
        
        self.bgcolor = "navy"
        self.bgcolor_map = "white"
        self.barcolor = "lime"
        self.titlecolor = "white"
        self.axcolor = "white"
        self.labelcolor = "white"
        self.gridcolor = "gray"
        self.plotcolor = "magenta"
    
    # グラフを作成する
    def createGraph(self, dataframe, prefecture):
        
        # 入力のデータフレームがFalseだった場合、処理終了
        if dataframe is False:
            return
                
        # 空のグラフオブジェクトを作成
        fig = plt.figure(figsize=(self.graph_width, self.graph_hight),
                         facecolor=self.bgcolor, dpi=self.graph_dpi, 
                         tight_layout=False)
        
        # サブプロットを作成する
        ax = plt.subplot(facecolor=self.bgcolor)
        
        # ax1とax2を関連させる
        ax2 = ax.twinx()

        # x軸のデータのフォーマットを指定する
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        
        # x軸の範囲を設定
        # コメントアウトすると自動調節
#        ax.set_xlim(self.xlim_min, self.xlim_max)
#        ax2.set_xlim(self.xlim_min, self.xlim_max)
        
        # 目盛り幅を設定
        xloc = mpl.dates.MinuteLocator(byminute=range(0,60,1))
        ax.xaxis.set_major_locator(xloc)
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, 
                                                     interval=self.daylocate, 
                                                     tz=None))
        ax2.xaxis.set_major_locator(xloc)
        ax2.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, 
                                                     interval=self.daylocate, 
                                                     tz=None))



        # 軸ラベル削除
        ax2.tick_params(labelbottom=False, labelleft=False,
                        labelright=True, labeltop=False)
        
        # 軸メモリ削除
        ax2.tick_params(bottom=False, left=False, right=True, top=False)
        
        
        # y軸の範囲を設定
        # コメントアウトすると自動調節
#        ax.set_ylim(self.ylim_min, self.ylim_max)
        
        # ラベルの色を設定
        ax.xaxis.label.set_color(self.labelcolor)
        ax.yaxis.label.set_color(self.labelcolor)
        ax2.xaxis.label.set_color(self.labelcolor)
        ax2.yaxis.label.set_color(self.labelcolor)
        
        # 軸の色を設定
        ax.spines['top'].set_color(self.axcolor)
        ax.spines['bottom'].set_color(self.axcolor)
        ax.spines['left'].set_color(self.axcolor)
        ax.spines['right'].set_color(self.axcolor)
        ax.tick_params(axis='x', colors=self.axcolor)
        ax.tick_params(axis='y', colors=self.axcolor)
 
        ax2.spines['top'].set_color(self.axcolor)
        ax2.spines['bottom'].set_color(self.axcolor)
        ax2.spines['left'].set_color(self.axcolor)
        ax2.spines['right'].set_color(self.axcolor)
        ax2.tick_params(axis='x', colors=self.axcolor)
        ax2.tick_params(axis='y', colors=self.axcolor)
        
        # グリッドを設定
        ax.xaxis.grid(True, which='major', linestyle='-', color=self.gridcolor)
        ax.yaxis.grid(True, which='major', linestyle='-', color=self.gridcolor)
        ax.set_axisbelow(True)
        
#        ax2.xaxis.grid(False, which='major', linestyle='-', color=self.gridcolor)
#        ax2.yaxis.grid(False, which='major', linestyle='-', color=self.gridcolor)
#        ax2.set_axisbelow(False)

        # データをプロットする    
        dataframe = dataframe.sort_values('Date')
        x = list(dataframe['Date'])
        y = list(dataframe['InfNum'].astype(int))
                    
        y2 = list(dataframe["Total"])
        ax.bar(x, y, color=self.barcolor)
        ax2.plot(x, y2, color=self.plotcolor)
        
        # タイトルを設定する
        pref_romaji = self.__convertPrefKanji2Romaji(prefecture)
        title = self.title + pref_romaji
        
        plt.title(title, color=self.titlecolor)
        
        # x方向のラベルを設定する
        plt.xlabel(self.xlabel)
        
        # y方向のラベルを設定する
        plt.ylabel(self.ylabel)
        
        # 標準出力に表示
#        plt.show()
        
        return fig
    
    # 都道府県名を漢字からローマ字に変換する関数
    def __convertPrefKanji2Romaji(self, pref):
        
        # 変換定義ファイルの読み込み
        df = pd.read_csv(self.convert_path, header=None, names=["Kanji","Romaji"], 
                         comment='#', encoding=self.code_type)
                         
        # 漢字に対応するローマ字を取得
        df_pref = df.query('Kanji == @pref')
        pref_romaji = df_pref["Romaji"].astype(str).tolist()[0]
                
        # ローマ字の都道府県名を返す
        return pref_romaji
    
    def createInfMapJapan(self, df, date):
                
        if df is False:
            return
        
        # 空のグラフオブジェクトを作成
        fig = plt.figure(figsize=(self.graph_width_map, self.graph_hight_map),
                         facecolor=self.bgcolor_map, dpi=self.graph_dpi, 
                         tight_layout=True)
        
        # 都道府県名を行名に設定
        df_in = df.set_index("Pref")
        
        # カラーマップの作成
        cmap = plt.get_cmap('Blues')
        
        # 値の正規化
        norm = mpl.colors.Normalize(vmin=df_in["InfNum"].min(), vmax=df_in["InfNum"].max())
        
        # 色変換
        fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

        # カラーバーの作成
        mappable = plt.cm.ScalarMappable(norm, cmap)
        mappable.set_array(df_in["InfNum"])
        plt.colorbar(mappable)
        
        # タイトルの設定
        title = self.title_map + date
        plt.title(title)
        
        # 軸ラベル削除
        plt.tick_params(labelbottom=False, labelleft=False,
                        labelright=False, labeltop=False)
        
        # 軸メモリ削除
        plt.tick_params(bottom=False, left=False, right=False, top=False)
        
        # 描画
        plt.imshow(picture(df_in["InfNum"].apply(fcol)));     
        
        # 表示
#        plt.show()
        
        return fig
        
        
class DataOperator():
    
    # コンストラクタ
    def __init__(self):
        
        # ファイル設定
        self.read_dir_path = "./CoronavirusData/"
        self.write_path = "./data/output/a.png"
        self.column_names = ["Date","Pref", "Total", "InfNum"]
        self.code_type = "utf-8"
               
        # 存在する日付
        self.date_list = list()
        
    # 日付リストに存在する日付をセット
    def setDateList(self, path):
        
        # 日付リストを作成
        date_list = list()
        
        # 指定したディレクトリのファイルパス名一覧を取得する
        file_name_list = sorted(glob.glob(path), reverse=True)
        # print(file_name_list)

        # ファイルパスをひとつずつ読み込む
        for file_path in file_name_list:

            # 日付を取得
            filename = os.path.splitext(os.path.basename(file_path))[0]
            # print(filename)
            date = filename[:8]    

            # 日付列を追加
            date_date = datetime.datetime.strptime(date, '%Y%m%d')
            # print(date_date)
            date_str = date_date.strftime('%Y/%m/%d')
            
            date_list.append(date_str)
            
        return date_list
        
    # データを読み取る
    def getCsvDataPref(self, prefecture):
        
        # 指定したディレクトリのファイルパス名一覧を取得する
        path = self.read_dir_path + "*"
        file_name_list = glob.glob(path)
        # print(file_name_list)
        # 空のデータフレームを作成
        df_merged = pd.DataFrame(columns=self.column_names)

        # ファイルパスをひとつずつ読み込む
        for file_path in file_name_list:
            
            # ファイルを読み込む
            # ヘッダーなし、列名["Pref","InfNum"]、コメント行#を飛ばす、日本語対応
            df = pd.read_csv(file_path, header=None, names=["Pref", "Total", "InfNum"], 
                             comment='#', encoding=self.code_type)
            # print(df)
            # 日付を取得
            filename = os.path.splitext(os.path.basename(file_path))[0]
            date = filename[:8]
            
            # 日付列を追加
            df["Date"] = datetime.datetime.strptime(date, '%Y%m%d')
            df.loc[:, self.column_names]
            
            # マージする
            df_merged = pd.concat([df_merged, df], sort=False)

        # print(df_merged)
            
        # 選択した都道府県だけのデータフレームを作成  
        # もし選択した都道府県名がデータになければFalseを返す
        if not prefecture in df_merged.values:
            print("インプットエラー：選択した都道府県名のデータはありませんでした。")
            return False
        
        df_pref = df_merged.query('Pref == @prefecture')
            
        return df_pref
    
    # 8桁の日付文字列を受け取り、その日の都道府県の感染者データフレームを返す
    def getCsvDataDate(self, date):
        
        # 指定したディレクトリのファイルパス名一覧を取得する
        file_path = self.read_dir_path + date + ".txt"
        # print(file_path)
        # 該当するファイルがない場合Falseを返す
        if os.path.exists(file_path) is False:
            print("インプットエラー：選択した日付のデータはありませんでした。")
            return False
        
        # ファイルを読み込む
        # ヘッダーなし、列名["Pref","InfNum"]、コメント行#を飛ばす、日本語対応
        df = pd.read_csv(file_path, header=None, names=["Pref", "Total", "InfNum"], 
                         comment='#', encoding=self.code_type)

        return df

if __name__ == "__main__":
    
    pref = "東京都"
    date = "20200402"
    save_path = "./data/output/a.png"
    
    do = DataOperator()
    df = do.getCsvDataPref(pref)
    
    cg = GraphCreator()
    cg.createGraph(df, pref)
    
