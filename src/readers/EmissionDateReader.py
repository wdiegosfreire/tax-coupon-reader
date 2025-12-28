from selenium.webdriver.common.by import By

class EmissionDateReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_0").click()
        return driver.find_element(By.ID, "NFe").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "td")[3].find_element(By.TAG_NAME, "span").text[0:19]
