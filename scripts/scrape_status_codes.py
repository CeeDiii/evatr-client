#!/usr/bin/env python

import html
import pprint
import requests

from typing import Dict

from bs4 import BeautifulSoup

def extract_status_codes(html: str) -> Dict:
    '''
    Extracts status codes and their descriptions from HTML content.

    Args:
        html (str): The HTML content to extract status codes from.

    Returns:
        dict: A dictionary containing status codes as keys and their descriptions as values.
    '''
    error_codes = {}
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('td.fett')
    for row in rows:
        code = row.text.strip()
        next_td = row.find_next_sibling('td', class_='left')
        description = next_td.text.strip() if next_td else ''
        error_codes[code] = description
    return error_codes

def update_status_codes(status_code_url, save_path):
    '''
    Updates the status codes file with the error codes obtained from the given URL.

    Args:
        status_code_url (str): The URL to fetch the status codes from.
        save_path (str): The path to save the updated status codes file.

    Returns:
        None
    '''
    res = requests.get(status_code_url)
    if res.ok:
        raw_html = res.text
        codes = extract_status_codes(raw_html)
        unescaped_codes = {key: html.unescape(value) for key, value in codes.items()}
        with open(save_path, 'w', encoding='utf-8') as f:
            formatted_codes = pprint.pformat(unescaped_codes)
            f.write('status_codes = ' + formatted_codes)
            print(f'Successfully added error codes to {save_path}')
    else:
        print(f'Status Code scraping failed. Please check if the url ({status_code_url}) is still valid.')

def main():
    status_code_url = 'https://evatr.bff-online.de/eVatR/xmlrpc/codes'
    save_path = './evatr_client/status_codes.py'
    update_status_codes(status_code_url, save_path)

if __name__ == '__main__':
    main()
