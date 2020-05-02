from selenium import webdriver
import time
import datetime
import urllib3

# Chromeを起動する --- (*1)
path = r"C:\\Users\\aokit\\PycharmProjects\\AutoDL\\venv\\Lib\\site-packages\\chromedriver_binary\\chromedriver.exe"
driver = webdriver.Chrome(path)
# リンク名の定義
link_name = u'国内事例における都道府県別の患者報告数'
# 取得する日付の配列を作成
dt_now = datetime.datetime.now()
date_list = []
date_list_fullwidth = []
i = 0
while (1):
    date_list.insert(0, '令和２年'
                     + str(dt_now.month).translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                     + '月'
                     + str(
        dt_now.day - i)  # .translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                     + '日版')
    date_list_fullwidth.insert(0, '令和２年'
                               + str(dt_now.month).translate(
        str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                               + '月'
                               + str(dt_now.day - i).translate(
        str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                               + '日版')
    if str(i + 1) == str(dt_now.day):
        break
    i += 1
# カウント変数
i = 0
# 取得する日付数だけループ
for data in date_list:
    # URLを開く
    # Googleのページを開く --- (*2)
    driver.get('https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00086.html')
    # ページが開くまで待つ --- (*3)
    time.sleep(1)
    try:
        # ある日付のコロナウイルス感染症の現状をダウンロード
        driver.find_element_by_partial_link_text(data).click()
        # # PDFを開く
        # time.sleep(1)
        # pdfbtn = driver.find_element_by_partial_link_text(link_name).click()
        # pdfbtn.click()
    except Exception:
        # 2秒待機
        time.sleep(2)
        try:
            # 文字列を全角に変換して再検索
            driver.find_element_by_partial_link_text(date_list_fullwidth[i]).click()
            # # PDFを開く
            # time.sleep(1)
            # pdfbtn = driver.find_element_by_partial_link_text(link_name).click()
            # pdfbtn.click()
        except:
            print(data + 'は見つかりませんでした。')
    # 2秒待機
    time.sleep(2)
    print(data + 'は見つかりました。')
    i += 1
