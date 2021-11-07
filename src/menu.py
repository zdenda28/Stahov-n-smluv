import requests
import contract


def create_menu():
    print_options()
    get_period_option()


def print_options():
    print("Vyberte období, pro které chcete zpracovat data:")
    print("[0] Zpracování měsíčních dat")
    print("[1] Zpracování denních dat")
    print("[2] Ukončit aplikaci")


def get_period_option():
    period = input("Období: ")
    if period == "2":
        exit()
    elif period == "1":
        get_daily_data_input()
    elif period == "0":
        get_monthly_data_input()
    else:
        print("\nNeplatná hodnota")
        get_period_option()


def get_daily_data_input():
    print("\nZadejte datum ve formátu YYYY_MM_DD")
    date = input("Datum: ")
    contract.load_contracts(date, get_api_key())


def get_monthly_data_input():
    print("\n\nZadejte datum ve formátu YYYY_MM")
    date = input("Datum: ")
    contract.load_contracts(date, get_api_key())


def get_api_key():
    print("\nZadejte váš API klíč přidělený hlídačem státu")
    api_key = input("API klíč: ")
    headers = {'Authorization': 'Token ' + api_key}
    url = 'https://www.hlidacstatu.cz/api/v2/ping/ping'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return api_key
    else:
        print("\nNeplatný API klíč")
        get_api_key()
