from selenium.webdriver.common.by import By

class FantasyNameReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_1").click()
        return driver.find_element(By.ID, "Emitente").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "tr")[0].find_elements(By.TAG_NAME, "td")[1].find_element(By.TAG_NAME, "span").text
