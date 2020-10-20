from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

USER_NAME = ''
USER_PASSWORD = ''
PPPOE_LOGIN = ''
PPPOE_PASSWORD = ''
WIRELESS_NAME = ''
WIRELESS_PASSWORD = ''
REMOTE_PORT = ''


def setup_wirless_ac(browser_object, wireless_name, wireless_password):
    # setup 2.4Ghz wireless
    browser_object.find_element_by_id('wifiSet_menu2G').click()
    browser_object.find_element_by_id('ssid').clear()
    browser_object.find_element_by_id('ssid').send_keys(wireless_name)
    browser_object.find_element_by_id('securityDisable').click()
    browser_object.find_element_by_id('wlanPwd').send_keys(wireless_password)
    browser_object.find_element_by_id('save').click()

    # setup 5Ghz wireless
    browser_object.find_element_by_id('wifiSet_menu5G').click()
    browser_object.find_element_by_id('ssid').clear()
    browser_object.find_element_by_id('ssid').send_keys(wireless_name)
    browser_object.find_element_by_id('securityDisable').click()
    browser_object.find_element_by_id('wlanPwd').send_keys(wireless_password)
    browser_object.find_element_by_id('save').click()


def merc():
    ac_5g = False

    opts = Options()
    # set headless mode. means launch browser in background mode
    opts.headless = True

    browser = webdriver.Firefox(options=opts)
    browser.get('http://192.168.1.1')
    browser.implicitly_wait(15)

    if browser.title == 'AC12G':
        ac_5g = True

    # set new user password
    browser.find_element_by_id('pwd').send_keys(USER_PASSWORD)
    browser.find_element_by_id('pwdConf').send_keys(USER_PASSWORD)
    browser.find_element_by_id('sub').send_keys(Keys.ENTER)
    # skip wizard

    # time.sleeps are workaround for freezed JS on 5G models
    time.sleep(1)
    browser.find_element_by_class_name('wizardSkip').click()

    # set pppoe_logn&password
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[3]/div[1]/ul[1]/li[2]').click()
    if ac_5g:
        browser.find_element_by_id('netWorkData_menu1').click()
    else:
        browser.find_element_by_id('netWorkData_menu0').click()
    browser.find_element_by_id('wanSel').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/fieldset/div/div/div[2]/ul[1]/li/span/ul/li[3]').click()
    browser.find_element_by_id('name').send_keys(PPPOE_LOGIN)
    browser.find_element_by_id('psw').send_keys(PPPOE_PASSWORD)
    browser.find_element_by_id('save').click()

    # wireless settings
    if ac_5g:
        setup_wirless_ac(browser, WIRELESS_NAME, WIRELESS_PASSWORD)
    else:
        browser.find_element_by_id('wifiSet_menu').click()
        browser.find_element_by_id('ssid').clear()
        browser.find_element_by_id('ssid').send_keys(WIRELESS_NAME)
        browser.find_element_by_id('securityDisable').click()
        browser.find_element_by_id('wlanPwd').send_keys(WIRELESS_PASSWORD)
        browser.find_element_by_id('save').click()

    # remote management
    browser.find_element_by_id('sysTool_menu').click()
    # workaround for freezed JS
    time.sleep(1)
    browser.find_element_by_id('remoteManageOpts').click()
    # workaround for freezed JS
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/fieldset/div/div/div[4]/ul[1]/li/span/ul/li[2]').click()
    browser.find_element_by_id('remoteWebManagePort').clear()
    browser.find_element_by_id('remoteWebManagePort').send_keys('8080')
    browser.find_element_by_id('rmtManageSave').click()

    browser.close()

    return True


if __name__ == '__main__':
    merc()
