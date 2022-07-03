import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Selenium4対応済


def set_driver(hidden_chrome: bool=False):
    '''
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
    '''
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）の設定
    if hidden_chrome:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

def divide(x, path):
    try:
        print(54/x)
    except:
        #ログ出力(エラー)
        with open(path, mode='a', encoding='utf-8') as f:
            f.write("\nエラー(例外)")

def main():
    '''
    main処理
    '''
    # ログファイルパス
    path = 'log.txt'
    
    # search_keyword = "高収入"
    # 検索ワードをユーザ入力
    search_keyword = input("検索ワードを入力してください。")
    
    # driverを起動
    driver = set_driver()

    # Webサイトを開く
    #driver.get("https://tenshoku.mynavi.jp/")
    
    # Webサイトを開く　オプション対応ver
    driver.get(f"https://tenshoku.mynavi.jp/list/kw{search_keyword}/?jobsearchType=14&searchType=18")
    #time.sleep(5)
    time.sleep(1)
    
    '''
    ポップアップを閉じる
    ※余計なポップアップが操作の邪魔になる場合がある
      モーダルのようなポップアップ画面は、通常のclick操作では処理できない場合があるため
      excute_scriptで直接Javascriptを実行することで対処する
    '''
    driver.execute_script('document.querySelector(".karte-close").click()')
    #time.sleep(5)
    time.sleep(1)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    '''
    find_elementでHTML要素(WebElement)を取得する
    byで、要素を特定する属性を指定するBy.CLASS_NAMEの他、By.NAME、By.ID、By.CSS_SELECTORなどがある
    特定した要素に対して、send_keysで入力、clickでクリック、textでデータ取得が可能
    '''    
    # # 検索窓に入力
    # driver.find_element(by=By.CLASS_NAME, value="topSearch__text").send_keys(search_keyword)
    # # 検索ボタンクリック
    # driver.find_element(by=By.CLASS_NAME, value="topSearch__button").click()

    # 企業名、求人タイトル一覧を格納するリストを準備
    name_elms=[]
    
    # 例外の処理　例外処理お試し　特に意味がない処理
    divide(0, path)
    
    # whileでfind_element_by_link_textがbreakするまでループ
    while True:
        '''
        find_elements(※複数形)を使用すると複数のデータがListで取得できる
        一覧から同一条件で複数のデータを取得する場合は、こちらを使用する
        '''
        name_elms = driver.find_elements(by=By.CLASS_NAME, value="cassetteRecruit__heading")
        # 空のDataFrame作成
        df = pd.DataFrame()

        # 1ページ分繰り返し
        print(len(name_elms))
        '''
        name_elmsには１ページ分の情報が格納されているのでforでループさせて１つずつ取り出して、Dataframeに格納する
        '''
        cnt = 0
        for name_elm in name_elms:
            cnt = cnt + 1
            # ログ出力(件数)
            with open(path, mode='a', encoding='utf-8') as f:
                f.write(f"\n{cnt}件目情報取得")
            
            print(name_elm.text)
            split_list = name_elm.text.splitlines()
            # DataFrameに対して辞書形式でデータを追加する
            df = df.append(
                {"会社名": split_list[0], 
                "求人タイトル": split_list[1],
                "項目C": "項目C"}, 
                ignore_index=True)
            
        # 次へボタンまでスクロール。ボタンは見えてないと押せないみたいだから。
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 次へをクリックしページ遷移する
        try:
            driver.find_element(by=By.LINK_TEXT, value="次へ").click()
            #time.sleep(3)
            time.sleep(1)
        except Exception:
            #browser.quit()
            break
    
    # CSV出力
    df.to_csv('out.csv') 
        
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()