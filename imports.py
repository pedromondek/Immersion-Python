import pandas as pd

df_principal = pd.read_excel("tabela-acoes.xlsx", sheet_name="Principal")
df_principal.head(10)

df_total_acoes = pd.read_excel("tabela-acoes.xlsx", sheet_name="Total_de_acoes")
df_total_acoes

df_ticker = pd.read_excel("tabela-acoes.xlsx", sheet_name="Ticker")
df_ticker

df_chatgpt = pd.read_excel("tabela-acoes.xlsx", sheet_name="ChatGPT")
df_chatgpt