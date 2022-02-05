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


# In[4]:


##informações do df:
df_base.size


# ## Resumo:
#  - Total de vandas
#  - Vendas por Marcas
#  - Média de vendas por Semana
#  - Variação de Vendas por Semana

# In[5]:


# Colunas da tabela
df_base.columns


# In[6]:


# Transformar todas as Colunas em menúsculas:
df_base.columns = df_base.columns.str.lower()


# In[7]:


# Modificar o indice
df_base.set_index('semana',inplace=True)


# In[8]:


### Adicionar a coluna mercado que é a soma de todas as vendas:
df_base['mercado'] = 0
for i in df_base.columns:
    if i.startswith('vendas'):
        df_base['mercado'] += df_base[i]
        


# In[9]:


df_base.head(5)


# 
# ## Total de Mercado

# In[10]:


mercado = df_base['mercado'].sum()
print(f'Total de mercado de Chocolate foi de: R${mercado}')


# In[11]:


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


# In[12]:


# análise estatistica do mercado:
data.describe()


# In[13]:


# Histrograma de total de mercado:
df= data
fig = figsize=(9,6)
fig = px.histogram(df, 
                   marginal='violin',
                   template='simple_white'
                  )
fig.update_layout(title={'text':'Histograma de Mercado', 'y':0.95, 'x':0.5})
fig.show()


# In[14]:


## Boxplot do total de mercado:
fig= figsize=(10,6)
fig = px.box(data, x='mercado',
             labels={'value':'Vendas','variable': ''},points='all',template='simple_white')
fig.update_layout(title={
    'text': 'Boxplot de Mercado de Chocolate',
    'y': 0.95,
    'x': 0.5
})
fig.show()


#  ## Variação de Mercado
#  
#  verificando a variação do mercado ao longo do tempo:

# In[15]:


df_variacao_mercado = data.pct_change()

df_variacao_mercado


# In[16]:


# Variação de Mercado:
variacao = df_variacao_mercado
fig = figsize=(9, 6)
fig = px.line(variacao, y='mercado',
              labels={'index': 'Semana', 'mercado': 'Variação de Mercado%'},
              template='simple_white'
             )
fig.update_layout(title={'text':'Variação de Mercado', 'y':0.95, 'x':0.5})
             
fig.show()


# In[17]:


# Variação de Mercado dos ultimos 4 semanas:
variacao = df_variacao_mercado['mercado'].rolling(4).mean()
fig = figsize=(9, 6)
fig = px.line(variacao, y='mercado',
              labels={'index': 'Semana', 'mercado': 'Variação de Mercado %'},
              template='simple_white'
             )
fig.update_layout(title={'text':'Variação Movel de Mercado das ultimas 4 semana', 'y':0.95, 'x':0.5})
             
fig.show()


# In[18]:


# Taxa de Crescimento - calculando a média variação total:
taxa_crecimento = df_variacao_mercado['mercado'].mean()
print(f'A taxa de crescimento do mercado é de {"%.2f"%taxa_crecimento}%')


# In[19]:


# Variação de Mercado de Chocolates
df_variacao_mercado['taxa_crecimento'] = taxa_crecimento


# In[20]:


# Variação de Mercado:
df = df_variacao_mercado
fig = figsize=(9, 6)
fig = px.line(df,
              labels={'index': 'Semana', 'mercado': 'Variação de Mercado',
                      'taxa_crecimento':'Taxa de Crescimento'},
              template='simple_white')
fig.update_layout(title={
                    'text': 'Variação do Mercado',
                    'y':0.95,
                    'x':0.5}
                 )             
fig.show()


# # Análise de Produtos:
# 

# In[21]:


vendas = []
for c in list(df_base.columns):
    if c.startswith('vendas'):
        vendas.append(c)


# In[22]:


# Filtrar a tabela somente com os valores de vendas:
vendas_marcas= df_base[vendas].sum().sort_values(ascending=False)
# Arterando o nome do index:
vendas_marcas.index = vendas_marcas.index.str.replace('vendas_',"").str.strip().str.title()


# In[23]:


df = vendas_marcas
fig = px.bar(vendas_marcas, 
             template='simple_white', 
             text='value',
            labels={'index': 'produto', 'value': 'Mercado'}
            )
fig.update_traces(textposition='inside',
                  texttemplate='%{text:.2s}'
                 )
fig.update_layout(title={'text':'Total  de Mercado por Produto','y':0.95,'x':0.5})
fig.show()


# - Participação Total de Mercado por Produto

# In[24]:


# Participação Total de Mercado
df = vendas_marcas/mercado*100
fig = px.bar(df, template='simple_white', text='value',
            labels={'index': 'produto', 'value': ' Total Participação %'})
fig.update_traces(textposition='inside',texttemplate='%{text:.2}%')
fig.update_layout(title={'text':'Participaçãp Total de Mercado','y':0.95,'x':0.5})
fig.show()


# ## Análise detalhadas:
# - Média de Mercado por Marca

# In[25]:


df_base[vendas].describe()


# In[26]:


