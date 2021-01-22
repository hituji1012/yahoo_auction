from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import os
from time import sleep

# 設定
user = '' # ユーザーID
password = '' # パスワード
url = 'https://login.yahoo.co.jp/config/login?auth_lv=pw&.src=auc&.done=https%3A%2F%2Fauctions.yahoo.co.jp%2Fsell%2Fjp%2Fshow%2Fsubmit?category=0'
chrome_path = 'chromedriver.exe'

# 出品情報
product_img = 'product.jpg'
title = 'sample 出品'
category = '26395' # idの番号
new_old = '未使用に近い'
description = 'この商品はサンプルです。'
product_return = True
location = '東京都'
shipping_charge = '出品者' # 出品者/落札者
shipping_end = 1 # 2日後 = 設定値+1
shipping_time = 1 # 午前1時から午前2時 リストのIndex番号
price = 10000000

"""
以下、自動操作
"""

# chrome 起動
options = Options()
options.add_argument('--incognito') # シークレットモード
driver = webdriver.Chrome(os.path.abspath(chrome_path), options=options)

sleep(1)
driver.get(url)

# ログイン
sleep(1)
driver.find_element_by_id('username').send_keys(user)
driver.find_element_by_id('btnNext').click()

sleep(1)
driver.find_element_by_id('passwd').send_keys(password)
driver.find_element_by_id('btnSubmit').click()

# ポップアップの削除
driver.execute_script('document.getElementById("js-ListingModal").style.display = "none";')

# 画像 複数枚貼る
sleep(1)
driver.find_element_by_id('selectFile').send_keys(os.path.abspath(product_img))
driver.find_element_by_id('selectFile').send_keys(os.path.abspath(product_img))

# タイトル
driver.find_element_by_id('fleaTitleForm').send_keys(title)

# カテゴリ
driver.execute_script(f'arguments[0].value = {category}', driver.find_element_by_name('category'))

# 商品の状態
Select(driver.find_element_by_name('istatus')).select_by_visible_text(new_old)

# 返品 /html/body/form/div/div[13]/label/
if not product_return:
    driver.find_element_by_xpath('/html/body/form/div/div[13]/label[(contains(@class, "is-check"))]').click()
else:
    driver.find_element_by_xpath('/html/body/form/div/div[13]/label[not(contains(@class, "is-check"))]').click()

# 説明 iframeのrteEditorComposition0に切り替え
iframe = driver.find_element_by_id('rteEditorComposition0')
driver.switch_to.frame(iframe)
driver.find_element_by_id('0').send_keys(description)
driver.switch_to.default_content()

# 発送元の地域　リストの中から文字列で都道府県選択
Select(driver.find_element_by_name("loc_cd")).select_by_visible_text(location)

# 送料負担　/html/body/form/div/section[2]/div[6]/label[1]
if shipping_charge=="出品者":
    driver.find_element_by_xpath('/html/body/form/div/section[2]/div[6]/label[(contains(@class, "is-check"))]').click()
else:
    driver.find_element_by_xpath('/html/body/form/div/section[2]/div[6]/label[not(contains(@class, "is-check"))]').click()

# 配送方法　ネコポス選択
driver.find_element_by_xpath('/html/body/form/div/div[21]/div/section[1]/div[2]/ul/li[1]/label[not(contains(@class, "is-check"))]').click()

# 発送までの日数 2-3日を選択
driver.find_element_by_xpath('/html/body/form/div/div[22]/div[2]/label[not(contains(@class, "is-check"))]').click()

# 終了日時
Select(driver.find_element_by_id("ClosingYMD")).select_by_index(shipping_end)
Select(driver.find_element_by_id("ClosingTime")).select_by_index(shipping_time)

# 開始価格
driver.find_element_by_id("auc_StartPrice").clear()
driver.find_element_by_id("auc_StartPrice").send_keys(price)

# 確認ボタン
driver.find_element_by_xpath('/html/body/form/div/ul/li/input').click()

# 確認画面の処理
print("あとは出品ボタンを押せば完成です！")

sleep(3)
driver.close()
driver.quit()

print("Done.")