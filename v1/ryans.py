from time import sleep
from selenium import webdriver
from selenium.webdriver.common import keys
from bs4 import BeautifulSoup
from gsheet import authenticate

# USE THE AUTHENTICATION
client = authenticate("credentials.json")
# OPEN SHEET AND DO SOME MODIFICATIONS
sheet_url = "https://docs.google.com/spreadsheets/d/1O65J346YX-cprNxW4BW7_-L15lwnPJRFcmWDImYk01g/edit#gid=0"
workbook = client.open_by_url(sheet_url)
selected_tab = workbook.worksheet("Sheet1")

base_url = 'https://www.ryanscomputers.com'
req_specs = [
    'Model',
    'Processor Model',
    'Generation',
    'Processor Clock Speed',
    'CPU Cache',
    'Display Type',
    'Display Resolution',
    'Ram',
    'Ram Type',
    'RAM Bus (MHz)',
    'Storage',
    'Graphics Chipset',
    'Operating System',
    'Color',
    'Warranty',
    'Price',
    'Link'
]


def first_search(driver, base_url, qry):
    driver.get(base_url)
    sleep(1)
    search_box = driver.find_element_by_id('search')
    search_box.send_keys(qry)
    sleep(1)
    search_btn = driver.find_element_by_id('alg-search-btn')
    search_btn.click()


# Parse Product links from a search page
def get_product_links(driver, search_url, is_first_page):
    if not is_first_page:
        driver.get(search_url)
    sleep(1)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    page_items = soup.find_all('div', {'class': 'product-thumb'})
    product_links = []
    for item in page_items:
        x = item.find('a', href=True)
        product_links.append(x['href'])
    return product_links


# Parse Product details from a product link
def get_product_details(driver, product_link):
    driver.get(product_link)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    price = 'N/A'
    try:
        price = soup.find('span', {'class': 'price'}).text.strip()
    except:
        pass
    specs = soup.find('table').find_all('tr')
    product_details = {'Price': f"Tk {price}", 'Link': product_link}
    for spec in specs:
        sp = spec.find_all('td')
        spec_name = sp[0].text.strip()
        spec_value = sp[1].text.strip()
        product_details[f'{spec_name}'] = f'{spec_value}'
    return product_details


qry = input('Which product are you finding? - ')
# p_qry1 = qry.strip().replace(' ', '+')
# p_qry2 = qry.strip().replace(' ', '%20')
# idx = '&idx=products&p='
page_counter = 0
# search_url = base_url + p_qry1
# https://www.ryanscomputers.com/search?q=intel%20core%20i5%2010th%20gen&idx=products&p=0

starting_row = int(
    input('Write down the starting row number of Google Sheet - '))
# Open the driver
chrome_exe_src = 'C:/Development/res/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_exe_src, options=chrome_options)
# driver = webdriver.Chrome(chrome_exe_src)
first_search(driver, base_url, qry)
is_first_page = True
will_run = True
row_counter = 0
search_url = ''
while will_run and page_counter < 10:
    print(f'Digging on page {page_counter}')
    product_links = get_product_links(driver, search_url, is_first_page)
    try:
        for i in range(len(product_links)):
            details = get_product_details(driver, product_links[i])
            sleep(2)
            row_data = []
            for j in range(len(req_specs)):
                try:
                    row_data.append(details[f"{req_specs[j]}"])
                except:
                    row_data.append('N/A')
            f_row_data = [row_data]
            selected_tab.update(
                f"A{starting_row + row_counter}", f_row_data)
            row_counter += 1
        try:
            if is_first_page:
                first_search(driver, base_url, qry)
            else:
                driver.get(search_url)
            sleep(2)
            search_url = driver.find_element_by_xpath(
                '//a[@aria-label="Next"]').get_attribute("href")
            page_counter += 1
        except:
            will_run = False
    except:
        will_run = False
    is_first_page = False


driver.close()
