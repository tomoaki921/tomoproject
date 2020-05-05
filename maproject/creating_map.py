import folium
import pandas as pd

#地図を作成する
map = folium.Map(
    location=[35.681236, 139.767125],  # 地図の中央にくる緯度と経度を指定
    zoom_start=12)  # 初期表示の縮尺を指定
map.save('sample1.html')


#全山手線の駅をプロットする
data = pd.read_csv('input_data/yamanote.csv')
for k, v in data.iterrows():
    pin = [v.latitude, v.longitude]
    folium.Marker(pin,
                  popup=v.station,
                  icon=folium.Icon(color="red", icon="flag")
                  ).add_to(map)

#全東京都コンビニエンスストアをプロットする
# data = pd.read_csv('input_data/convenience_store.csv')
# for k, v in data.iterrows():
#     pin = [v.latitude, v.longitude]
#     folium.Marker(pin,
#                   popup=v.name,
#                   icon=folium.Icon(color="blue", icon="flag")
#                   ).add_to(map)
# map.save('sample2.html')

