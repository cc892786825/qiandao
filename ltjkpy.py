import requests

from notify import send

msg = ''


def jk():
    global msg
    ids = [994210179233, 994211139173, 994210179247]
    for id in ids:
        url = "https://card.10010.com/mall-order/qryStock/v2"
        params = {
            'goodsId': id,
            'cityCode': "110",
            'mode': "1"}
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 14; PJX110 Build/UKQ1.231108.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.39 Mobile Safari/537.36; unicom{version:android@11.0900,desmobile:0};devicetype{deviceBrand:OnePlus,deviceModel:PJX110}"}
        res = requests.get(url, params=params, headers=headers).json()
        nn = [item["SHOW_NAME"] for item in res['data']['bareMetal']["modelsList"]]
        name = [item["COLOR_DESC"] for item in res['data']['bareMetal']["modelsList"]]
        sl = [item["articleAmount"] for item in res['data']['bareMetal']["modelsList"]]
        for v, n, l in zip(nn, name, sl):
            print(v, n, l)
            if l > 0:
                msg += f'{v},{n}:{l}'
    if msg:
        send('商城监控', msg)


if __name__ == '__main__':
    jk()
