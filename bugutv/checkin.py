import httpx
import re
import sys
import time
import configparser
import send_mail
from config import CONFIG_FILE

# global variables
r = httpx.Client(http2=True)


# 获取当前积分
def get_point():
    res = r.get('https://www.bugutv.vip/user').text
    time.sleep(1)
    point_now = re.findall(r'<span class="badge badge-warning-lighten"><i class="fas fa-coins"></i> (.*?)</span>', res)[
        0]
    return point_now


# 登录网站，并获取个人空间入口
def login(uname, upassword):
    res = r.get(r'https://www.bugutv.org').text
    time.sleep(1)
    print("准备登录")
    # 进行登录
    data = {'action': "user_login", 'username': uname, 'password': upassword, 'rememberme': 1}
    res = r.post('https://www.bugutv.vip/wp-admin/admin-ajax.php', data=data).text
    time.sleep(1)
    print('登录结果：' + res)
    if '\\u767b\\u5f55\\u6210\\u529f' in res:
        print('登录成功')
    else:
        print('登录失败')
        return False, False


# 退出登录
def logout(wpnonce):
    res = r.get(
        'https://www.bugutv.vip/wp-login.php?action=logout&redirect_to=https%3A%2F%2Fwww.bugutv.org&_wpnonce=' + wpnonce
    ).text
    print('退出登录')


# 进行签到
def checkin():
    res = r.get('https://www.bugutv.vip/user').text
    time.sleep(1)
    data_nonce = re.findall(r'data-nonce="(.*?)" ', res)[0]
    print('准备签到：获取到签到页 data-nonce: ' + data_nonce)

    data = {'action': 'user_qiandao', "nonce": data_nonce}
    res = r.post('https://www.bugutv.vip/wp-admin/admin-ajax.php', data=data).text
    time.sleep(1)
    print('签到结果：' + res)
    if '\\u4eca\\u65e5\\u5df2\\u7b7e\\u5230' in res:
        print('今日已签到，请明日再来')
    if '\\u7b7e\\u5230\\u6210\\u529f' in res:
        print('签到成功，奖励已到账：1.0积分')


def run():
    print("开始运行布谷TV自动签到脚本：")
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    default_config = config['DEFAULT']
    for i in range(3):  # 尝试3次
        if i > 0:
            print('尝试第' + str(i) + '次')
        try:
            login(default_config['uname'], default_config['upass'])

            # 获取签到前的积分数量
            point_1 = get_point()
            # 开始签到
            checkin()
            # 获取签到后的积分数量
            point_2 = get_point()

            # 发送邮件通知
            subject = '布谷TV签到：获得' + str(int(point_2) - int(point_1)) + '个积分'
            body = default_config['uname'] + '本次获得积分: ' + str(int(point_2) - int(point_1)) + '个\n' + '累计积分: ' + str(int(point_2)) + '个'

            print('****************布谷TV签到：结果统计****************')
            print(body)
            print('************************************************')
            send_mail.send_email(subject, body)
            sys.exit(0)
        except Exception as e:
            print('line: ' + str(e.__traceback__.tb_lineno) + ' ' + repr(e))
            time.sleep(10)
        finally:
            ret = r.get("https://www.bugutv.vip/user").text
            wpnonce = re.findall(r'action=logout&amp;redirect_to=https%3A%2F%2Fwww.bugutv.vip&amp;_wpnonce=(.*?)', ret)[
                0]
            # 退出登录
            logout(wpnonce)


if __name__ == '__main__':
    run()

