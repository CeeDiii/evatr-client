#!/usr/bin/env python

import html
import pprint
import requests

from bs4 import BeautifulSoup

def extract_error_codes(html):
    error_codes = {}
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('td.fett')
    for row in rows:
        code = row.text.strip()
        next_td = row.find_next_sibling('td', class_='left')
        description = next_td.text.strip() if next_td else ''
        error_codes[code] = description
    return error_codes

res = requests.get('https://evatr.bff-online.de/eVatR/xmlrpc/codes')
if res.ok:
    raw_html = res.text
    codes = extract_error_codes(raw_html)
    unescaped_codes = {key: html.unescape(value) for key, value in codes.items()}
    with open('./error-code.py', 'w', encoding='utf-8') as f:
        formatted_codes = pprint.pformat(unescaped_codes)
        f.write('data = ' + formatted_codes)
    print('Successfully added error codes to error-code.py')
