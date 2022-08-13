from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
# import requests
import json
from selenium.webdriver.common.by import By


# 获取cookie到本地

# 这里主要利用了selenium的get_cookies函数获取cookies。

# # 获取cookies 到本地
def get_cookies(driver):
    driver.get('https://weibo.com/login.php')
    time.sleep(20)  # 留时间进行扫码
    Cookies = driver.get_cookies()  # 获取list的cookies
    jsCookies = json.dumps(Cookies)  # 转换成字符串保存
    with open('weiboCookies.txt', 'w') as f:
        f.write(jsCookies)
    print('weiboCookies已重新写入！')


#
# # 读取本地的cookies
def read_cookies():
    with open('weiboCookies.txt', 'r', encoding='utf8') as f:
        Cookies = json.loads(f.read())
    cookies = []
    for cookie in Cookies:
        cookie_dict = {
            'domain': cookie.get('domain'),
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'expires': '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        cookies.append(cookie_dict)
    return cookies


# 初始化浏览器 打开微博登录页面
def init_browser():
    path = r'D:\Download\chromedriver_win32\chromedriver.exe '  # 指定驱动存放目录
    ser = Service(path)
    chrome_options = webdriver.ChromeOptions()
    # 把允许提示这个弹窗关闭
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.maximize_window()
    driver.get('https://weibo.com/login.php')
    time.sleep(5)
    return driver


# 读取cookies 登录微博
def login_weibo(driver):
    cookies = read_cookies()
    if cookies is None:
        print('获取cookie失败')
    else:
        print('正在加载cookies...')
        for cookie in cookies:
            driver.add_cookie(cookie)
        time.sleep(3)
        driver.refresh()  # 刷新网页
        print('cookies加载完成')

    # 检测是否登录成功
    time.sleep(5)
    try:
        bodyElement = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a[5]/div/div/div/div')
        flag = check_login(bodyElement)
        print('是否已登录：')
        print(flag)
        pass
    except Exception as identifier:
        print("未找到头像标签，cookie已过期！")
    finally:
        print("")



# 发布微博
def post_weibo(content, driver):
    time.sleep(5)
    weibo_content = driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[1]/div/textarea')
    weibo_content.send_keys(content)
    time.sleep(5)
    bt_push = driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[4]/div/button')
    time.sleep(5)
    print('点击发送')
    bt_push.click()  # 点击发布
    time.sleep(5)
    # driver.close()  # 关闭浏览器


# 检测是否登录成功
def check_login(bodyElement):
    # 读取本地cookies
    # cookies = read_cookies()
    # s = requests.Session()
    # for cookie in cookies:
    #     s.cookies.set(cookie['name'], cookie['value'])
    # response = s.get("https://weibo.com")
    # html_t = response.text

    # 检测页面是否包含有用户头像标签
    if bodyElement is None:
        return False
    else:
        return True


def send_msg_to_weibo(send_msg):
    driver = init_browser()
    login_weibo(driver)
    post_weibo(send_msg, driver)


if __name__ == '__main__':
    driver = init_browser()
    get_cookies(driver)
    # cookie登录微博

    # login_weibo(driver)
    driver.close()
    # 自动发微博
    # content = '自动微博~下班了！！！'
    # post_weibo(content, driver)