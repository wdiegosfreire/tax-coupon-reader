from selenium.webdriver.common.by import By

class AddressReader:

    def get(self, driver):
        driver.find_element(By.ID, "tab_1").click()

        return {
            "street": driver.find_element(By.ID, "Emitente").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "tr")[1].find_elements(By.TAG_NAME, "td")[1].find_element(By.TAG_NAME, "span").text,
            "number": "",
            "neighborhood": driver.find_element(By.ID, "Emitente").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "tr")[2].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text,
            "zipCode": driver.find_element(By.ID, "Emitente").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "tr")[2].find_elements(By.TAG_NAME, "td")[1].find_element(By.TAG_NAME, "span").text,
            "city": {
                "name": driver.find_element(By.ID, "Emitente").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "tr")[3].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text
            }
        }