from selenium.webdriver.common.by import By

from src.utils.ConverterUtils import ConverterUtils

converter = ConverterUtils()

class PaymentListReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_6").click()

        paymentList = driver.find_element(By.ID, "Cobranca").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.CSS_SELECTOR, "table.toggle.box")
        paymentDetailList = driver.find_element(By.ID, "Cobranca").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.CSS_SELECTOR, "table.toggable.box")

        itemList = []
        for payment, paymentDetail in zip(paymentList, paymentDetailList):
            driver.execute_script("arguments[0].style.display = 'block';", paymentDetail)

            item = {}
            item["method"] = payment.find_elements(By.TAG_NAME, "td")[1].text.split(" - ")[1]
            item["value"] = converter.toDecimal(paymentDetail.find_elements(By.TAG_NAME, "table")[0].find_elements(By.TAG_NAME, "tr")[1].find_elements(By.TAG_NAME, "td")[0].text)

            itemList.append(item)

        return itemList
