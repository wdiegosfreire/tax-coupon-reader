from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import json

from src.readers.ItemReader import ItemReader
from src.readers.TotalReader import TotalReader
from src.readers.AddressReader import AddressReader
from src.readers.FantasyNameReader import FantasyNameReader
from src.readers.PaymentChangeReader import PaymentChangeReader
from src.readers.StateRegistrationReader import StateRegistrationReader
from src.readers.CostumerTaxIdNumberReader import CostumerTaxIdNumberReader

itemReader = ItemReader()
totalReader = TotalReader()
addressReader = AddressReader()
fantasyNameReader = FantasyNameReader()
paymentChangeReader = PaymentChangeReader()
stateRegistrationReader = StateRegistrationReader()
costumerTaxIdNumberReader = CostumerTaxIdNumberReader()

#------------------------------------------------------------------------------
# Global Methods
#------------------------------------------------------------------------------
def getCfeKey():
    return qrcode

def getMfe():
    return {"serialNumber": qrcode[22:31]}

def getCustomer():
    return {}

def getTaxIdNumber():
    return qrcode[6:20]

def getExtractNumber():
    return qrcode[31:37]

def getCostumerTaxIdNumberFormatted():
    driver.find_element(By.ID, "tab_0").click()
    return driver.find_element(By.ID, "NFe").find_elements(By.TAG_NAME, "fieldset")[2].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text

def getTaxpayerObservation():
    return ""

def getCompanyName():
    driver.find_element(By.ID, "tab_0").click()
    return driver.find_element(By.ID, "NFe").find_elements(By.TAG_NAME, "fieldset")[1].find_elements(By.TAG_NAME, "td")[1].find_element(By.TAG_NAME, "span").text

#todo
def getPayments():
    return []

#todo
def getSubTotal():
    return 0

#todo
def getDiscount():
    return 0

#todo
def getIncrease():
    return 0

def getEmissionDate():
    driver.find_element(By.ID, "tab_0").click()
    return driver.find_element(By.ID, "NFe").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "td")[3].find_element(By.TAG_NAME, "span").text[0:19]

def getBarcode():
    return qrcode

def getQrCode():
    driver.find_element(By.ID, "tab_7").click()
    return driver.find_element(By.ID, "Inf").find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "fieldset")[0].find_elements(By.TAG_NAME, "td")[0].find_element(By.TAG_NAME, "span").text

def getLogoURL():
    return ""

def getSatNumber():
    return ""

def getTotalTaxes():
    return ""

def getCouponType():
    return ""

def getSaleCanceled():
    return ""

def getCancellationCouponData():
    return {}

def getPaymentMethod():
    return ""

def getPaymentValue():
    return 0

def getObsFiscoList():
    return []

#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------
qrcode = "23240606057223038063650230000001531023004649"


#------------------------------------------------------------------------------
# Json Builder
#------------------------------------------------------------------------------
now = datetime.now()

driver = webdriver.Edge()
driver.get('http://nfce.sefaz.ce.gov.br/pages/consultaNota.jsf')

sleep(1)

accessKey = driver.find_element(By.ID, "acompanhamentoForm:chaveAcesso")
accessCode = driver.find_element(By.ID, "acompanhamentoForm:codigoAcesso")

accessKey.send_keys(qrcode)

print("Vá ao navegador e preencha o código CAPTCHA.")
input("Em seguida, retorne para este terminal e pressione Enter para continuar.")

consultaCompletaBtn = driver.find_element(By.NAME, "acompanhamentoForm:j_idt54")
consultaCompletaBtn.click()

sleep(2)

with open("target/" + now.strftime("%Y-%m-%d %H%M") + " " + qrcode + ".json", "w", encoding="utf-8") as arquivo:
    json_list = {}

    json_list["cfeKey"] = getCfeKey()
    json_list["mfe"] = getMfe()
    json_list["customer"] = getCustomer()
    json_list["taxIdNumber"] = getTaxIdNumber()
    json_list["stateRegistration"] = stateRegistrationReader.get(driver)
    json_list["extractNumber"] = getExtractNumber()
    json_list["costumerTaxIdNumber"] = costumerTaxIdNumberReader.get(driver)
    json_list["costumerTaxIdNumberFormatted"] = getCostumerTaxIdNumberFormatted()
    json_list["taxpayerObservation"] = getTaxpayerObservation()
    json_list["companyName"] = getCompanyName()
    json_list["fantasyName"] = fantasyNameReader.get(driver)
    json_list["address"] = addressReader.get(driver)
    json_list["items"] = itemReader.get(driver)
    json_list["payments"] = getPayments()
    json_list["subTotal"] = getSubTotal()
    json_list["discount"] = getDiscount()
    json_list["increase"] = getIncrease()
    json_list["emissionDate"] = getEmissionDate()
    json_list["barcode"] = getBarcode()
    json_list["qrCode"] = getQrCode()
    json_list["logoURL"] = getLogoURL()
    json_list["satNumber"] = getSatNumber()
    json_list["totalTaxes"] = getTotalTaxes()
    json_list["total"] = totalReader.get(driver)
    json_list["couponType"] = getCouponType()
    json_list["saleCanceled"] = getSaleCanceled()
    json_list["cancellationCouponData"] = getCancellationCouponData()
    json_list["paymentMethod"] = getPaymentMethod()
    json_list["paymentValue"] = getPaymentValue()
    json_list["paymentChange"] = paymentChangeReader.get(driver)
    json_list["obsFiscoList"] = getObsFiscoList()

    json.dump(json_list, arquivo, indent=4, ensure_ascii=False)
