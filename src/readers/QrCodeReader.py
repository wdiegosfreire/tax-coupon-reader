from selenium.webdriver.common.by import By

class QrCodeReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_7").click()
        return driver.find_element(By.ID, "Inf").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text
