import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import db
import elastic


def get_contract(identifier, api_key): # TODO api key sem musí jít jako parametr
    # Funkce vrací fulltext smlouvy poskytovaný zpracovaný Hlídačem státu
    identifier = str(identifier)
    headers = {'Authorization': 'Token ' + api_key}  # TODO API key předávat jako arg nebo env proměnnou dockerem
    url_text = 'https://www.hlidacstatu.cz/Api/v2/smlouvy/text/' + identifier
    url_metadata = 'https://www.hlidacstatu.cz/Api/v2/smlouvy/' + identifier
    contract = {
        "metadata": requests.get(url_metadata, headers=headers).text,
        "text": requests.get(url_text, headers=headers).text
    }
    return contract


def get_contract_and_party_identifiers(date):
    # Funkce vrací pole identifikátorů smluv
    url = 'https://data.smlouvy.gov.cz/dump_' + date + '.xml'
    response = requests.get(url)
    if response.status_code == 200:
        xml_dump = response.text
        tree = ET.ElementTree(ET.fromstring(xml_dump))
        root = tree.getroot()
        ET.register_namespace("", "http://portal.gov.cz/rejstriky/ISRS/1.2/")
        ns = {"": "http://portal.gov.cz/rejstriky/ISRS/1.2/"}
        contract_and_party_identifiers = []
        for elm in root.findall('.//zaznam', ns):
            id_verze = elm.find('.//idVerze', ns).text  # verze smlouvy (identifikátor)
            contracting_parties = []
            for contract_party in elm.findall('.//smluvniStrana', ns):  # hledání iča dodavatelů
                ico = contract_party.find('.//ico', ns)
                if ico is not None and ico.text.isnumeric():
                    contracting_parties.append(ico.text)
            contract_and_party_identifiers.append([id_verze, contracting_parties])
        return contract_and_party_identifiers
    elif response.status_code == 404:
        print("Pro zadané období " + date + " neexistují žádná data")
        return None
    else:
        print("Vyskytl se problém při dotazování dat. Status code " + response.status_code)
        return None


def load_contracts(date, api_key):
    # Funkce načítá fulltexty všech smluv dle zadaného období
    identifiers = get_contract_and_party_identifiers(date)
    if identifiers:
        for identifier in tqdm(identifiers):
            # identifier[0] obsahuje identifikátor smlouvy
            # identifier[1] obsahuje pole IČA dodavatelů
            for ICO in identifier[1]:
                if db.find_ict_supplier(ICO):
                    contract_dict = get_contract(identifier[0], api_key)
                    elastic.insert_into_elastic(identifier[0], contract_dict["metadata"], contract_dict["text"])
                    break



