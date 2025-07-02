from selenium.webdriver.common.by import By

from src.utils.ConverterUtils import ConverterUtils

converter = ConverterUtils()

class PaymentChangeReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_6").click()
        table = driver.find_element(By.ID, "Cobranca").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.CSS_SELECTOR, "table.toggable.box")[0]
        driver.execute_script("arguments[0].style.display = 'block';", table)
        return converter.toDecimal(table.find_elements(By.TAG_NAME, "table")[0].find_elements(By.TAG_NAME, "tr")[9].find_elements(By.TAG_NAME, "td")[0].find_elements(By.TAG_NAME, "span")[0].text)
