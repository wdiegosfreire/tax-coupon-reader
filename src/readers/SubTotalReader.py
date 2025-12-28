from selenium.webdriver.common.by import By

from src.utils.ConverterUtils import ConverterUtils

converter = ConverterUtils()

class SubTotalReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_4").click()
        totalTab = driver.find_element(By.ID, "Totais")

        return converter.toDecimal(totalTab.find_elements(By.TAG_NAME, "tr")[8].find_elements(By.TAG_NAME, "td")[2].find_element(By.TAG_NAME, "span").text)
        
