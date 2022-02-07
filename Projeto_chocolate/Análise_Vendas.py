#!/usr/bin/env python
# coding: utf-8

# # Análise de Mercado de vendas de Chocolate

# In[1]:


# Importação dos pacotes:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go 
import seaborn as sns


# In[2]:


# Formatação Geral do relatório:
sns.set()
# Formatar o número de casas decimais:
pd.set_option('float_format', '{:.2f}'.format)


# In[3]:


### Importação dos Dados
df_base = pd.read_excel(r'C:\Users\Nzuzi Armindo\Documents\Programacao_DC\Jupter_notebook\Marketing_Analytics\Projeto_chocolate\Chocolate.xlsx')


# In[5]:


##informações do df:
display(df_base)


# ## Resumo:
#  - Total de vandas
#  - Vendas por Marcas
#  - Média de vendas por Semana
#  - Variação de Vendas por Semana

# In[6]:


# Colunas da tabela
df_base.columns


# In[7]:


# Transformar todas as Colunas em menúsculas:
df_base.columns = df_base.columns.str.lower()


# In[8]:


# Modificar o indice
df_base.set_index('semana',inplace=True)


# In[9]:


### Adicionar a coluna mercado que é a soma de todas as vendas:
df_base['mercado'] = 0
for i in df_base.columns:
    if i.startswith('vendas'):
        df_base['mercado'] += df_base[i]
        


# In[10]:


df_base.head(5)


# 
# ## Total de Mercado

# In[11]:


mercado = df_base['mercado'].sum()
print(f'Total de mercado de Chocolate foi de: R${mercado}')


# In[12]:


## Análise de mercado ao longo do tempo:
group = df_base.groupby('semana', as_index=False)
data =group['mercado'].sum()
fig = figsize=(9,6)
fig = px.line(data, y='mercado',
              labels={'index':'Semana', 'mercado': 'Mercado'},
              template='simple_white'
             )
fig.update_layout(
                title={
                'text': 'Total de Mercado',
                'y': 0.95,
                'x': 0.5}
                )
fig.show()


# In[14]:


# análise estatistica do mercado:
data.describe()


# In[17]:


# Histrograma de total de mercado:
df= data
fig = figsize=(9,6)
fig = px.histogram(df, 
                   marginal='violin',
                   template='simple_white',
                   labels={'value':'Mercado'}
                  )
fig.update_layout(title={'text':'Histograma do Mercado', 'y':0.95, 'x':0.5})
fig.show()


# In[18]:


## Boxplot do total de mercado:
fig= figsize=(10,6)
fig = px.box(data, x='mercado',
             labels={'value':'Vendas','variable': ''},points='all',template='simple_white')
fig.update_layout(title={
    'text': 'Boxplot de Mercado',
    'y': 0.95,
    'x': 0.5
})
fig.show()


#  ## Variação de Mercado
#  
#  verificando a variação do mercado ao longo do tempo:

# In[73]:


df_variacao_mercado = data.pct_change()

df_variacao_mercado


# In[74]:


# Taxa de Crescimento - calculando a média variação total:
taxa_crecimento = df_variacao_mercado['mercado'].mean()
print(f'A taxa de crescimento médio do mercado é de {"%.2f"%taxa_crecimento}%')


# In[75]:


# Média da taxa de crescimento movel do mercado das ultimas 4 semanas: 
df_variacao_mercado['mercado_movel']= df_variacao_mercado['mercado'].rolling(4).mean() 


# In[76]:


# Variação de Mercado de Chocolates
df_variacao_mercado['taxa_média_crecimento'] = taxa_crecimento


# In[77]:


df_variacao_mercado


# In[78]:


# Variação de Mercado:
variacao = df_variacao_mercado['mercado']
fig = figsize=(9, 6)
fig = px.line(variacao, y='mercado',
              labels={'index': 'Semana', 'mercado': 'Variação de Mercado'},
              template='simple_white'
             )
fig.update_layout(title={'text':'Variação Semanal do Mercado', 'y':0.95, 'x':0.5})
             
fig.show()


# In[79]:


# Variação de Mercado dos ultimos 4 semanas:
variacao = df_variacao_mercado[['mercado','mercado_movel']]
variacao.columns=['Variação de Mercado', 'Variaçao Movel 4 semanas']
fig = figsize=(9, 6)
fig = px.line(variacao,
              labels={'index': 'Semana', 'mercado': 'Variação de Mercado '},
              template='simple_white'
             )
