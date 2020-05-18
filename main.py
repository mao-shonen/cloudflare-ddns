import os
import random
import requests
import logging
from time import sleep
from ipaddress import ip_address


CLOUDFLARE_API_URL = 'https://api.cloudflare.com/client/v4'
CLOUDFLARE_TOKEN = os.environ.get('CLOUDFLARE_TOKEN')
CLOUDFLARE_ZONE_ID = os.environ.get('CLOUDFLARE_ZONE_ID')
CLOUDFLARE_RECORDS = os.environ.get('CLOUDFLARE_RECORDS').split('|')
UPDATE_RATE = float(os.environ.get('UPDATE_RATE', 60.0))
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
GET_IP_URLS = [
    'ifconfig.io',
    'ifconfig.im',
    'ifconfig.ca',
    'ifconfig.co',
    'ifconfig.tw',
    'ifconfig.me',
    'ifconfig.cc',
    'ifconfig.ru',
]

client = requests.session()
cloudflare_auth_headers = dict(Authorization=f'Bearer {CLOUDFLARE_TOKEN}')
record_ids = {}
last_ip = None

logging.basicConfig(level=getattr(LOG_LEVEL, LOG_LEVEL, 'INFO'), format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def getRecordId(record_name):
    if record_name not in record_ids:
        res = client.get(f'{CLOUDFLARE_API_URL}/zones/{CLOUDFLARE_ZONE_ID}/dns_records', headers=cloudflare_auth_headers, params=dict(name=record_name), timeout=5.0)
        record_ids[record_name] = res.json()['result'][0]['id']
    return record_ids[record_name]


def dnsRecordUpdate(ip):
    for record in CLOUDFLARE_RECORDS:
        try:
            record_id = getRecordId(record.strip())
            res = client.patch(f'{CLOUDFLARE_API_URL}/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}', headers=cloudflare_auth_headers, json=dict(content=str(ip)), timeout=5.0)
            logging.info(f'update {record} success')
        except Exception as e:
            logging.exception(f'update {record} fail')


if __name__ == '__main__':
    while True:
        random.shuffle(GET_IP_URLS)
        for url in GET_IP_URLS:
            try:
                res = client.get(f'http://{url}', headers={'User-Agent': 'curl'}, timeout=5.0)
                ip = ip_address(res.text.strip())
                if ip == last_ip:
                    logging.info(f'IP not change')
                else:
                    logging.info(f'IP change to {ip}')
                    dnsRecordUpdate(ip)
                    last_ip = ip
                break
            except requests.Timeout:
                continue
            except Exception as e:
                logging.exception(f'error: {e}')

        logging.info(f'All updated. next update after {UPDATE_RATE} seconds')
        sleep(UPDATE_RATE)
