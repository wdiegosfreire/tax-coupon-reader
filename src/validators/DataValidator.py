from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from selenium.webdriver.common.by import By

class DataValidator:

    def execute(self, jsonList, roundMethod):
        totalItens = Decimal(str(0.0))

        for item in jsonList["items"]:
            if (roundMethod == "roundUp"):
                totalItens = totalItens + self.roundUp(item["amount"], item["price"], item["register"]["discount"], item["register"]["addition"])
            elif (roundMethod == "trunc"):
                totalItens = totalItens + self.truncate(item["amount"], item["price"], item["register"]["discount"], item["register"]["addition"])

        totalItens = round(totalItens, 2)

        totalBruto = self.toStandards(jsonList["total"]["gross"])
        totalPago = self.toStandards(jsonList["total"]["total"])
        totalAddition = self.toStandards(jsonList["total"]["subtotalAddition"])
        totalDiscount = self.toStandards(jsonList["total"]["subtotalDiscount"])

        print("-------------------------------------")

        print("Items Amount: " + str(len(jsonList["items"])))
        print("Total Gross: " + str(totalBruto))
        print("Total Additions: " + str(totalAddition))
        print("Total Discounts: " + str(totalDiscount))
        print("Total pago com descontos/acrescimos: " + str(totalPago))
        print("Total calculado a partir dos itens com descontos/acrescimos: " + str(totalItens))

        print("-------------------------------------" + "\n")

        if totalItens == totalPago:
            return True

        return False

    def roundUp(self, amount, price, discount, addition):
        amount = Decimal(str(amount))
        price = Decimal(str(price))
        discount = Decimal(str(discount))
        addition = Decimal(str(addition))

        total = (amount * price) - discount + addition
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def truncate(self, amount, price, discount, addition):
        amount = Decimal(str(amount))
        price = Decimal(str(price))
        discount = Decimal(str(discount))
        addition = Decimal(str(addition))

        total = (amount * price) - discount + addition
        return total.quantize(Decimal("0.00"), rounding=ROUND_DOWN)

    def toStandards(self, value):
        decimalValue = Decimal(str(value))
        return decimalValue.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
