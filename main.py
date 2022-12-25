import json
import random
import re

from threading import Thread

import requests
from bs4 import BeautifulSoup


from selenium.webdriver.common.by import By


class OlxDataLoader(Thread):
    def get_list_of_urls_olx(self, url: str) -> list[str]:
        response = requests.get(url)
        BeautifulSoup(response.text, "html.parser")
        pattern = re.compile(r'"urlPath\\":\\"(.*?\.html)\\"')
        matches = pattern.finditer(response.text)
        list_of_urls = []
        for match in matches:
            list_of_urls.append(match.groups()[0].replace("\\\\", "\\"))
        return list_of_urls

    def run(self) -> None:
        list_of_urls = self.get_list_of_urls_olx(
            url="https://www.olx.kz/d/elektronika/noutbuki-i-aksesuary/noutbuki/q-macbook-2021/?search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bfilter_enum_laptop_manufacturer%5D%5B0%5D=2112"
        )
        if len(list_of_urls) <= 50:
            list_of_urls += self.get_list_of_urls_olx(
                url="https://www.olx.kz/d/elektronika/noutbuki-i-aksesuary/noutbuki/q-macbook-2021/?page=2&search%5Bfilter_enum_laptop_manufacturer%5D%5B0%5D=2112&search%5Bfilter_enum_state%5D%5B0%5D=used"
            )
        dict_of_data = {}
        for index, url_path in enumerate(list_of_urls):
            url = f"https://www.olx.kz{url_path}".replace("\\u002F", "/")
            from selenium import webdriver
            import time

            driver = webdriver.Chrome(r"./driver/chromedriver")
            driver.get(url)
            driver.maximize_window()
            time.sleep(7 + random.randint(1, 3))
            dict_of_page = {}
            try:
                price_element = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[3]/div[1]/div[2]/div[3]/h3'
                )
                dict_of_page["price"] = price_element.text
            except:
                dict_of_page["price"] = None
            try:
                device_name = driver.find_element(
                    By.XPATH, '//*[@id="root"]/div[1]/div[3]/div[3]/div[1]/div[2]/div[2]/h1'
                )
                dict_of_page["device_name"] = device_name.text
            except:
                dict_of_page["device_name"] = None
            try:
                seller_name = driver.find_element(
                    By.XPATH,
                    '//*[@id="root"]/div[1]/div[3]/div[3]/div[2]/div[1]/div[2]/div/a/div/div[2]/h4',
                )
                dict_of_page["seller_name"] = seller_name.text
            except:
                dict_of_page["seller_name"] = None
            try:
                device_description = driver.find_element(
                    By.XPATH,
                    '// *[ @ id = "root"] / div[1] / div[3] / div[3] / div[1] / div[2] / div[8] / div',
                )
                dict_of_page["description"] = device_description.text
            except:
                dict_of_page["description"] = None
            try:
                phone_number_element = driver.find_element(
                    By.XPATH, '//button[@data-cy = "ad-contact-phone"]'
                )
                driver.execute_script("arguments[0].click();", phone_number_element)
                time.sleep(3)
                dict_of_page["phone_number"] = phone_number_element.text
            except:
                dict_of_page["phone_number"] = None
            dict_of_data[url] = dict_of_page
            driver.close()

            print(dict_of_page)

            if index % 10 == 0 and index != 0:
                time.sleep(300)

            if len(dict_of_data) == 50:
                break

        with open("olx_data.json", "w+", encoding="utf-8") as outfile:
            json.dump(dict_of_data, outfile, indent=4, ensure_ascii=False)


class KolesaDataLoader(Thread):
    def get_list_of_urls_kolesa(self, url: str):
        response = requests.get(url)
        BeautifulSoup(response.text, "html.parser")

        with open("auto_data.txt", "w+", encoding="utf-8") as data:
            data.write(response.text)
        pattern = re.compile(r'"url":"(https:\\/\\/kolesa.kz\\/a.*?)"')
        matches = pattern.finditer(response.text)
        list_of_urls = []
        for match in matches:
            print(match.group())
            list_of_urls.append(match.groups()[0].replace("\\", ""))
        return list_of_urls

    def run(self) -> None:
        list_of_urls = self.get_list_of_urls_kolesa(
            url="https://kolesa.kz/cars/toyota/avtomobili-s-probegom/camry/?year[from]=2021"
        )
        if len(list_of_urls) <= 49:
            list_of_urls += self.get_list_of_urls_kolesa(
                url="https://kolesa.kz/cars/toyota/avtomobili-s-probegom/camry/?year[from]=2021&page=2"
            )
            list_of_urls += self.get_list_of_urls_kolesa(
                url="https://kolesa.kz/cars/toyota/avtomobili-s-probegom/camry/?year[from]=2021&page=3"
            )

        dict_of_data = {}
        for index, url_path in enumerate(list_of_urls):
            url = url_path
            from selenium import webdriver
            import time

            driver = webdriver.Chrome(r"./driver/chromedriver")
            driver.get(url)
            dict_of_page = {}
            driver.maximize_window()
            time.sleep(7 + random.randint(1, 3))
            try:
                item_name = driver.find_element(
                    By.XPATH, "/html/body/main/div/div/div/header/div[1]/h1"
                )
                dict_of_page["item_name"] = item_name.text
            except:
                dict_of_page["item_name"] = None
            try:
                description = driver.find_element(
                    By.XPATH,
                    "/html/body/main/div/div/div/section/div[2]/div[3]/div[3]/p",
                )
                dict_of_page["description"] = description.text
            except:
                dict_of_page["description"] = None
            try:

                price = driver.find_element(
                    By.XPATH,
                    "/html/body/main/div/div/div/section/div[1]/div[1]/div[1]/div[1]",
                )
                dict_of_page["price"] = price.text
            except:
                dict_of_page["price"] = None

            try:
                show_number_element = driver.find_element(
                    By.XPATH,
                    "/html/body/main/div/div/div/section/div[1]/div[2]/div[1]/div/div/div[1]/div/div/button",
                )
                driver.execute_script("arguments[0].click();", show_number_element)
                time.sleep(3)
                phone_number_element = driver.find_element(
                    By.XPATH,
                    "/html/body/main/div/div/div/section/div[1]/div[2]/div[1]/div/div/div[1]/div/ul/li",
                )
                dict_of_page["phone_number"] = phone_number_element.text
            except:
                dict_of_page["phone_number"] = None
            dict_of_data[url] = dict_of_page
            driver.close()

            print(dict_of_page)

            if index % 10 == 0 and index != 0:
                time.sleep(300)

            if len(dict_of_data) == 50:
                break

        with open("auto_data.json", "w+", encoding="utf-8") as outfile:
            json.dump(dict_of_data, outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    olx_data_loader = OlxDataLoader()
    kolesa_data_loader = KolesaDataLoader()
    t1 = Thread(target=olx_data_loader.run)
    t1.start()
    t2 = Thread(target=kolesa_data_loader.run)
    t2.start()
