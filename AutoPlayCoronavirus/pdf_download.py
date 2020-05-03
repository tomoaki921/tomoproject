import os
from selenium import webdriver
import time
import datetime
from tika import parser
import re

class DownloadCoronavirusData():
    def __init__(self):
        # 定数の宣言
        self.SEPALATE = '/'
        self.FILE_PATH = './CoronavirusData'
        self.DRIVER_PATH = r"C:\\Users\\aokit\\PycharmProjects\\AutoPlayCoronavirus\\venv\\Lib\\site-packages\\chromedriver_binary\\chromedriver.exe"
        self.START_URL = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00086.html'

    def make_directry(self):
        # ディレクトリの存在チェック、存在しない場合はディレクトリを作成
        if os.path.isdir(self.FILE_PATH) == False:
            os.mkdir(self.FILE_PATH)

    def download_doronavirus_Data(self):
        # Chromeを起動する --- (*1)
        driver = webdriver.Chrome(self.DRIVER_PATH)

        # リンク名の定義
        link_name = u'国内事例における都道府県別の患者報告数'
        link_name2 = u'国内における都道府県別の'
        
        # 取得する日付の配列を作成
        dt_now = datetime.datetime.now()
        # 半角対応用
        date_list = []
        # 全角対応用
        date_list_fullwidth = []
        # yyyymmdd型テキスト名保存用
        filename_list = []
        i = 0
        while (1):
            dt_now_day = dt_now.day - i
            date_list.insert(0, '令和２年'
                             + str(dt_now.month)
                             + '月'
                             + str(dt_now_day)
                             + '日版')
            date_list_fullwidth.insert(0, '令和２年'
                             + str(dt_now.month).translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                             + '月'
                             + str(dt_now_day).translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                             + '日版')
            dt_now_yyyymmdd =  dt_now + datetime.timedelta(days = -i)
            filename_list.insert(0, dt_now_yyyymmdd.strftime('%Y%m%d'))
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
            except Exception:
                """
                未解決部分！！！
                厚労省はごみ！！！！
                リンクの名前が半角だったり全角だったりする。。。
                """

                # 2秒待機
                time.sleep(2)
                try:
                    # 文字列を全角に変換して再検索
                    driver.find_element_by_partial_link_text(date_list_fullwidth[i]
                                                         ).click()
                except:
                    print(data + 'は見つかりませんでした。')
                    i += 1
                    continue
                
                    
            # 2秒待機
            time.sleep(2)
            # pdfファイル先に遷移する
            try:
                driver.find_element_by_partial_link_text(link_name).click()

            except Exception:
                driver.find_element_by_partial_link_text(link_name2).click()

            # 5秒待機
            time.sleep(5)
            # pdfのurlを取得する
            cur_url = driver.current_url
            
            
            # pdfをtxtに変換する
            file_data = parser.from_file(cur_url)
            text = file_data["content"]
            # print(text)
            text_path = self.FILE_PATH + self.SEPALATE + 'result_'+ data +  '.txt'
            file = open(text_path, 'w')
            file.write(text)
            file.close()

            # textを編集する
            # 都道府県データを作成する
            DATA = """
            北海道
            青森県
            岩手県
            宮城県
            秋田県
            山形県
            福島県
            茨城県
            栃木県
            群馬県
            埼玉県
            千葉県
            東京都
            神奈川県
            新潟県
            富山県
            石川県
            福井県
            山梨県
            長野県
            岐阜県
            静岡県
            愛知県
            三重県
            滋賀県
            京都府
            大阪府
            兵庫県
            奈良県
            和歌山県
            鳥取県
            島根県
            岡山県
            広島県
            山口県
            徳島県
            香川県
            愛媛県
            高知県
            福岡県
            佐賀県
            長崎県
            熊本県
            大分県
            宮崎県
            鹿児島県
            沖縄県
            """
            #textの空白行と行を除く
            path = text_path
            output = ''
            with open(path) as f:
                for s_line in f:
                    pre = re.sub('^([^\s]*).*', '\\1', s_line)
                    if pre in DATA and re.sub('\s', '', pre) != '':
                        s_line2 = re.sub('^([^\s]*)\s([^\s]*)\s([^\s]*)\s([^\s]*).*', '\\1,\\2,\\3,\\4', s_line)
                        str2 = re.sub('.*,(.*),.*,.*', '\\1', s_line2)
                        str2 = re.sub('\r|\n', '', str2)
                        if str2.isdigit():
                            s_line3 = re.sub('(.*),(.*),(.*),.*', '\\1,\\2,\\3', s_line2)
                        else:
                            s_line3 = re.sub('(.*),.*,(.*),(.*)', '\\1,\\2,\\3', s_line2)
                        output = output + s_line3
                    else:
                        pre = re.sub('^[^\s]*\s([^\s]*).*', '\\1', s_line)
                        if pre in DATA and re.sub('\s', '', pre) != '':
                            s_line2 = re.sub('^[^\s]*\s([^\s]*)\s([^\s]*)\s([^\s]*)\s[^\s]*.*', '\\1,\\2,\\3', s_line)
                            output = output + s_line2
            file = open(self.FILE_PATH + self.SEPALATE +filename_list[i] + '.txt', 'w', encoding="utf-8")
            file.write(output)
            f.close()
            file.close()
            
            os.remove(path)

            print(data + 'は見つかりました。')
            i += 1
            
        # 2秒待機
        time.sleep(2)
        # driverを閉じる
        driver.close()
        driver.quit()


if __name__ == "__main__":
    # instanceを作成し、プログラムを実行
    instance = DownloadCoronavirusData()
    instance.make_directry()
    instance.download_doronavirus_Data()