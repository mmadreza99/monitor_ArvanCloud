import requests

last_ips = []
all_ips = []
new_ips = []
lost_ips = []
ip_list = []


def save_file(lasts, all, lost):
    with open(f'last_ips.txt', 'w') as f:
        f.writelines(lasts)

    with open('all_ips.txt', 'a') as f:
        f.writelines(all)

    with open('lost.txt', 'a') as f:
        f.writelines(lost)


def open_file():
    with open(f'last_ips.txt', 'r') as f:
        last_ips = f.readlines()

    with open('all_ips.txt', 'r') as f:
        all_ips = f.readlines()

    return all_ips, last_ips


def send_sms(ips, lost):
    print('new', ips)
    print('lost', lost)


def remove_ip_in_all_ip(ip):
    with open('all_ips.txt', 'r') as f:
        all = f.readlines()

    all.remove(ip)

    with open('all_ips.txt', 'w') as f:
        f.writelines(all)

try:
    all_ips, last_ips = open_file()
except:
    all_ips, last_ips = [], []

response = requests.get('https://www.arvancloud.com/fa/ips.txt')

ips = response.text.split('\n')

for ip in ips:
    ip_list.append(f'{ip}\n')

for ip in ip_list:
    if ip not in last_ips:
        new_ips.append(ip)

for ip in all_ips:
    if ip not in ip_list:
        lost_ips.append(ip)
        remove_ip_in_all_ip(ip)

if new_ips or lost_ips:
    send_sms(new_ips, lost_ips)


save_file(ip_list, new_ips, lost_ips)
