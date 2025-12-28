from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import json

from src.readers.MfeReader import MfeReader
from src.readers.ItemListReader import ItemListReader
from src.readers.TotalReader import TotalReader
from src.readers.CfeKeyReader import CfeKeyReader
from src.readers.QrCodeReader import QrCodeReader
from src.readers.AddressReader import AddressReader
from src.readers.DiscountReader import DiscountReader
from src.readers.SubTotalReader import SubTotalReader
from src.readers.CompanyNameReader import CompanyNameReader
from src.readers.FantasyNameReader import FantasyNameReader
from src.readers.EmissionDateReader import EmissionDateReader
from src.readers.PaymentChangeReader import PaymentChangeReader
from src.readers.StateRegistrationReader import StateRegistrationReader
from src.readers.CostumerTaxIdNumberReader import CostumerTaxIdNumberReader

from src.readers.PaymentListReader import PaymentListReader

mfeReader = MfeReader()
totalReader = TotalReader()
cfeKeyReader = CfeKeyReader()
qrCodeReader = QrCodeReader()
addressReader = AddressReader()
discountReader = DiscountReader()
subTotalReader = SubTotalReader()
companyNameReader = CompanyNameReader()
fantasyNameReader = FantasyNameReader()
emissionDateReader = EmissionDateReader()
paymentChangeReader = PaymentChangeReader()
stateRegistrationReader = StateRegistrationReader()
costumerTaxIdNumberReader = CostumerTaxIdNumberReader()

itemListReader = ItemListReader()
paymentListReader = PaymentListReader()

#------------------------------------------------------------------------------
# Global Methods
#------------------------------------------------------------------------------
def getCustomer():
    return {}

def getTaxIdNumber():
    return qrcode[6:20]

def getExtractNumber():
    return qrcode[31:37]

def getTaxpayerObservation():
    return ""

#todo
def getIncrease():
    return 0

def getBarcode():
    return qrcode

def getLogoURL():
    return ""

def getSatNumber():
    return ""

def getTotalTaxes():
    return ""

def getCouponType():
    return ""

def getSaleCanceled():
    return False

def getCancellationCouponData():
    return {}

def getPaymentMethod():
    return ""

def getPaymentValue():
    return 0

def getObsFiscoList():
    return []

#------------------------------------------------------------------------------
# webdriver configuration
#------------------------------------------------------------------------------

options = Options()
options.add_argument("--start-maximized")
service = Service(executable_path="C:\\Development\\Projects\\other-environment\\driver\\msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)

#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Json Builder
#------------------------------------------------------------------------------

# qrcode = "23250933200056034710651410001085051507317009"
print("\nOla!")
qrcode = input("Informe o QRCODE da NFC-e e pressione Enter:")

driver.get('http://nfce.sefaz.ce.gov.br/pages/consultaNota.jsf')

sleep(1)

accessKey = driver.find_element(By.ID, "acompanhamentoForm:chaveAcesso")
accessCode = driver.find_element(By.ID, "acompanhamentoForm:codigoAcesso")

accessKey.send_keys(qrcode)

print("\nVa ao navegador e preencha o codigo CAPTCHA, mas nao continue pelo navegador.")
input("Em seguida, retorne para este terminal e pressione Enter para continuar.")

print("\nAgora vamos iniciar a captura das informacoes. Por favor, aguarde...")

consultaCompletaBtn = driver.find_element(By.NAME, "acompanhamentoForm:j_idt54")
consultaCompletaBtn.click()

sleep(2)

with open("target/" + datetime.now().strftime("%Y-%m-%d %H%M") + " " + qrcode + ".json", "w", encoding="utf-8") as arquivo:
    json_list = {}

    json_list["cfeKey"] = cfeKeyReader.get(qrcode)
    json_list["mfe"] = mfeReader.get(qrcode)
    json_list["customer"] = getCustomer()
    json_list["taxIdNumber"] = getTaxIdNumber()
    json_list["stateRegistration"] = stateRegistrationReader.get(driver)
    json_list["extractNumber"] = getExtractNumber()
    json_list["costumerTaxIdNumber"] = costumerTaxIdNumberReader.get(driver)
    json_list["costumerTaxIdNumberFormatted"] = costumerTaxIdNumberReader.get(driver)
    json_list["taxpayerObservation"] = getTaxpayerObservation()
    json_list["companyName"] = companyNameReader.get(driver)
    json_list["fantasyName"] = fantasyNameReader.get(driver)
    json_list["address"] = addressReader.get(driver)
    json_list["items"] = itemListReader.get(driver)

    paymentList = paymentListReader.get(driver)

    json_list["payments"] = paymentList
    json_list["subTotal"] = subTotalReader.get(driver)
    json_list["discount"] = discountReader.get(driver)
    json_list["increase"] = getIncrease()
    json_list["emissionDate"] = emissionDateReader.get(driver)
    json_list["barcode"] = getBarcode()
    json_list["qrCode"] = qrCodeReader.get(driver)
    json_list["logoURL"] = getLogoURL()
    json_list["satNumber"] = mfeReader.get(qrcode)["serialNumber"]
    json_list["totalTaxes"] = getTotalTaxes()
    json_list["total"] = totalReader.get(driver)
    json_list["couponType"] = getCouponType()
    json_list["saleCanceled"] = getSaleCanceled()
    json_list["cancellationCouponData"] = getCancellationCouponData()
    json_list["paymentMethod"] = paymentList[-1]["method"]
    json_list["paymentValue"] = paymentList[-1]["value"]
    json_list["paymentChange"] = paymentChangeReader.get(driver)
    json_list["obsFiscoList"] = getObsFiscoList()

    json.dump(json_list, arquivo, indent=4, ensure_ascii=False)

print("\nProcesso de captura finalizado.")
print("O arquivo .json foi gravado na pasta \"target\" dentro deste projeto.")

print("\nAgora vamos iniciar a validacao dos dados do arquivo json. Aguarde mais um pouco...")

sleep(2)
print("Mas isso sao cenas para os proximos capitulos...")