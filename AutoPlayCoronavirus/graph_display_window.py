#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 01:18:39 2020

@author: kei
"""

import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial


# グラフ表示・保存する画面を作成するクラス
class GraphDisplayWindow():
    
    # コンストラクタ
    def __init__(self, figure):
        
        # 変数
        self.bgcolor = "white"
        self.default_write_pass = "./data/output/"
        
        # 画面マスターを作成
        master = tk.Tk()
        
        # 画面設定
        master.title("Graph")
        master.geometry("920x648")
        master.configure(bg=self.bgcolor)
        
        # グラフ表示ウィジェットの作成
        self.displayGraph(master, figure)
        
        # グラフ保存ボタンの作成
        self.createSaveGraphButton(master, figure)
        
        # 画面を表示
        master.mainloop()
    
    # グラフを表示
    def displayGraph(self, root, figure):
        
        canvas = FigureCanvasTkAgg(figure, root)
        canvas.get_tk_widget().pack(padx=20, pady=10)
    
    # グラフ保存ボタンを作成
    def createSaveGraphButton(self, root, figure):
        
        # 実行ボタンを作成
        action = partial(self.__saveFileDialog, root, figure)
        button = tk.Button(root, text="保存", command=action)
        
        # 色を設定
        button.configure(bg=self.bgcolor)
        
        # ボタンを表示
        button.pack(padx=20, pady=10)
        
        return
    
    # 保存ボタンが押下された場合起動される
    # ポップアップウィンドウが出て、保存先を指定できる
    def __saveFileDialog(self, root, figure):
        
        # 保存用ファイルダイアログを表示
        save_path = fd.asksaveasfilename(initialdir=self.default_write_pass, 
                                         defaultextension=".png")
                
        # パスが帰ってきた場合
        if save_path:
            
            # ファイルを保存
            figure.savefig(save_path, facecolor=figure.get_facecolor())  
            
            # 保存成功メッセージの表示
            self.__createLabelSave(root, save_path)
        
        return
    
    # 画像保存時のラベルを表示するメソッド
    def __createLabelSave(self, root, path):
        
        # メッセージを設定
        text= str(path) + "　にグラフを保存しました。"
        
        # ラベルを設定
        label = tk.Label(root, text=text)
        
        # 色を設定
        label.configure(bg=self.bgcolor, fg="lime")
        
        # ラベルを表示
        label.pack(padx=20, pady=15)
        
        
if __name__ == "__main__":
    figure = plt.figure()
    GraphDisplayWindow(figure)