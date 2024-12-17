import httpx
import configparser
from config import CONFIG_FILE


def serverchan(title: str, content: str) -> None:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    sever_chan_send_key = config['SERVERCHAN']['sever_chan_send_key']  # server酱的send_key
    """
    通过 server酱 推送消息。
    """
    if sever_chan_send_key == '':
        print("serverChan 服务的 send_KEY 未设置!!\n取消推送")
        return
    print("serverChan 服务启动")

    data = {"text": title, "desp": content.replace("\n", "\n\n")}
    if sever_chan_send_key.find("SCT") != -1:
        url = f'https://sctapi.ftqq.com/{sever_chan_send_key}.send'
    else:
        url = f'https://sc.ftqq.com/{sever_chan_send_key}.send'
    response = httpx.Client(http2=True).post(url, data=data).json()

    if response.get("error") == 0 or response.get("code") == 0:
        print("serverChan 推送成功！")
    else:
        print(f'serverChan 推送失败！错误码：{response["message"]}')


if __name__ == "__main__":
    serverchan('', '')