fig.update_layout(title={'text':'Média Movel de Avalizção de Mercado', 'y':0.95, 'x':0.5})
             
fig.show()


# In[80]:


# Variação de Mercado:
df = df_variacao_mercado
df.columns=['Variação de Mercado', 'Variaçao Movel 4 semanas','Taxa de Crecimento']
fig = figsize=(9, 6)
fig = px.line(df,
              labels={'index': 'Semana', 'value': 'Variação de Mercado',
                      },
              template='simple_white')
fig.update_layout(title={
                    'text': 'Taxa de Crescimento de Mercado',
                    'y':0.95,
                    'x':0.5}
                 )             
fig.show()


# # Análise de Produtos:
# 

# In[81]:


## Criando uma lista com as colunas de vendas:
vendas = [c for c in df_base.columns if c.startswith('vendas')]


# In[82]:


# Filtrar a tabela somente com os valores de vendas:
vendas_marcas= df_base[vendas].sum().sort_values(ascending=False)
# Arterando o nome do index:
vendas_marcas.index = vendas_marcas.index.str.replace('vendas_',"").str.strip().str.title()


# In[83]:


df = vendas_marcas
fig = px.bar(vendas_marcas, 
             template='simple_white', 
             text='value',
            labels={'index': 'Marca', 'value': 'Vendas'}
            )
fig.update_traces(textposition='inside',
                  texttemplate='%{text:.2s}'
                 )
fig.update_layout(title={'text':'Total  de Mercado por Marca','y':0.95,'x':0.5})
fig.show()


# - Participação Total de Mercado por Produto

# In[84]:


# Participação Total de Mercado
df = vendas_marcas/mercado*100
fig = px.bar(df, template='simple_white', text='value',
            labels={'index': 'Mercado', 'value': ' Total Participação %'})
fig.update_traces(textposition='inside',texttemplate='%{text:.2}%')
fig.update_layout(title={'text':'Participação Total de Mercado','y':0.95,'x':0.5})
fig.show()


# ## Análise detalhadas:
# - Média de Mercado por Marca

# In[85]:


df_base[vendas].describe()


# In[86]:


##Boxplot de Vendas:
df= df_base[vendas]
df.columns= df.columns.str.replace('vendas_','').str.title()
fig = px.box(df, 
             template='simple_white',
             labels={'value':'Vendas','variable': ''}
            )
fig.update_layout(title={'text':'Boxplot de Vendas por Marca','y':0.95,'x':0.5})
fig.show()


# In[87]:


# Adicionando a coluna mercado
vendas2=[c for c in df_base.columns if c.startswith('vendas') or c == 'mercado']


# In[88]:


# Criando um DataFrame df_vendas2 para seleciornar-mos as colunas necessaria para a nossa analise:
df_vendas2= df_base[vendas2]


# - Calculando a participação de mercado para cada marca por semana

# In[89]:


for i in df_vendas2.columns:
    if i != 'mercado':
        df_vendas2[i]/=df_vendas2['mercado']
         


# In[90]:


# Retirando a coluna mercado da amostra:
df_vendas2= df_vendas2.drop(['mercado'], axis=1)


# In[93]:


df_vendas2.columns= df_vendas2.columns.str.replace('Vendas_','').str.strip().str.title()


# In[94]:


df_vendas2.head(5)


# - Análise descritiva das Marcas:
#  

# In[95]:


# Resumo estatístico da participação de mercado  
df_vendas2.describe()


# In[96]:


# Boxplot da participação de mercado:
df= df_vendas2
fig = px.box(df, 
             template='simple_white',
             points='all',
             labels={'value':' Participação do Mercado','variable': 'Marca'}
            )
fig.update_layout(title={'text':'Boxplot de Participação por Marca','y':0.95,'x':0.5})
fig.show()


# - Analizando a participação da Whittaker

# A Marca Whittaker apresenta maior Variabilidade:

# In[75]:


## Histograma da participação da Whittaker:
df=df_vendas2['Whittaker']
fig = figsize=(9,6)
fig = px.histogram(df, 
                   template='simple_white',
                   labels={'value': ' Participação', 'count':'nº de partipação'}
                  )
