# データ分析で使用
import inline as inline
import matplotlib
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
# データの可視化で使用
import matplotlib.pyplot as plt
import seaborn as sns  # seaborn色の設定


sns.set_style('whitegrid')  # matplotlibをインライン表示


# csvを取り込む
df = pd.read_csv("C:/Users/aokit/PycharmProjects/maproject/input_data/amazon.csv", encoding="ISO-8859-1")
print(df.head())


# 欠損値のチェック
def see_lack(i):
    print("◆各カラムの型")
    print(i.dtypes)
    print("")
    print("◆列の中に、一つでも欠損値があるかを確かめる")
    print(i.isnull().any())
    print("")
    print("◆欠損値の数を数える")
    print(i.isnull().sum())
    print("")
    print("◆全部の(行,列)")
    print(i.shape)
    print("")
    print("◆全部が欠損している'行'があるデータを削除したら")
    data_drop_allna = i.dropna(how='all')
    print(data_drop_allna.shape)
    print("\n◆一つでも欠損している'行'があるデータを削除したら")
    data_dropna = i.dropna()
    print(data_dropna.shape)
    print("\n◆一つでも欠損している'列'があるデータを削除したら")
    data_dropna_columns = i.dropna(axis='columns')
    print(data_dropna_columns.shape)
    print("")


print(see_lack(df))

# ポルトガル語の月名を英語に変換
month_convert = {'Janeiro': 'January',
                 "Fevereiro": "Feburary",
                 "Março": "March",
                 "Abril": "April",
                 "Maio": "May",
                 "Junho": "June",
                 "Julho": "July",
                 "Agosto": "August",
                 "Setembro": "September",
                 "Outubro": "October",
                 "Novembro": "November",
                 "Dezembro": "December"}
df["month_en"] = df.month.replace(month_convert)
print(df.head())

# "year"列の型を int → objectに変換
df.year = df.year.astype("O")
print(see_lack(df))

# year列で、groupbyしたデータフレームを作成
gb_year = df.groupby("year")
# sumで確認
print(gb_year.sum())

# グラフ化①
graph1 = gb_year.sum().plot(kind="bar", figsize=[10, 5], color="r")
fig = graph1.get_figure()
fig.savefig('sample10.png')

# グラフ化②
graph2 = gb_year.sum().plot(kind="line", figsize=[10, 5], color="b")
fig = graph2.get_figure()
fig.savefig('sample11.png')

# グラフ化③
graph3 = gb_year.sum().plot(kind="area", figsize=[10, 5], color="g")
fig = graph3.get_figure()
fig.savefig('sample12.png')


# 年月別ヒートマップ作成
#yearとmonth_enでクロス集計(レポート回数合計)　
pivot_sum = df.pivot_table(values="number", index="year", columns="month_en", aggfunc=np.sum)
#月名の順番で整列
pivot_sum = pivot_sum.loc[:,['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
                             'August','September', 'October', 'November', 'December']]
#確認
print(pivot_sum)

# ヒートマップ①
heatmap1 = plt.figure(figsize=(15, 8))
sns.heatmap(pivot_sum, annot=True, fmt="1.2f", cmap='Reds')
heatmap1.savefig("sample13.png")


# ヒートマップ②
heatmap2 = plt.figure(figsize=(15, 8))
sns.heatmap(pivot_sum,annot=True,fmt="1.2f",cmap='hot_r')
heatmap2.savefig("sample14.png")

