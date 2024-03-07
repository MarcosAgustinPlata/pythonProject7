import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm

# Cargar los datos macroeconómicos
data_cpi = pd.read_csv('/mnt/data/FRACPIALLMINMEI (3).csv')
data_interest_rate = pd.read_csv('/mnt/data/FRASARTMISMEI.csv')
data_unemployment = pd.read_csv('/mnt/data/LRHUTTTTFRM156S (2).csv')

# Preparar los datos macroeconómicos
data_cpi['DATE'] = pd.to_datetime(data_cpi['DATE'])
data_interest_rate['DATE'] = pd.to_datetime(data_interest_rate['DATE'])
data_unemployment['DATE'] = pd.to_datetime(data_unemployment['DATE'])

# Filtrar los datos para el rango 2010-2023
data_cpi_filtered = data_cpi[(data_cpi['DATE'] >= '2010-01-01') & (data_cpi['DATE'] <= '2023-12-31')]
data_interest_rate_filtered = data_interest_rate[(data_interest_rate['DATE'] >= '2010-01-01') & (data_interest_rate['DATE'] <= '2023-12-31')]
data_unemployment_filtered = data_unemployment[(data_unemployment['DATE'] >= '2010-01-01') & (data_unemployment['DATE'] <= '2023-12-31')]

# Unir los tres DataFrames en uno solo basado en la columna 'DATE'
data_macro = pd.merge(data_cpi_filtered, data_interest_rate_filtered, on='DATE', how='outer')
data_macro = pd.merge(data_macro, data_unemployment_filtered, on='DATE', how='outer')

# Descargar los datos del índice CAC 40
cac40 = yf.download('^FCHI', start='2010-01-01', end='2023-12-31')

# Preparar los datos del CAC 40
cac40['Date'] = cac40.index
cac40['YearMonth'] = cac40['Date'].dt.to_period('M')

# Calcular los retornos mensuales del CAC 40
cac40['Monthly Returns'] = cac40['Adj Close'].pct_change()

# Preparar data_macro para fusionar
data_macro['YearMonth'] = data_macro['DATE'].dt.to_period('M')

# Fusionar los datos del CAC 40 con los datos macroeconómicos
merged_data = pd.merge(cac40, data_macro, left_on='YearMonth', right_on='YearMonth', how='inner')

# Seleccionar las columnas necesarias para la regresión
regression_data = merged_data[['Monthly Returns', 'FRACPIALLMINMEI', 'FRASARTMISMEI', 'LRHUTTTTFRM156S']].dropna()

# Preparar las variables para la regresión
X = regression_data[['FRACPIALLMINMEI', 'FRASARTMISMEI', 'LRHUTTTTFRM156S']]  # Variables independientes
y = regression_data['Monthly Returns']  # Variable dependiente
X = sm.add_constant(X)  # Agregar constante al modelo

# Realizar la regresión lineal
model = sm.OLS(y, X).fit()

# Mostrar el resumen del modelo
model_summary = model.summary()
model_summary