from selenium.webdriver.common.by import By

class DataValidator:

    def execute(self, jsonList):
        print("-------------------------------------")
        print("Quantidade de itens: " + str(len(jsonList["items"])))
        print("Valor total bruto: " + str(jsonList["total"]["gross"]))
        print("Valor total com desconto: " + str(jsonList["total"]["total"]))
        print("-------------------------------------")