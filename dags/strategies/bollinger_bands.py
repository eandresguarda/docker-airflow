import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import numpy as np
import pandas as pd

#Calcular Metricas (Bandas de Bollinger)
def get_b_bands(data, n):
    """
    Calcular bandas de bollinger

    Parametros
    ----------
    data : pd.Series
        Precio de Cierre.
    n : int
        Nùmero de velas.

    Regresa
    ----------
    df :  pd.DataFrame
        Bandas de Bollinger + Precio de Cierre df.
    """
    MA = pd.Series(pd.Series.rollings(data, n).mean())
    MSD = pd.Series(pd.Series.rolling(data, n).std())
    b1 = MA + (MSD*2)
    B1 = pd.Series(b1, name = 'BB_' + str(n))
    df = pd.concat([data, B1], axis=1)
    b2 = MA - (MSD*2)
    B2 = pd.Series(b2, name = 'Bb_' + str(n))
    df = pd.concat([df,B2], axis =1)
    df.reset_index(inplace=True, drop=True)
    return df

def apply_mean_reverse(data,n):
    """
    Crear estrategia de regresion a la media con base en bandas de bollinger

    Parametros
    ----------
    data : pd.DataFrame
        Datos provenientes del exchange.

    n    : int
        Venta de tiempo de las bandas de bollinger
    
        Regresa
    -----------
    signal  : bool
        Señal de la estrategia para comprar, vender o pasar
    
    data    : pd.DataFrame
        Datos finales de la estrategia
    """

    #Calcular bandas de collinger
    bbands = get_b_bands(data['close'], n)    

    #Crear columnas side (1,-1) y side ref (ref precio)
    bbands['side'] = np.nan
    bbands['side_ref'] = np.nan

    #Crear mascara booleana de posiciones
    long_signals = (bbands['close']) <= bbands[f'Bb_{n}']
    short_signals = (bbands['close']) <= bbands[f'BB_{n}']

    # Asignar valores de side y sider ref
    bbands.loc[long_signals, 'side_ref'] = bbands['close']
    bbands.loc[short_signals, 'side_ref'] = bbands['close']

    bbands.loc[long_signals, 'side'] = 1
    bbands.loc[short_signals, 'side'] = -1

    # Aplicar logica para definir output
    if bbands['side'].iloc[-2] == 1:
        return True, bbands
    
    if bbands['side'].iloc[-2] == -1:
        return False, bbands
    else:
        return None, bbands

if __name__ == "__main__":
    #from api.bybit_data import get_u_timestamp, get_historic_data_bybit
    #data = get_historic_data_bybit('BTCUSD', '5', get_u_timestamp())
    #signal, data_bands = aplly_mean_reverse(data,30)
    print('BOLLINGER BANDS STRATEGY')

