from selenium.webdriver.common.by import By

from src.utils.ConverterUtils import ConverterUtils

converter = ConverterUtils()

class ItemReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_3").click()

        productList = driver.find_element(By.ID, "Prod").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "div")[0].find_elements(By.CSS_SELECTOR, "table.toggle.box")
        productDetailList = driver.find_element(By.ID, "Prod").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "div")[0].find_elements(By.CSS_SELECTOR, "table.toggable.box")

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
            item["price"] = converter.toDecimal(PRODUCT_DETAIL_TD0_TABLE1.find_elements(By.TAG_NAME, "tr")[3].find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "span")[0].text)
            item["un"] = product.find_elements(By.TAG_NAME, "td")[3].text
            item["valueOfTaxes"] = converter.toDecimal(PRODUCT_DETAIL_TD0_TABLE1.find_elements(By.TAG_NAME, "tr")[4].find_elements(By.TAG_NAME, "td")[2].find_elements(By.TAG_NAME, "span")[0].text)
            item["register"] = {
                "addition": 0,
                "additionApportionment": 0,
                "discount": converter.toDecimal(PRODUCT_DETAIL_TD0_TABLE0.find_elements(By.TAG_NAME, "tr")[3].find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "span")[0].text),
                "discountApportionment": 0
            }

            itemList.append(item)

        return itemList
