const notify = require("./sendNotify");


const goods = [
    {
        "name": "音响",
        "id": "994210179233"
    },
    {
        "name": "路由器",
        "id": "994210179247"
    }
]

async function monitorGood(good) {
    let res = await fetch(`https://card.10010.com/mall-order/qryStock/v2?goodsId=${good.id}&cityCode=132&mode=1`, {
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7,ja;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        },
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": null,
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    }).then(res => res.json());

    if (res.code !== "0000") return;
    let item = res?.data?.bareMetal?.modelsList?.[0]
    if (!item) return;
    let amount = item.articleAmount;
    if (amount > 0) {
        let msg = good.name + "有货了：" + amount;
        console.log(msg);
        return msg;
    }
    console.log(good.name + "没货", item);
    return;
}

const main = async () => {
    let msgList = await Promise.all(goods.map(monitorGood))
    msgList = msgList.filter(m => m);
    if (msgList.length > 0) {
        console.log(msgList)
        notify.sendNotify('联通助手', msgList.join('\r\n'));
    }
}





main();
