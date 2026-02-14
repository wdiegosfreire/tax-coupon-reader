import unicodedata

from selenium.webdriver.common.by import By
from src.utils.ConverterUtils import ConverterUtils

converter = ConverterUtils()

class ItemListReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_3").click()

        productList = driver.find_element(By.ID, "Prod").find_element(By.TAG_NAME, "fieldset").find_element(By.TAG_NAME, "div").find_elements(By.CSS_SELECTOR, "table.toggle.box")
        productDetailList = driver.find_element(By.ID, "Prod").find_element(By.TAG_NAME, "fieldset").find_element(By.TAG_NAME, "div").find_elements(By.CSS_SELECTOR, "table.toggable.box")

        itemList = []
        for product, productDetail in zip(productList, productDetailList):
            driver.execute_script("arguments[0].style.display = 'block';", productDetail)

            PRODUCT_DETAIL_TD0_TABLE0 = productDetail.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "table")[0]
            PRODUCT_DETAIL_TD0_TABLE1 = productDetail.find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "table")[1]

            item = {}
            item["item"] = converter.toInt(product.find_elements(By.TAG_NAME, "td")[0].text)
            item["code"] = PRODUCT_DETAIL_TD0_TABLE0.find_elements(By.TAG_NAME, "tr")[0].find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "span")[0].text
            item["codeTrafic"] = PRODUCT_DETAIL_TD0_TABLE0.find_elements(By.TAG_NAME, "tr")[0].find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "span")[0].text
            item["description"] = product.find_elements(By.TAG_NAME, "td")[1].text
            item["amount"] = converter.toDecimal(product.find_elements(By.TAG_NAME, "td")[2].text)
            item["price"] = converter.toDecimal(self.getValueWithLabel(PRODUCT_DETAIL_TD0_TABLE1, "Valor Unitário de Comercialização"))
            item["un"] = product.find_elements(By.TAG_NAME, "td")[3].text
            item["valueOfTaxes"] = converter.toDecimal(self.getValueWithLabel(PRODUCT_DETAIL_TD0_TABLE1, "Valor Aproximado dos Tributos"))
            item["register"] = {
                "addition": converter.toDecimal(PRODUCT_DETAIL_TD0_TABLE0.find_elements(By.TAG_NAME, "tr")[2].find_elements(By.TAG_NAME, "td")[2].find_elements(By.TAG_NAME, "span")[0].text),
                "additionApportionment": 0,
                "discount": converter.toDecimal(PRODUCT_DETAIL_TD0_TABLE0.find_elements(By.TAG_NAME, "tr")[3].find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "span")[0].text),
                "discountApportionment": 0
            }

            itemList.append(item)

        return itemList

    def getValueWithLabel(self, table, key):
        key_norm = self.normalize(key)

        cellList = table.find_elements(By.XPATH, ".//td")

        for cell in cellList:
            try:
                label = cell.find_element(By.TAG_NAME, "label").text.strip()
                label_norm = self.normalize(label)

                if label_norm == key_norm:
                    span = cell.find_element(By.TAG_NAME, "span")
                    return span.text.strip()

            except:
                continue

        return 0

    def normalize(self, text):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        ).lower().strip()

