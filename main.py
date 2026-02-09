import sys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from pathlib import Path

import json

from src.readers.MfeReader import MfeReader
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

from src.readers.ItemListReader import ItemListReader
from src.readers.PaymentListReader import PaymentListReader

from src.validators.DataValidator import DataValidator

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

dataValidator = DataValidator()

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

def printRed(text):
    print(f"\033[31m{text}\033[0m")

def printGreen(text):
    print(f"\033[32m{text}\033[0m")

def getStandarizedCompanyName(fileName: str, taxIdNumber: str) -> str:
    mapa = readCompanies()

    for chave, retorno in mapa.items():
        if chave in taxIdNumber:
            printGreen(f"\nA empresa '{fileName}' foi padronizada para '{retorno}'.")
            return retorno

    printRed(f"\nA empresa '{fileName}' nao possui padronizacao definida. Utilizando o nome original.")
    return fileName

def readCompanies() -> dict:
    mapa = {}

    with open("companies.txt", "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or ";" not in linha:
                continue

            chave, valor = linha.split(";", 1)
            mapa[chave.strip()] = valor.strip()

    return mapa


#------------------------------------------------------------------------------
# webdriver configuration
#------------------------------------------------------------------------------

options = Options()
options.add_argument("--start-maximized")

BASE_DIR = Path(__file__).resolve().parent
driver_path = BASE_DIR / "driver" / "msedgedriver.exe"
service = Service(executable_path=str(driver_path))

try:
    driver = webdriver.Edge(service=service, options=options)
except Exception as e:
    print("")
    print("Não foi possivel iniciar o WebDriver do Microsoft Edge.")
    print("Possivelmente a versao instalada do WebDriver não e compativel com a versão atual do navegador.")
    print("Acesse o site https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ para baixar a versao correta do WebDriver.")
    print("Apos baixar, substitua o arquivo msedgedriver.exe na pasta driver deste projeto.")
    sys.exit(0)


#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Json Builder
#------------------------------------------------------------------------------

while True:

    # qrcode = "23250933200056034710651410001085051507317009"
    print("\nOla!")
    print("Informe o QRCODE da NFC-e para iniciar o processamento ou 'exit' para finalizar o programa.")
    print("OBS.: Para que o processamento ocorra com sucesso, utilize o Microsoft Edge.")
    print("Pressione ENTER para continuar...")
    qrcode = input("")

    if qrcode == "exit":
        print("Encerrando o programa...")
        break  # Sai do loop e finaliza o script

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

    fileName = fantasyNameReader.get(driver)

    if not fileName or not fileName.strip():
        fileName = companyNameReader.get(driver)

    if not fileName or not fileName.strip():
        fileName = qrcode

    if not fileName or not fileName.strip():
        fileName = "Undefined Name"

    fileName = getStandarizedCompanyName(fileName, getTaxIdNumber())

    fileDate = datetime.strptime(emissionDateReader.get(driver), "%d/%m/%Y %H:%M:%S")
    fileDate = fileDate.strftime("%Y-%m-%d %H%M")

    with open("target/" + fileDate + " " + fileName + ".json", "w", encoding="utf-8") as arquivo:
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

    print("\nAgora vamos iniciar a validacao dos dados do arquivo json. Aguarde mais um pouco..." + "\n")

    printGreen("Validacao ROUND_UP iniciada!" + "\n")
    sleep(3)

    isValid = dataValidator.execute(json_list, "roundUp")

    if isValid:
        printGreen("Validacao ROUND_UP finalizada com SUCESSO!")
    else:
        printRed("Validacao ROUND_UP finalizada com erro!" + "\n")

        sleep(1)
        printGreen("Validacao TRUNCATE iniciada!")
        sleep(3)

        isValid = dataValidator.execute(json_list, "trunc")

        if isValid:
            printGreen("Validacao TRUNCATE finalizada com SUCESSO!")
        else:
            printRed("Validacao TRUNCATE finalizada com erro!")

    sleep(2)
