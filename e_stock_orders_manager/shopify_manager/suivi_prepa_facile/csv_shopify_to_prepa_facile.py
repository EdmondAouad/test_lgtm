import pandas as pd
import sys
from datetime import date, timedelta
import os
import re
from process_data.process_adress import process_adress
droppedFile = sys.argv[1]

LAPOSTE_COLUMNS = ['Raison sociale', 'Civilité', 'Nom', 'Prénom', 'Identité / Service / Etage',
 'Bâtiment / Immeuble', 'N° et libellé de voie', 'Lieu-dit / BP', 'Code Postal', 'Ville',
 'Mobile', 'Téléphone', 'Email', 'Référence Destinataire']


def laposte_df(path):
    shipping_data = pd.read_csv(path)
    df = pd.DataFrame(columns = LAPOSTE_COLUMNS)
    df['Nom'] = shipping_data['Billing Name'].apply(lambda x: ' '.join(x.split(' ')[1:])).apply(lambda x : x.replace('  ', ' ').strip())
    df['Prénom'] = shipping_data['Billing Name'].apply(lambda x: x.split(' ')[0]).apply(lambda x: x.replace('  ', ' ').strip())
    df['N° et libellé de voie'] = shipping_data['Shipping Address1'].apply(lambda x: x.replace('  ', ' ').strip())
    df = process_adress(df)
    df['Code Postal'] = shipping_data['Shipping Zip'].apply(lambda x: str(x))
    df['Ville'] = shipping_data['Shipping City'].apply(lambda x: x.strip())
    df['Mobile'] = shipping_data['Shipping Phone'].apply(lambda x: str(x).replace(' ', '').replace('nan', '') if x else x)
    df['Email'] = shipping_data['Email']
    
    df = df.reset_index(drop = True)
    df.index = [i+1 for i in range(len(df))]
    return df

subdir = 'prepafacile_csv/from_shopify_csv'
today = str(date.today())
if not os.path.exists(subdir):
    os.mkdir(subdir)
laposte_df(droppedFile).to_csv(subdir + '/' + today +'.csv', sep = ';')
