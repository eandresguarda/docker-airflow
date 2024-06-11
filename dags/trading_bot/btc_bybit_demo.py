import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

def run_bollinger_strategy():
    from settings.config import BYBIT_API_KEY, BYBIT_API_SECRET,ORDER_SIZE_DEFAULT
    #from api.bybit_data import get_u_timestamp, get_historic_data_bybit
    from api.bybit_orders import set_buy_order, set_sell_order
    from strategies.bollinger_bands import aplly_mean_reverse

    #Cargar Datos
    data = []
    #data = get_historic_data_bybit('BTCUSD', '5', get_u_timestamp())

    #Ejecutar estrategia
    signal, data_bands = aplly_mean_reverse(data,30)

    print("--------------------- DATA FINAL --------------------------")
    print(data_bands.tail())

    #colocal ordenes
    if signal == True:
        #set_buy_order(BYBIT_API_KEY, BYBIT_API_SECRET, ORDER_SIZE_DEFAULT)
        print("--------------------- ORDEN LARGA ---------------------")
    
    if signal == False:
        #set_sell_order(BYBIT_API_KEY, BYBIT_API_SECRET, ORDER_SIZE_DEFAULT)
        print("--------------------- ORDEN CORTA ---------------------")
    
    if signal is None:
        raise("SIN ORDEN EJECUTADA")