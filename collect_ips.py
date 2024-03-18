import os
import re
import requests
from bs4 import BeautifulSoup

# 目标URL列表
urls = ['https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
        'https://ip.164746.xyz']

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储响应时间小于300毫秒的IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            
            # 如果找到IP地址,则进行ping测试
            for ip in ip_matches:
                # 执行ping命令
                response = os.popen(f'ping -n 1 {ip}').read()
                
                # 使用正则表达式匹配ping响应时间
                ping_time = re.findall(r'时间=(\d+)ms', response)
                
                # 如果ping响应时间存在且小于300毫秒，则保存IP地址
                if ping_time and int(ping_time[0]) < 300:
                    file.write(ip +  ':8443#CF''\n')

print('响应时间小于300毫秒的IP地址已保存到ip.txt文件中。')
