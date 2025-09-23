from selenium.webdriver.common.by import By

class CostumerTaxIdNumberReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_0").click()

        fieldsetList = driver.find_element(By.ID, "NFe").find_elements(By.TAG_NAME, "fieldset")

        fieldsetIndex = -1
        for index, fieldset in enumerate(fieldsetList):
            if fieldset.find_elements(By.TAG_NAME, "legend")[0].text == "Destinatário":
                fieldsetIndex = index
                break
        
        if fieldsetIndex == -1:
            return ""

        return driver.find_element(By.ID, "NFe").find_elements(By.TAG_NAME, "fieldset")[fieldsetIndex].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text.replace(".", "").replace("-", "")
