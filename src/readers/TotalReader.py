from selenium.webdriver.common.by import By

from src.utils.ConverterUtils import ConverterUtils

converter = ConverterUtils()

class TotalReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_4").click()
        totalTab = driver.find_element(By.ID, "Totais")

        return {
            "gross": converter.toDecimal(totalTab.find_elements(By.TAG_NAME, "tr")[6].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text),
            "totalDiscountAddition": converter.toDecimal(totalTab.find_elements(By.TAG_NAME, "tr")[6].find_elements(By.TAG_NAME, "td")[3].find_element(By.TAG_NAME, "span").text),
            "subtotalDiscount": 0,
            "subtotalAddition": 0,
            "total": converter.toDecimal(totalTab.find_elements(By.TAG_NAME, "tr")[8].find_elements(By.TAG_NAME, "td")[2].find_element(By.TAG_NAME, "span").text),
        }
