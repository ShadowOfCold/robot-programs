# АБГВА
# А: Google Chrome
# Б: locked_out_user (standard_user) / secret_sauce
# Г: Сортировка по цене (high to low)
# В: Добавить самый дешевый товар (обратите внимание на сортировку!).
# A: Добавить товар в корзину и завершить работу скрипта.

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome()
browser.get("https://www.saucedemo.com/")

username = browser.find_element(By.ID, "user-name")
password = browser.find_element(By.ID, "password")
username.send_keys("locked_out_user")
password.send_keys("secret_sauce")
browser.find_element(By.ID, "login-button").click()
error = browser.find_element(By.CSS_SELECTOR, "[data-test='error']")
if "locked out" in error.text.lower():
    username.clear()
    username.send_keys("standard_user")
    browser.find_element(By.ID, "login-button").click()

select = Select(browser.find_element(By.CLASS_NAME, "product_sort_container"))
select.select_by_visible_text("Price (high to low)")
time.sleep(1)

browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
buttons = browser.find_elements(By.CLASS_NAME, "btn_inventory")
buttons[-1].click()
time.sleep(1)