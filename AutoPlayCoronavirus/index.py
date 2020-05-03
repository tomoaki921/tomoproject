#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:55:07 2020

@author: kei
"""

import tkinter as tk
from tkinter import ttk
import create_graph as cg
import graph_display_window as gdw
import pdf_download as pdfdl
from functools import partial



class IndexWindow():

    # コンストラクタ
    def __init__(self):

        # 変数
        self.prefectures_list = ['北海道', '青森県', '岩手県', '宮城県',
                                 '秋田県', '山形県', '福島県', '茨城県',
                                 '栃木県', '群馬県', '埼玉県', '千葉県',
                                 '東京都', '神奈川県', '新潟県', '山梨県',
                                 '長野県', '富山県', '石川県', '福井県',
                                 '岐阜県', '静岡県', '愛知県', '三重県',
                                 '滋賀県', '京都府', '大阪府', '兵庫県',
                                 '奈良県', '和歌山県', '鳥取県', '島根県',
                                 '岡山県', '広島県', '山口県', '徳島県',
                                 '香川県', '愛媛県', '高知県', '福岡県',
                                 '佐賀県', '長崎県', '熊本県', '大分県',
                                 '宮崎県', '鹿児島県', '沖縄県']
        self.bgcolor = "white"
        self.image_path1 = "./data/image/case.png"
        self.image_path2 = "./data/image/crate_heatmap.png"
        self.read_dir_path = "./CoronavirusData/*"
        self.img1 = None
        self.img2 = None
        self.error_label_flag = False
        self.error_label_flag2 = False
        self.combo_pref = None
        self.combo_japan = None

        # データを再取得が不要の際はコメントアウトする
        dlcd = pdfdl.DownloadCoronavirusData()
        dlcd.make_directry()
        dlcd.download_doronavirus_Data()

        # 画面マスターを作成
        master = tk.Tk()

        # 画面設定
        master.title("Creating Graph Tool")
        window_w = 710
        window_h = 440
        window_geo = str(window_w) + "x" + str(window_h)
        master.geometry(window_geo)
        master.configure(bg=self.bgcolor)

        # メインフレームを作成
        self.createMainFrame(master, window_w, window_h)

        # 画面を表示
        master.mainloop()

    def createMainFrame(self, root, height, width):

        frame = tk.Frame(root,height=height, width=width, relief='flat',
                          background=self.bgcolor)
        frame.grid()

        self.createSubFramePref(frame, height, width/2)
        self.createSubFrameJapan(frame, height, width/2)

        return frame

    def createSubFramePref(self, root, height, width):

        frame = tk.Frame(root,height=height, width=width, relief='flat',
                          borderwidth=5, background=self.bgcolor)
        frame.pack(fill=tk.BOTH, side=tk.LEFT)

        # プルダウン案内メッセージを表示
#        self.createLabelPullDown(frame)

        # 都道府県選択プルダウンの作成
        self.combo_pref = self.createPullDown(frame, self.prefectures_list, 12)

        # 実行ボタンの作成
        self.createExeButton1(frame)

        return


    def createSubFrameJapan(self, root, height, width):

        frame = tk.Frame(root,height=height, width=width, relief='flat',
                          borderwidth=5, background=self.bgcolor)
        frame.pack(fill=tk.BOTH, side=tk.LEFT)

        # プルダウン案内メッセージを表示
        do = cg.DataOperator()
        self.date_list = do.setDateList(self.read_dir_path)

        # 日付洗濯プルダウンの作成
        self.combo_japan = self.createPullDown(frame, self.date_list, 0)

        # 実行ボタンの作成
        self.createExeButton2(frame)

        return

    def createLabelPullDown(self, root):

        label = tk.Label(root,
                         text="新型コロナ感染者数推移グラフを表示したい都道府県を選択してください。")
        label.configure(bg=self.bgcolor)
        label.pack(padx=5, pady=20)

    # プルダウンを作成
    def createPullDown(self, root, combo_list, current_index):

        # プルダウンの設定
#        ttk.Style().configure("TCombobox", fieldbackground="red")
#        root.option_add("*TCombobox.fieldBackground", 'red')

        style = ttk.Style()
        style.configure('TCombobox', fieldbackground='red')


        # プルダウンウィジェットの作成
        combo = ttk.Combobox(root,values=combo_list,
                             state='readonly')
        combo.configure(style="TCombobox")

        # 初期状態を１２番目（東京都）に設定
        combo.current(current_index)

        # プルダウンの表示
        combo.pack(padx=5, pady=20)

        return combo

    # プルダウンのコンフィグ設定および取得関数
    def getComboStyle(self):
        combo_style = ttk.Style()
        combo_style.theme_create('combostyle', parent='alt',
                                 settings={'TCombobox':
                                          {'configure':
                                          {'fieldbackground': 'darkgray',
                                           'selectbackground': 'red',
                                           'selectforeground': 'black'}}}
                                )

        return combo_style

    # 実行ボタンを作成
    def createExeButton1(self, root):

        # 実行ボタンを作成
        action = partial(self.__pushCreateExeButton, root, self.prefectures_list)
        self.img1 = tk.PhotoImage(file=self.image_path1)
        button = tk.Button(root, image=self.img1, height=260, width=320,
                           command=action)

        # ボタンを表示
        button.pack(padx=10, pady=20)

        return


    # 実行ボタンを押下したアクション
    def __pushCreateExeButton(self, root, pull_list):

        #現在選択されている要素を取得
        result = self.combo_pref.current()
        pref = pull_list[result]

        # GraphCreator インスタンスを作成
        do = cg.DataOperator()

        # csvデータの取得
        df = do.getCsvDataPref(pref)

#        df = False

        # CSVデータが取得できなかった場合、エラーメッセージを表示
        if df is False:

            if self.error_label_flag is True:
                return

            self.__createLabelError(root)
            self.error_label_flag = True
            return

        # error_label_flag をフォルスに戻す
        self.error_label_flag = False

        # グラフ作成
        gc = cg.GraphCreator()
        figure = gc.createGraph(df, pref)

        # グラフ表示
        gdw.GraphDisplayWindow(figure)

        return

    # エラー時のラベルを表示するメソッド
    def __createLabelError(self, root):

        # メッセージを設定
        text="選択したデータはありません。"

        # ラベルを設定
        label = tk.Label(root, text=text)
        print(text)

        # 色を設定
        label.configure(bg=self.bgcolor, fg="red")

        # ラベルを表示
        label.pack(padx=20, pady=10)


    # 実行ボタンを作成
    def createExeButton2(self, root):

        # 実行ボタンを作成
        action = partial(self.__pushCreateExeButton2, root, self.date_list)
        self.img2 = tk.PhotoImage(file=self.image_path2)
        button = tk.Button(root, image=self.img2, height=260, width=320,
                           command=action)

        # ボタンを表示
        button.pack(padx=10, pady=20)

        return

    def __pushCreateExeButton2(self, root, pull_list):

        #現在選択されている要素を取得
        result = self.combo_japan.current()
        date_date = pull_list[result]
        date = date_date.replace("/", "")

        # GraphCreator インスタンスを作成
        do = cg.DataOperator()

        # csvデータの取得
        df = do.getCsvDataDate(date)

        # CSVデータが取得できなかった場合、エラーメッセージを表示
        if df is False:

            if self.error_label_flag2 is True:
                return

            self.__createLabelError(root)
            self.error_label_flag2 = True
            return

        # error_label_flag をフォルスに戻す
        self.error_label_flag2 = False

        # グラフ作成
        gc = cg.GraphCreator()
        figure = gc.createInfMapJapan(df, date_date)

        # グラフ表示
        gdw.GraphDisplayWindow(figure)

        return



if __name__ == "__main__":

    IndexWindow()