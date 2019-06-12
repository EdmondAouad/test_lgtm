import shopify
import datetime
from datetime import date, timedelta, time, datetime
import pandas as pd
from process_data.process_adress import process_adress
import os

SINCE_NUM_DAYS = 2
UNTIL_NUM_DAYS = 0

LAPOSTE_COLUMNS = ['Raison sociale', 'Civilité', 'Nom', 'Prénom', 'Identité / Service / Etage',
 'Bâtiment / Immeuble', 'N° et libellé de voie', 'Lieu-dit / BP', 'Code Postal', 'Ville',
 'Mobile', 'Téléphone', 'Email', 'Référence Destinataire']


API_KEY_ORDER_EXPORT = os.environ.get('API_KEY_ORDER_EXPORT')
API_PASSWORD_ORDER_EXPORT = os.environ.get('API_PASSWORD_ORDER_EXPORT')
SHOP_NAME = 'iriscosmetics'
shop_url = "https://%s.myshopify.com/admin" % (SHOP_NAME)

shopify.ShopifyResource.set_user(API_KEY_ORDER_EXPORT)
shopify.ShopifyResource.set_password(API_PASSWORD_ORDER_EXPORT)
shopify.ShopifyResource.set_site(shop_url)
#The following code prints the amount of orders up in your shopify store in command prompt window
#shop = shopify.Shop.current()
def date_from_today(n):
    date_today = date.today()
    return str(datetime.combine(date_today, time.min) - timedelta(days = n, hours = 2))

def laposte_df(orders):
    laposte_df = pd.DataFrame(columns = LAPOSTE_COLUMNS)
    for order in orders:
        dict_order = order.to_dict()
        shipping_data = dict_order['shipping_address']
        df = pd.DataFrame(columns = LAPOSTE_COLUMNS)
        df['created_at'] = [dict_order['created_at']]
        df['Number'] = [str(dict_order['number'])]
        df['Nom'] = [shipping_data['last_name'].replace('  ', ' ').strip()]
        df['Prénom'] = shipping_data['first_name'].replace('  ', ' ').strip()
        df['N° et libellé de voie'] = shipping_data['address1'].replace('  ', ' ').strip()
        if 'address2' in shipping_data.keys():
            df['N° et libellé de voie'] = df['N° et libellé de voie'] + ' ' + shipping_data['address2']
        df['Code Postal'] = shipping_data['zip']
        df['Ville'] = shipping_data['city'].strip()
        df['Mobile'] = shipping_data['phone']
        df['Email'] = dict_order['email']
        laposte_df = pd.concat([laposte_df, df])
        laposte_df['Number'] = laposte_df['Number'].apply(lambda x: str(1000 + int(x)))
        laposte_df['Mobile'] = laposte_df['Mobile'].apply(lambda x: x.replace(' ', '') if x else x)
        laposte_df = laposte_df.reset_index(drop = True)
        laposte_df.index = [i+1 for i in range(len(laposte_df))]
        laposte_df = process_adress(laposte_df)
    return laposte_df

subdir = 'prepafacile_csv/from_api'
yesterday = str(date.today() - timedelta(1))

orders = shopify.Order.find(created_at_min = date_from_today(SINCE_NUM_DAYS),
                           created_at_max = date_from_today(UNTIL_NUM_DAYS))
print(len(orders))

if not os.path.exists(subdir):
    os.mkdir(subdir)
df_orders = laposte_df(orders)
print(df_orders[['Number', 'created_at']])
df_orders = df_orders.drop(['created_at', 'Number'], axis = 1)
df_orders.to_csv(subdir + '/' + yesterday +'.csv', sep = ';')
