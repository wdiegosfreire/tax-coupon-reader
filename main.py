import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, time
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

    with open("companies.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{taxIdNumber};{fileName} (nao padronizado)")

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

BASE_DIR = Path(__file__).resolve().parent

BROWSERS = {
    "1": {
        "name": "Microsoft Edge",
        "driverFile": "msedgedriver.exe",
        "driverUrl": "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/",
    },
    "2": {
        "name": "Mozilla Firefox",
        "driverFile": "geckodriver.exe",
        "driverUrl": "https://github.com/mozilla/geckodriver/releases",
    },
}

def chooseBrowser() -> str:
    print("\nSelecione o navegador que sera utilizado:")
    for key, browser in BROWSERS.items():
        print(f"{key} - {browser['name']}")

    while True:
        option = input("").strip()
        if option in BROWSERS:
            return option
        printRed("Opcao invalida. Informe o numero de um dos navegadores listados:")

def createDriver(option: str):
    # Usa o driver da pasta "driver" quando existir; caso contrario, o Selenium Manager
    # localiza ou baixa automaticamente o driver compativel com o navegador instalado.
    driverPath = BASE_DIR / "driver" / BROWSERS[option]["driverFile"]
    executablePath = str(driverPath) if driverPath.exists() else None

    if option == "1":
        return webdriver.Edge(service=EdgeService(executable_path=executablePath), options=EdgeOptions())

    return webdriver.Firefox(service=FirefoxService(executable_path=executablePath), options=FirefoxOptions())

browserOption = chooseBrowser()
browser = BROWSERS[browserOption]

try:
    driver = createDriver(browserOption)
except Exception as e:
    print("")
    printRed(f"Não foi possivel iniciar o WebDriver do {browser['name']}.")
    print(f"Detalhes: {e}")
    print("Possivelmente o navegador nao esta instalado ou a versao do WebDriver não e compativel com a versão atual do navegador.")
    print(f"Acesse o site {browser['driverUrl']} para baixar a versao correta do WebDriver.")
    print(f"Apos baixar, coloque o arquivo {browser['driverFile']} na pasta driver deste projeto.")
    sys.exit(0)


#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Json Builder
#------------------------------------------------------------------------------

while True:

    # qrcode = "23250933200056034710651410001085051507317009"
    print("\n\n\n\n\n\n\n\n\n\n")
    print("\nOla!")
    print("Informe o QRCODE da NFC-e para iniciar o processamento ou 'exit' para finalizar o programa.")
    print(f"OBS.: O processamento sera feito pelo navegador {browser['name']}.")
    print("Pressione ENTER para continuar...")
    qrcode = input("")

    if qrcode == "exit":
        print("Encerrando o programa...")
        break  # Sai do loop e finaliza o script

    driver.get('http://nfce.sefaz.ce.gov.br/pages/consultaNota.jsf')

    sleep(1)

    accessKey = driver.find_element(By.ID, "acompanhamentoForm:chaveAcesso")
    accessKey.send_keys(qrcode)

    tentativas = 0

    while True:
        try:
            accessCode = driver.find_element(By.ID, "acompanhamentoForm:codigoAcesso")
            accessCode.clear()

            if tentativas == 0:
                print("\nInforme o codigo CAPTCHA:")
            else:
                print("\nCodigo CAPTCHA incorreto. Tente novamente:")

            accessCode.send_keys(input(""))

            consultaCompletaBtn = driver.find_element(By.NAME, "acompanhamentoForm:j_idt54")
            consultaCompletaBtn.click()

            tentativas += 1

            if (tentativas > 4):
                printRed("\nNumero maximo de tentativas de CAPTCHA atingido. Encerrando o programa.")
                sys.exit()

            sleep(2)
        except NoSuchElementException:
            break

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
