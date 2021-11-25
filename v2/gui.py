import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import threading
from tkinter import *


def generate_file_name(file_name, file_ext):
    file_no = 0
    file_name = file_name.replace(' ', '_')
    current_datetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    is_not_done = True
    while is_not_done:
        file_path = f"{file_name}_{current_datetime}_{file_no}.{file_ext}"
        if os.path.exists(file_path):
            file_no += 1
        else:
            is_not_done = False
            return file_path


def pull_ryans_data(search_input):
    search_url_model = 'https://www.ryanscomputers.com/api/search?keyword={}&returnType=searchPageHTML'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    search_term = search_input.replace(' ', '%2520')
    print('\nCollecting data...')
    resp = requests.get(search_url_model.format(search_term), headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    items = []
    products = []

    search_items = soup.find_all(attrs={'class': 'ais-hits--item'})
    for item in search_items:
        item_link = item.find(
            attrs={'class': 'product-content'}).find('a')['href']
        items.append(item_link)

    csv_headers = ['Image', 'Title', 'ID', 'Regular Price', 'Special Price']
    for link in items:
        resp = requests.get(link, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        product_data = {}

        try:
            product_data['Image'] = soup.find(attrs={'id': 'listMainImg'})[
                'data-zoom-image']
        except:
            pass
        try:
            product_details_short = soup.find(
                'div', attrs={'class': 'produc-details-short'})
        except:
            pass
        try:
            product_data['Title'] = product_details_short.find(
                'h1', attrs={'class': 'title'}).text
        except:
            pass
        try:
            product_data['ID'] = product_details_short.find('p').text
        except:
            pass
        try:
            product_data['Regular Price'] = product_details_short.find(
                'span', attrs={'class': 'old-price'}).text
        except:
            pass
        try:
            product_data['Special Price'] = product_details_short.find(
                'span', attrs={'class': 'price'}).text
        except:
            pass

        try:
            info_section = soup.find('div', attrs={'id': 'information'}).find_all(
                'div', attrs={'class': 'specs-item-wrapper'})

            for info in info_section:
                try:
                    row = info.find(
                        'div', attrs={'class': 'row'}).find_all('div')
                    key = row[0].text.strip()
                    if key not in csv_headers:
                        csv_headers.append(key)
                    product_data[key] = row[1].text.strip()
                except:
                    pass
        except:
            pass
        products.append(product_data)
    return products, csv_headers


def main():
    search_input = input('Search any product: ')
    ryans_data = pull_ryans_data(search_input)

    output_file = generate_file_name(
        f"{search_input.replace(' ', '_')}", 'csv')
    output_folder = 'output_files'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    complete_output_file_path = f'{output_folder}/{output_file}'

    with open(complete_output_file_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ryans_data[1])
        writer.writeheader()
        for d in ryans_data[0]:
            writer.writerow(d)

    print(f'\nYour data is ready. Please check the {output_file} file.')


root = Tk()

root.title('Make Computer Market Research')
root.geometry('500x300')

root.mainloop()
