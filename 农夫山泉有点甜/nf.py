import requests
import time
import re
import os

# 用于存储日志信息的集合
log_messages = []

# 日志记录函数
def log_message(message):
    log_messages.append(message)
    print(message)  # 可选：同时打印日志

# 统一的请求头（不包括Host和Content-Type）
base_headers = {
    'Xweb_Xhr': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6605.146 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wxd79ec05386a78727/88/page-frame.html',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

# 登录函数
def login(user, apitoken):
    url = 'https://gateway.jmhd8.com/geement.usercenter/api/v1/user/information'
    headers = base_headers.copy()
    headers['Host'] = 'gateway.jmhd8.com'
    headers['Apitoken'] = apitoken  # 使用对应的Apitoken
    params = {
        'levelprocessinfo': 'false',
        'gpslocationinfo': 'false',
        'popularizeinfo': 'false',
        'disablequery_extra_field': 'true',
        'disablequery_location': 'true',
        'disablequery_memberinfo': 'true',
        'disablequery_customfield': 'true',
        'disablequery_levelinfo': 'true',
        'disablequery_perfectinfo_status': 'true',
        'disablequery_extrainformation': 'true'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'code' in data:
            if data['code'] == 200:
                if 'data' in data and 'user_id' in data['data']:
                    user_id = data['data']['user_id']
                    log_message(f"登录成功")
                    return True  # 登录成功，继续执行
            elif data['code'] == 500:
                log_message(f"Token失效，跳过该账户执行")
                return False  # Token失效，跳过该账户
        else:
            log_message(f"{user}登录失败，返回数据没有'code'字段")
            return False
    else:
        log_message(f"{user}请求失败，状态码: {response.status_code}")
        return False

# 骰子游戏
def dice_game(user, apitoken):
    url = 'https://thirtypro.jmhd8.com/api/v1/nongfuwater/snake/checkerboard/lottery'
    headers = base_headers.copy()
    headers['Host'] = 'thirtypro.jmhd8.com'
    headers['Apitoken'] = apitoken  # 使用对应的Apitoken
    data = {
        "code": "SCENE-24121018362724",
        **location_data  # 引用共享位置数据
    }
    while True:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data['code'] == 200:
                log_message("继续游戏！")
            elif response_data['code'] == 500:
                log_message("当天的游戏次数已用尽，继续执行任务列表")
                break
        else:
            log_message(f"请求失败，状态码: {response.status_code}")
            break

# 获取任务列表
def get_task_list(user, apitoken):
    url = 'https://gateway.jmhd8.com/geement.marketingplay/api/v1/task'
    headers = base_headers.copy()
    headers['Host'] = 'gateway.jmhd8.com'
    headers['Apitoken'] = apitoken  # 使用对应的Apitoken
    params = {
        'pageNum': '1',
        'pageSize': '10',
        'task_status': '2',
        'status': '1',
        'group_id': '24121016331837'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            tasks = data['data']
            task_ids = []
            for task in tasks:
                task_name = task.get('name', '未知任务')
                task_id = task.get('id', '无任务ID')
                log_message(f"任务名称: {task_name}, 任务ID: {task_id}")
                task_ids.append(task_id)
            return task_ids
        else:
            log_message("获取任务列表失败，返回数据中没有'data'字段")
    else:
        log_message(f"请求失败，状态码: {response.status_code}")
    return []

# 执行任务
def execute_task(user, apitoken, task_ids):
    url = 'https://gateway.jmhd8.com/geement.marketingplay/api/v1/task/join'
    headers = base_headers.copy()
    headers['Host'] = 'gateway.jmhd8.com'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Apitoken'] = apitoken  # 使用对应的Apitoken
    for task_id in task_ids:
        params = {
            'task_id': task_id
        }
        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['code'] == 500:
                    log_message(f"任务 {task_id} 已完成，跳到下一个任务")
                    break  # 任务完成，跳出当前循环，继续下一个任务
                else:
                    log_message(f"任务 {task_id} 执行成功，继续执行")
                    time.sleep(2)  # 延迟2秒后继续执行任务
            else:
                log_message(f"请求失败，状态码: {response.status_code}")
                break  # 请求失败，跳出循环，尝试下一个任务

# 抽奖
def lottery(user, apitoken):
    url = 'https://gateway.jmhd8.com/geement.marketinglottery/api/v1/marketinglottery'
    headers = base_headers.copy()
    headers['Host'] = 'gateway.jmhd8.com'
    headers['Content-Type'] = 'application/json'
    headers['Apitoken'] = apitoken  # 使用对应的Apitoken
    codes = ["SCENE-24121018345681", "SCENE-24121018352070"]  # 两个抽奖场景
    prizes = []
    for code in codes:
        data = {
            "code": code,
            **location_data  # 引用共享位置数据
        }
        while True:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['code'] == 200:
                    prize_name = response_data['data']['prizedto']['prize_name']
                    log_message(f"恭喜你获得了: {prize_name}")
                    prizes.append(prize_name)
                    time.sleep(2)  # 延迟2秒后继续抽奖
                elif response_data['code'] == 500:
                    log_message(f"没有抽奖机会了，跳过代码 {code}")
                    break  # 没有机会了，跳过当前的code，继续下一个code
            else:
                log_message(f"抽奖请求失败，状态码: {response.status_code}")
                break
    return prizes

# 抓包apitoken
# 从环境变量获取账号和apitoken信息
nongfu_str = os.environ.get('nongfu')
if nongfu_str:
    users = {}
    for pair in nongfu_str.split('#'):
        user, apitoken = pair.split('&')
        users[user] = apitoken
else:
    print("请设置环境变量nongfu，格式为：user1&apitoken1#user2&apitoken2")
    exit(1)

# 抓包地理位置数据
location_data = {
    "provice_name": "湖南省",
    "city_name": "长沙市",
    "area_name": "**区",
    "address": "**东站",
    "longitude": 781.326543,
    "dimension": 12.707772
}

# 主函数
def main():
    results = []
    for user, apitoken in users.items():
        result = f"账户 {user}："
        log_message(f"\n开始执行账户 {user}...")
        if login(user, apitoken):
            dice_game(user, apitoken)  # 进行骰子游戏
            task_ids = get_task_list(user, apitoken)  # 获取任务列表
            if task_ids:
                execute_task(user, apitoken, task_ids)  # 执行任务
            prizes = lottery(user, apitoken)  # 执行抽奖
            if prizes:
                result += "抽奖结果：\n"
                for prize in prizes:
                    result += f"{prize}\n"
            else:
                result += "无抽奖结果"
        else:
            result += "已失效"
        results.append(result)
    # 通知结果
    notify_results('\n'.join(results))

# 通知函数
def notify_results(message):
    if os.path.isfile('notify.py'):
        from notify import send
        send('农夫山泉任务运行结果', message)
    else:
        print("通知模块加载失败，无法发送通知。")

if __name__ == "__main__":
    main()