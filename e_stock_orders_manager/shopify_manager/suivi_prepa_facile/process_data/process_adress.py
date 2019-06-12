import re

MAX_LENGTH = 36
def adress_treatment(adress_input):
    adress_input = re.sub('\s+', ' ', adress_input).strip()
    if len(adress_input) >= MAX_LENGTH:
        adress_troncated = adress_input[:MAX_LENGTH].strip()
        adress_first_half = ''.join(adress_troncated).strip()
        adress_second_half = adress_input.replace(adress_first_half, '').strip()
        return adress_first_half, adress_second_half
    else:
        return adress_input, ''

def process_adress(df):
    df['N° et libellé de voie'], df['Lieu-dit / BP'] = zip(*df['N° et libellé de voie'].apply(adress_treatment))
    df['Lieu-dit / BP'], df['Bâtiment / Immeuble'] = zip(*df['Lieu-dit / BP'].apply(adress_treatment))
    df['Bâtiment / Immeuble'] = df['Bâtiment / Immeuble'].apply(lambda x: x[:MAX_LENGTH] if len(x) >= MAX_LENGTH + 2 else x)
    return df