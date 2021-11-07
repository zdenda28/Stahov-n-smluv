import requests
import xml.etree.ElementTree as ET
import db


def get_ares_response(ico):
    # Vrací XML string s údaji z Registru ekonomických subjektů pro daný subjekt
    url = "https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_res.cgi?ico=" + ico
    response = requests.get(url)
    return response.text


def get_nace_list(ico):
    # Vrací seznam ekonomických činností (čísla NACE) pro daný subjekt
    tree = ET.ElementTree(ET.fromstring(get_ares_response(ico)))
    root = tree.getroot()
    nace_list = []
    for elm in root.findall('.//{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.3}NACE'):
        if elm.text.isnumeric():
            nace_list.append(int(elm.text))
    return nace_list


def is_subject_ict(ico):
    # ICT NACE kódy:
    allowed_nace_codes = [261, 2611, 26110,  # Výroba elektronických součástek a desek
                          2612, 26120, 262, 2620, 26200,  # Výroba počítačů a periferních zařízení
                          263, 2630, 26300,  # Výroba komunikačních zařízení; skupina
                          264, 2640, 26400,  # Výroba spotřební elektroniky
                          268, 2680, 26800,  # Výroba magnetických a optických médií.
                          465, 4651, 46510, 4652, 46520,  # Velkoobchod s počítačovým a komunikačním zařízením.
                          611, 6110, 61101, 61102, 61103, 61104, 61109,  # Činnosti související s pevnou telekomunikační sítí
                          612, 6120, 61201, 61202, 61203, 61204, 61209,  # Činnosti související s bezdrátovou telekomunikační sítí
                          613, 6130, 61300,  # Činnosti související se satelitní telekomunikační sítí
                          619, 6190, 61900,  # Ostatní telekomunikační činnosti
                          582, 5821, 58210, 5829, 58290,  # Vydávání softwaru
                          620, 6201, 62010,  # Programování
                          6202, 62020,  # Poradenství v oblasti informačních technologií
                          6203, 62030,  # Správa počítačového vybavení
                          6209, 62090,  # Ostatní činnosti v oblasti informačních technologií
                          631, 6311, 63110, 6312, 63120,  # Činnosti související se zpracováním dat a hostingem
                          951, 9511, 95110, 9512, 95120]  # Opravy počítačů a komunikačních zařízení
    subject_nace_codes = get_nace_list(ico)
    # ošetření dělení nulou
    if len(subject_nace_codes) > 0:
        ict_nace_ratio = len([x for x in allowed_nace_codes if x in subject_nace_codes]) / len(subject_nace_codes)
    else:
        ict_nace_ratio = 0
    # Jako ICT dodavatel je označen pouze ten, který má více či rovno 0,2 činností z oblasti ICT
    if ict_nace_ratio >= 0.2:
        ict_supplier = True
    else:
        ict_supplier = False

    db.insert_supplier(ico, ', '.join(map(str, subject_nace_codes)), ict_supplier)

    return ict_supplier
