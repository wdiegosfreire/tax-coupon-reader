class MfeReader:

    def get(self, qrcode):
        return {"serialNumber": qrcode[22:31]}