fig.update_layout(title={'text':'Histograma de Mercado', 'y':0.95, 'x':0.5})
fig.show()


# #### Para Obter maior detalhes Vamos dividir a base em 2 anos para entedermos as mudanças de participação das marcas
# 

# In[97]:


# A função personalizada
def ano(Coluna):
    x = np.where(Coluna <= 52, '1º ano', '2º ano')
    return x


# In[98]:


# Adicionando a coluna de Ano:
df_base['ano']= ano(df_base.index)


# In[99]:


df_vendas2['ano']= ano(df_vendas2.index)


# - Participação de mercado das marcas por ano

# In[100]:


# Resumo de participação de mercado do 1º ano:
df_vendas2[df_vendas2['ano']=='1º ano'].describe()


# In[101]:


#Resumo de participação de mercado do 2º ano
df_vendas2[df_vendas2['ano']=='2º ano'].describe()


# In[102]:


df_vendas2.columns


# In[103]:


df = df_vendas2.groupby('ano').agg(lambda x: np.mean(x)*100).T
fig= px.bar(df, color= 'ano',barmode="group",text='value',
           labels={'value':' % Participação', 'index':''},
           template='simple_white')
fig.update_traces(textposition='inside',texttemplate='%{text:.2}%')
fig.update_layout(title={'text':'Percentual Médio de Participação de Mercado','y':0.95,'x':0.5})
fig.show()


# In[104]:



df = df_vendas2.groupby('ano').agg(lambda x: x.median()*100).T
fig= px.bar(df, color= 'ano',barmode="group",text='value',
           labels={'value':' % Participação', 'index':''},
            template='simple_white'
           )
fig.update_traces(textposition='inside',texttemplate='%{text:.2}%')
fig.update_layout(title={'text':'Percentual Mediano de Participação de Mercado','y':0.95,'x':0.5})
fig.show()


# - Analizar a marca whittaker e a Caddury

# In[105]:


df_base.columns


# In[106]:


# Gráfico de disperção da Marca Whitteker
df= df_base[['vendas_whittaker', 'preco_atual_whittaker']]
fig= px.scatter(df, x='preco_atual_whittaker', y='vendas_whittaker', trendline='ols',template="simple_white")
fig.update_layout(title={'text':'Vendas x Preço da Whittaker','y':0.95,'x':0.5})
fig.show()


# In[107]:


# Gráfico de disperção da Marca Whitteker
df= df_base[['vendas_cadbury', 'preco_atual_cadbury']]
fig= px.scatter(df, x='preco_atual_cadbury', y='vendas_cadbury',
                trendline='ols',template="simple_white",
               )
fig.update_layout(title={'text':'Vendas x Preço da cadbury','y':0.95,'x':0.5})
fig.show()


# - Estratégia de preço

# In[108]:


### Preço Médio das Marcas
preco = [i for i in df_base.columns if i.startswith('preco_atual') or i =='ano']


# In[109]:


# Estrategia de Preco
df_base[preco].groupby('ano').mean().T


# In[110]:


df= df_base[preco].groupby(ano).mean().T
df.index =df.index.str.replace('preco_atual_','').str.strip().str.title()
fig= px.bar(df,barmode="group",text='value',
           labels={'value':'Média de Preço', 'index':'Marca'},
            template='simple_white'
           )
fig.update_traces(textposition='inside',texttemplate='%{text:.2}')
fig.update_layout(title={'text':'Média de Preço por Marca','y':0.95,'x':0.5})
fig.show()


#    - Estrategia de A&D

# In[111]:


## criando uma lista com somente as colunas de anuncios.
anunciodisplay = [c for c in df_base.columns if c.startswith('ad_') or c == 'ano']


# In[112]:


df_base[anunciodisplay].groupby('ano').agg(lambda x: np.mean(x)*100).T


# In[113]:


df = df_base[anunciodisplay].groupby('ano').agg(lambda x: np.mean(x)*100).T
df.index = df.index.str.replace('ad_', '').str.strip().str.title()
fig= px.bar(df,barmode="group",text='value',
           labels={'value':'Média de Preço', 'index':'Marca'},
            template='simple_white'
           )
fig.update_traces(textposition='inside',texttemplate='%{text:.2}')
fig.update_layout(title={'text':'Média de Preço por Marca','y':0.95,'x':0.5})
fig.show()

