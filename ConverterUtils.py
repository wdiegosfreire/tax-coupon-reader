class ConverterUtils:

    def toInt(self, stringValue):
        try:
            return int(stringValue)
        except ValueError:
            return 0

    def toDecimal(self, stringValue):
        try:
            stringValue = stringValue.replace(".", "").replace(",", ".")
            return float(stringValue)
        except ValueError:
            return 0