from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from selenium.webdriver.common.by import By

class DataValidator:

    def execute(self, jsonList, roundMethod):
        totalItens = Decimal(str(0.0))

        for item in jsonList["items"]:
            if (roundMethod == "roundUp"):
                totalItens = totalItens + self.roundUp(item["amount"], item["price"], item["register"]["discount"])
            elif (roundMethod == "trunc"):
                totalItens = totalItens + self.truncate(item["amount"], item["price"], item["register"]["discount"])

        totalItens = round(totalItens, 2)

        totalBruto = jsonList["total"]["gross"]
        totalPago = jsonList["total"]["total"]

        print("-------------------------------------")

        print("Quantidade de itens: " + str(len(jsonList["items"])))
        print("Valor total bruto: " + str(totalBruto))
        print("Valor pago com desconto ou acrescimo: " + str(totalPago))
        print("Valor total calculado a partir dos itens: " + str(totalItens))

        print("-------------------------------------" + "\n")

        if str(totalItens) == str(totalPago):
            return True

        return False

    def roundUp(self, amount, price, discount):
        amount = Decimal(str(amount))
        price = Decimal(str(price))
        discount = Decimal(str(discount))

        total = (amount * price) - discount
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def truncate(self, amount, price, discount):
        amount = Decimal(str(amount))
        price = Decimal(str(price))
        discount = Decimal(str(discount))

        total = (amount * price) - discount
        return total.quantize(Decimal("0.00"), rounding=ROUND_DOWN)
