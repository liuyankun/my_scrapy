# -*- coding:utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver = "./chromedriver"

driver = webdriver.Chrome(executable_path=chromedriver)

print('start')
driver.get("http://www.baidu.com/")

assert u"百度一下" in driver.title

elem = driver.find_element_by_name("wd")

elem.send_keys("selenium")

elem.send_keys(Keys.RETURN)

assert "selenium" in driver.title

print('end')

#driver.close()