##Boxplot de Vendas:
df= df_base[vendas]
fig = px.box(df, 
             template='simple_white',
             labels={'value':'Mercado','variable': ''}
            )
fig.update_layout(title={'text':'Boxplot de Vendas por Marca','y':0.95,'x':0.5})
fig.show()


# In[27]:


#Adicionando os nomes das colunas para o filtro:
vendas2= vendas
vendas2


# In[28]:


# Adicionando a coluna mercado
vendas2.append('mercado')
vendas2


# In[29]:


# Criando um DataFrame df_vendas2 para seleciornar-mos as colunas necessaria para a nossa analise:
df_vendas2= df_base[vendas2]


# - Calculando a participação de mercado para cada marca por semana

# In[30]:


for i in df_vendas2.columns:
    if i != 'mercado':
        df_vendas2[i]/=df_vendas2['mercado']
         


# In[31]:


# Retirando a coluna mercado da amostra:
df_vendas2= df_vendas2.drop(['mercado'], axis=1)


# In[32]:


df_vendas2.head(5)


# In[37]:


# Renomendo as colunas:
df_vendas2.columns = df_vendas2.columns.str.replace('Vendas','Participacao').str.strip().str.title()


# - Análise descritiva das Marcas:
#  

# In[38]:


# Resumo estatístico da participação de mercado  
df_vendas2.describe()


# In[39]:


# Boxplot da participação de mercado:
df= df_vendas2
fig = px.box(df, 
             template='simple_white',
             points='all',
             labels={'value':' de Participação','variable': ''}
            )
fig.update_layout(title={'text':'Participação por Marca','y':0.95,'x':0.5})
fig.show()


# - Analizando a participação da Whittaker

# A Marca Whittaker apresenta maior Variabilidade:

# In[40]:


## Histograma da participação da Whittaker:
df=df_vendas2['Participacao_Whittaker']
fig = figsize=(9,6)
fig = px.histogram(df, 
                   template='simple_white',
                   labels={'value': ' Participação'}
                  )
fig.update_layout(title={'text':'Histograma de Mercado', 'y':0.95, 'x':0.5})
fig.show()


# ### Para Obter maior detalhes Vamos dividir a base sem 2 anos para entedermos as mudanças de participação das marcas
# 

# In[41]:


# A função personalizada
def ano(Coluna):
    x = np.where(Coluna <= 52, '1º ano', '2º ano')
    return x


# In[42]:


# Adicionando a coluna de Ano:
df_base['ano']= ano(df_base.index)


# In[43]:


df_vendas2['ano']= ano(df_vendas2.index)


# - Participação de mercado das marcas por ano

# In[44]:


# Resumo do 1º ano:
df_vendas2[df_vendas2['ano']=='1º ano'].describe()


# In[45]:


df_vendas2[df_vendas2['ano']=='2º ano'].describe()


# In[46]:


df_vendas2.columns


# In[63]:


df = df_vendas2.groupby('ano').agg(lambda x: np.mean(x)*100).T
fig= px.bar(df, color= 'ano',barmode="group",text='value',
           labels={'value':' % Participação', 'index':''},
           template='simple_white')
fig.update_traces(textposition='inside',texttemplate='%{text:.2}%')
fig.update_layout(title={'text':'Percentual Médio de Participação de Mercado','y':0.95,'x':0.5})
fig.show()


# In[62]:



df = df_vendas2.groupby('ano').agg(lambda x: x.median()*100).T
fig= px.bar(df, color= 'ano',barmode="group",text='value',
           labels={'value':' % Participação', 'index':''},
            template='simple_white'
           )
fig.update_traces(textposition='inside',texttemplate='%{text:.2}%')
fig.update_layout(title={'text':'Percentual Mediano de Participação de Mercado','y':0.95,'x':0.5})
fig.show()


# - Analizar a marca whittaker e a Caddury

# In[65]:


df_base.columns


# In[71]:


# Gráfico de disperção da Marca Whitteker
df= df_base[['vendas_whittaker', 'preco_atual_whittaker']]
fig= px.scatter(df, x='preco_atual_whittaker', y='vendas_whittaker', trendline='ols',template="simple_white")
fig.update_layout(title={'text':'Vendas x Preço da Whittaker','y':0.95,'x':0.5})
fig.show()


# In[75]:


# Gráfico de disperção da Marca Whitteker
df= df_base[['vendas_cadbury', 'preco_atual_cadbury']]
fig= px.scatter(df, x='preco_atual_cadbury', y='vendas_cadbury',
                trendline='ols',template="simple_white",
               )
fig.update_layout(title={'text':'Vendas x Preço da cadbury','y':0.95,'x':0.5})
fig.show()


# - Aplicando o logaritimo natual:
# 

# In[77]:


# Gráfico de disperção da Marca Whitteker
df= df_base[['vendas_whittaker', 'preco_atual_whittaker']]
fig= px.scatter(df, x='preco_atual_whittaker', y='vendas_whittaker', 
                trendline='ols',
                template="simple_white",
               log_x=True, log_y=False)
fig.update_layout(title={'text':'Vendas x Preço da Whittaker','y':0.95,'x':0.5})
fig.show()

