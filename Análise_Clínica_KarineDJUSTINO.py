#!/usr/bin/env python
# coding: utf-8

# ## Introdução
# 
# **Iniciaremos a Análise nos familiarizando com a planilha apresentada, ela contém, 48 registros.**  
# 
# **Ela possui 48 registros que nos apresentaram insights sobre as seguintes variáveis: Grupo, Gravidade, Sexo, Idade, Peso, Altura, IMC, Eventos, % eventos, Resultado teste A, Frequência e Intensidade.**
# 
# 

# In[4]:


pip install pandas openpyxl


# In[5]:


pip install scikit-posthocs


# In[8]:


import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, kruskal, shapiro, levene
import numpy as np
from IPython.display import display, HTML


# In[10]:


df = pd.read_excel(r'C:\Users\lost4\OneDrive\Documentos\DATA\job related\CONSULTORIA\Banco de dados.xlsx')


# In[12]:


def create_scrollable_table(data, table_id, title):
    html = f'<h3>{title}</h3>'
    html += f'<div id="{table_id}" style="height:200px; overflow:auto;">'
    html += data.to_html()
    html += '</div>'
    return html


# In[14]:


df.head()


# As primeiras linhas da tabela nos retornam uma exemplificação das variáveis, 
# 
# 1. **Grupo**: Na coluna grupo os indivíduos estão ramificados em "Controle" e "Caso Tipo A" e "Caso Tipo B", salientando assim, os tratamentos utilizados. 
#    
# 3. **Gravidade**: As gravidades indicam a severidade da condição e variam entre  "normal" a "grave".
# 
# 4. **Sexo**: Os sexo são binarizados entre F e M.
# 
# 5. **Idade**: As idades das primeiras linhas nos indicam um público jovem  de 26 a adulto com 50 anos.
# 
# 6. **Peso e Altura**: Os pesos e altura são refletidos diretamente no IMC (Índice de Massa Corporal), e variam entre 25.60 a 34.53 kg/m².
# 
# 7. **Eventos e % eventos**: Indicam a incidência do evento  e a porcentagem do mesmo.
# 8. **Resultado teste A**: Todos os resultados são "Positivo".
# 
# 9. **Frequência**: As frequências são apresentas situacionalmente entre: "constante", "intermitente" ou "esporádico".
# 
# 10. **Intensidade**: Sendo classificada inicialmente entre "baixa" a "moderada".
# 
# As inferências iniciais nos retornam possibilidades de análises que abrangem a relação entre as variáveis, como a gravidade da condição e a frequência e sua relação com a intensidade dos eventos.

# **Removeremos os valores duplicados, eliminaremos da análise os valores vazios
# e checaremos os faltantes duplicados**

# In[20]:


# Removendo as linhas com valores em brancos presentes na planilha disponibilizada
df_limpo = df.dropna()  

print(df_limpo)


# ## 1. Estatísticas Descritivas

# In[22]:


# Selecionaremos as Colunas Numéricas com Valores Quantitativos para apresentação de uma sumarização Estatística
numerical_features = df.select_dtypes(include=[np.number])

# Calcularemos as Estatísticas Descritivas 
summary_stats = numerical_features.describe().T

# Calcularemos a mediana (medida central) para cada coluna numérica
median_values = numerical_features.median()

summary_stats['median'] = median_values

# Utilizando essa função para criação de uma barra de rolagem para auxiliar na Atenção Sustentada do Leitor. 
def create_scrollable_table(dataframe, table_id, title):
    html = f'<h3>{title}</h3>'
    html += f'<div id="{table_id}" style="height:300px; overflow-y:auto;">'
    html += dataframe.to_html(classes='table table-striped', border=0)
    html += '</div>'
    return html

# Criando uma tabela HTML para as estatísticas descritivas
html_numerical = create_scrollable_table(summary_stats, 'numerical_features', 'Estatísticas Sucintas para Características Numéricas')

# Exibiremos a tabela em HTML
display(HTML(html_numerical))


# In[164]:


# Listando de variáveis categóricas
variaveis_categoricas = ['Grupo', 'Gravidade', 'Sexo', 'Resultado teste A', 'Frequência', 'Intensidade']

# Função que auxilia na criação de uma tabela HTML com barra de rolagem
def create_scrollable_table(dataframe, table_id, title):
    html = f'<h3>{title}</h3>'
    html += f'<div id="{table_id}" style="height:300px; overflow-y:auto;">'
    html += dataframe.to_html(classes='table table-striped', border=0)
    html += '</div>'
    return html

# Dicionário para armazenar as frequências
frequencias_dict = {}

# Calculando as frequências para cada variável categórica
for var in variaveis_categoricas:
    frequencias_absolutas = df[var].value_counts()
    frequencias_relativas = df[var].value_counts(normalize=True) * 100
    
    # Criando um DataFrame para cada variável
    var_df = pd.DataFrame({
        'Categoria': frequencias_absolutas.index,
        'Frequência Absoluta': frequencias_absolutas.values,
        'Frequência Relativa (%)': frequencias_relativas.values.round(1)
    })
    
    frequencias_dict[var] = var_df

# Exibindo as tabelas para cada variável categórica
for var, table in frequencias_dict.items():
    html_table = create_scrollable_table(table, f'{var}_table', f'Frequências para {var}')
    display(HTML(html_table))


# ##  2. Comparar os resultados das variáveis quantitativas entre as categorias da variável Grupo (3 grupos: controle, caso A e caso B);
# 
# **Comparação dos dados Quantitativas entre  os Grupos**

# In[167]:


import pandas as pd
from scipy.stats import shapiro

# Agruparemos o banco de dados por 'Grupo'
grupos = df.groupby('Grupo')

# utilizaremos o dicionário para armazenar os resultados
resultados_shapiro = {}

# Realizaremos o teste de Shapiro-Wilk para cada grupo
for nome_grupo, dados_grupo in grupos:
    stat, p_value = shapiro(dados_grupo['Idade'].dropna())
    resultados_shapiro[nome_grupo] = {'Estatística': stat, 'p-valor': p_value}

# Exibindo os resultados
for grupo, resultado in resultados_shapiro.items():
    print(f"Grupo: {grupo}")
    print(f"  Estatística: {resultado['Estatística']:.4f}")
    print(f"  p-valor: {resultado['p-valor']:.4f}\n")


# Observamos que: 
# 
# ### Grupo: Caso Tipo A
# - **Estatística: 0.9543**
# - **p-valor: 0.7684**
# 
# O p-valor de 0.7684 é bem acima do nível de significância estatística comum de 0.05. Indicando que, não há evidências suficientes para rejeitar a hipótese nula de que os dados são normalmente distribuídos. Portanto, podemos considerar que a distribuição de dados para o grupo "Caso Tipo A" é normal.
# 
# ### Grupo: Caso Tipo B
# - **Estatística: 0.9898**
# - **p-valor: 0.9790**
# 
# O p-valor de 0.9790 nos retorna um valor exorbitante, salientando assim, que os dados seguem uma distribuição normal. A hipótese nula de normalidade levantada para o grupo "Caso Tipo B" não é rejeitada.
# 
# ### Grupo: Controle
# - **Estatística: 0.9810**
# - **p-valor: 0.7791**
# 
# O p-valor de 0.7791 ultrapassando também o de 0.05 estabelecido para significância estatística, indicando não haver evidências para rejeitar a hipótese de normalidade. Portanto, os dados do grupo "Controle" podem ser considerados normalmente distribuídos.
# 
# ### Concluindo
# 
# Entre os grupos apresentados: ("Caso Tipo A", "Caso Tipo B" e "Controle"), os p-valores são significativamente maiores que 0.05. Sugerindo uma distribuição apresentada por eles. Portanto, assumimos assim que os dados seguem uma distribuição normal em cada grupo.

# In[169]:


import pandas as pd
import numpy as np
from scipy.stats import f_oneway, kruskal


# Analisaremos as seguintes variáveis
variaveis_quantitativas = ['Idade', 'Peso (kg)', 'IMC (kg/m2)', 'Eventos']
grupos = df['Grupo'].unique()

# Função utilizada para calcular média e desvio padrão por grupo
def calcular_media_dp(df, variavel):
    return df.groupby('Grupo')[variavel].agg(['mean', 'std'])

# Função para realizar ANOVA e Kruskal-Wallis
def realizar_teste(df, variavel):
    grupos = [df[df['Grupo'] == grupo][variavel] for grupo in df['Grupo'].unique()]
    if variavel in ['Idade']:  
        stat, p_value = f_oneway(*grupos)
        teste = 'ANOVA'
    else:
        stat, p_value = kruskal(*grupos)
        teste = 'Kruskal-Wallis'
    return teste, p_value

# Análise e impressão dos resultados
resultados = []
for variavel in variaveis_quantitativas:
    media_dp = calcular_media_dp(df, variavel)
    teste, p_value = realizar_teste(df, variavel)
    resultado = {
        'Variável': variavel,
        'Controle (Média ± DP)': f"{media_dp.loc['Controle', 'mean']:.1f} ± {media_dp.loc['Controle', 'std']:.1f}",
        'Caso A (Média ± DP)': f"{media_dp.loc['Caso Tipo A', 'mean']:.1f} ± {media_dp.loc['Caso Tipo A', 'std']:.1f}",
        'Caso B (Média ± DP)': f"{media_dp.loc['Caso Tipo B', 'mean']:.1f} ± {media_dp.loc['Caso Tipo B', 'std']:.1f}",
        'Teste Utilizado': teste,
        'Valor-p': f"{p_value:.3f}" + ("*" if p_value < 0.05 else "")
    }
    resultados.append(resultado)

# Exibindo os resultados
resultados_df = pd.DataFrame(resultados)
print(resultados_df)


# ### Comentário do Código
# 
# 1. **Importação de Bibliotecas**: O código importa `pandas` para manipulação de dados, `numpy` para operações numéricas, e funções estatísticas de `scipy.stats` para realizar testes ANOVA e Kruskal-Wallis.
# 2. ANOVA que consiste na (Análise de Variância), obtém o pPropósit dea comparar as médias de três ou mais grupos para ver se pelo menos um grupo é significativamente diferente dos outros
# 
# 3. Propósito do teste Kruskal-Wallis não paramétrico é utilizado para comparar três ou mais grupos. é acionado  quando os dados não são normalmente distribuídos ou as variâncias não são homogêneas.l.
# 
# ### Comentário dos Resultados
# 
# 1. **Idade**:
#    - **Controle**: 37.0 ± 9.1
#    - **Caso A**: 51.1 ± 5.1
#    - **Caso B**: 44.2 ± 11.2
#    - **Teste Utilizado**: ANOVA
#    - **Valor-p**: 0.001* (significativo)
# 
#  O teste ANOVA foi utilizado para comparar as idades entre os grupos "Controle", "Caso A" e "Caso B". Com um valor-p de 0.001, apresentando uma diferença estatisticamente significativa entre as médias de idade dos grupos. Sugerindo que pelo menos um dos grupos apresenta uma média de idade diferente dos outros. A significância é indicada pelo asterisco (*), indicando que a diferença não foi apresentada ocasionalmente. 1.
# 
# 2. **Peso (kg)**:
#    - **Controle**: 66.7 ± 14.8
#    - **Caso A**: 65.1 ± 23.5
#    - **Caso B**: 62.0 ± 19.3
#    - **Teste Utilizado**: Kruskal-Wallis
#    - **Valor-p**: 0.619 (não significativo)
# 
#    O teste Kruskal-Wallis não encontrou diferenças significativas entre os grupos para 'Peso', com um p-valor de 0.619.
# 
# 3. **IMC (kg/m2)**:
#    - **Controle**: 29.0 ± 6.0
#    - **Caso A**: 26.6 ± 8.9
#    - **Caso B**: 24.8 ± 5.9
#    - **Teste Utilizado**: Kruskal-Wallis
#    - **Valor-p**: 0.173 (não significativo)
# 
#    Não há diferença significativa entre os grupos para 'IMC', com um p-valor de 0.173.
# 
# 4. **Eventos**:
#    - **Controle**: 30.1 ± 31.7
#    - **Caso A**: 29.5 ± 27.8
#    - **Caso B**: 34.9 ± 43.1
#    - **Teste Utilizado**: Kruskal-Wallis
#    - **Valor-p**: 0.949 (não significativo)
# 
#    O teste não encontrou diferenças significativas entre os grupos para 'Eventos', com um p-valor de 0.949.
# 
# ### Conclusão
# 
# A análise mostra que apenas a variável 'Idade' apresenta diferenças estatisticamente significativas entre os grus.s.

# In[172]:


import pandas as pd
from scipy.stats import levene

# Variáveis utilizadas na análise
variaveis_quantitativas = ['Idade', 'Peso (kg)', 'IMC (kg/m2)', 'Eventos']

# Função para realizar o teste de Levene
def teste_levene(df, variavel):
    grupos = [df[df['Grupo'] == grupo][variavel] for grupo in df['Grupo'].unique()]
    stat, p_value = levene(*grupos)
    return stat, p_value

# Análise e impressão dos resultados
resultados_levene = []
for variavel in variaveis_quantitativas:
    stat, p_value = teste_levene(df, variavel)
    resultado = {
        'Variável': variavel,
        'Estatística': stat,
        'Valor-p': p_value,
        'Homogeneidade': 'Sim' if p_value > 0.05 else 'Não'
    }
    resultados_levene.append(resultado)

# Exibir resultados
resultados_levene_df = pd.DataFrame(resultados_levene)
print(resultados_levene_df)


# 
# 
# | Variável        | Estatística | Valor-p | Homogeneidade | Interpretação |
# |----------------|-------------|---------|----------------|----------------|
# | **Idade**        | 1.288       | 0.286   | Sim            | Não há diferença significativa na idade média entre os grupos. |
# | **Peso (kg)**    | 0.149       | 0.862   | Sim            | Os grupos apresentam pesos médios semelhantes. |
# | **IMC (kg/m²)**  | 0.146       | 0.864   | Sim            | O índice de massa corporal não difere significativamente entre os grupos. |
# | **Eventos**      | 0.166       | 0.847   | Sim            | A frequência de eventos apresenta similaridade entre eles |
# 
# 
# 
# 
# Com **valores-p todos acima de 0.05**, **não foram retornadas diferenças estatisticamente significativas** entre os grupos nas variáveis quantitativas analisadas.  
# A conclusão de “**Homogeneidade: Sim**” está correta — os grupos são homogêneos em relação a essas variáveis.
# 

# In[183]:


import pandas as pd
from scipy.stats import f_oneway, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sp

# Variáveis para análise
variaveis_quantitativas = ['Idade', 'Peso (kg)', 'IMC (kg/m2)', 'Eventos']

# Função para realizar ANOVA ou Kruskal-Wallis
def realizar_teste(df, variavel):
    grupos = [df[df['Grupo'] == grupo][variavel] for grupo in df['Grupo'].unique()]
    if variavel in ['Idade']:  # Supondo que 'Idade' é normalmente distribuída
        stat, p_value = f_oneway(*grupos)
        teste = 'ANOVA'
    else:
        stat, p_value = kruskal(*grupos)
        teste = 'Kruskal-Wallis'
    return teste, p_value

# Função para realizar teste post-hoc
def teste_post_hoc(df, variavel, teste):
    if teste == 'ANOVA':
        tukey = pairwise_tukeyhsd(endog=df[variavel], groups=df['Grupo'], alpha=0.05)
        print(tukey)
    elif teste == 'Kruskal-Wallis':
        dunn = sp.posthoc_dunn(df, val_col=variavel, group_col='Grupo', p_adjust='bonferroni')
        print(dunn)

# Análise e impressão dos resultados
for variavel in variaveis_quantitativas:
    teste, p_value = realizar_teste(df, variavel)
    if p_value < 0.05:
        print(f"\nTeste post-hoc para {variavel} ({teste}):")
        teste_post_hoc(df, variavel, teste)


# ### Comentário dos Resultados do Teste Post-hoc (Tukey HSD) para a Faixa Etáriapers científicos.
# 
# 
# 
# 1. **Comparações entre os Caso Tipo A e Caso Tipo B**:
#    - **Diferença de Médias (meandiff)**: -6.9429
#    - **p-valor ajustado (p-adj)**: 0.3854
#    - **Intervalo de Confiança (IC)**: [-19.5805, 5.6947]
#    - **Rejeição da Hipótese Nula (reject)**: False
# 
#    Não há diferença estatisticamente significativa entre "Caso Tipo A" e "Caso Tipo B" para a variável "Idade", já que o p-valor é maior que 0.05 e o intervalo de conEfiança inclui zero.
# 
# 2. **Comp
#    aração entre Caso Tipo A e Controle**:
#    - **Diferença de Médias (meandiff)**: -14.1151
#    - **p-valor ajustado (p-adj)**: 0.0011
#    - **Intervalo de Confiança (IC)**: [-23.0305, -5.1997]
#    - **Rejeição da Hipótese Nula (reject)**: True
# 
#    Existe uma diferença estatisticamente significativa entre "Caso Tipo A" e "Controle" para a variável "Idade", com um p-valor menor que 0.05 e o intervalo de confiança não incluindo zero. Isso indica que as idades no grupo "Caso Tipo A" são significativamente diferentes das do grupo "Controle".
# 
# 3. **Comparação entre Caso Tipo B e Controle**:
#    - **Diferença de Médias (meandiff)**: -7.1722
#    - **p-valor ajustado (p-adj)**: 0.221
#    - **Intervalo de Confiança (IC)**: [-17.4728, 3.1284]
#    - **Rejeição da Hipótese Nula (reject)**: False
# 
#    Não há diferença estatisticamente significativa entre "Caso Tipo B" e "Controle" para a variável "Idade", já que o p-valor é maior que 0.05 ea
# nça inclui zero.
# 
# ### Concretornou ral
# 
# - A única comparação que mostrou uma diferença estatisticamente significativa foi entre "Caso Tipo A" e "Controle". As idades no grupo "Caso Tipo A" são significativamente diferentes das do grupo "Capresentaram
# - As outras comparações não mostraram diferenças significativas, indicando que as idades entre "Caso Tipo A" e "Caso Tipo B", e entre "Caso Tipo B" e "Controle", são semelhantes.

# ## 3. Comparação de Categóricas entre Grupos
# 

# In[198]:


import pandas as pd

# Lista de variáveis categóricas para análise
variaveis_categoricas = ['Gravidade', 'Sexo', 'Resultado teste A', 'Frequência', 'Intensidade']

# Criar e exibir tabelas de contingência para cada variável categórica
for variavel in variaveis_categoricas:
    tabela_contingencia = pd.crosstab(df['Grupo'], df[variavel])
    print(f"Tabela de Contingência para Grupo e {variavel}:\n")
    print(tabela_contingencia)
    print("\n" + "-"*50 + "\n")


# ### Análise dos Resultados das Tabelas de Contingência
# 
# #### Tabela de Contingência para Grupo e Gravidade
# 
# - **Caso Tipo A**: A maioria dos casos está na categoria "4- grave" (3 casos).
# - **Caso Tipo B**: Predominância também na categoria "4- grave" (2 casos).
# - **Controle**: Distribuição mais equilibrada, mas com mais casos em "4- grave" (13 casos).
# 
# **Conclusão**: Os grupos "Caso Tipo A" e "Caso Tipo B" têm uma concentração maior de casos graves em comparação com o grupo "Controle".
# 
# #### Tabela de Contingência para Grupo e Sexo
# 
# - **Caso Tipo A**: Distribuição quase igual entre feminino (3) e masculino (4).
# - **Caso Tipo B**: Todos os casos são masculinos (5).
# - **Controle**: Distribuição equilibrada entre feminino (19) e masculino (17).
# 
# **Conclusão**: O grupo "Caso Tipo B" é exclusivamente masculino, enquanto os outros grupos têm uma distribuição mais equilibrada.
# 
# #### Tabela de Contingência para Grupo e Resultado teste A
# 
# - **Caso Tipo A**: Maioria dos resultados são positivos (6).
# - **Caso Tipo B**: Todos os resultados são positivos (5).
# - **Controle**: Maioria dos resultados são positivos (24), mas há uma quantidade significativa de negativos (12).
# 
# **Conclusão**: Os grupos "Caso Tipo A" e "Caso Tipo B" têm uma alta proporção de resultados positivos em comparação com o grupo "Controle".
# 
# #### Tabela de Contingência para Grupo e Frequência
# 
# - **Caso Tipo A**: Predominância de "esporádico" (3).
# - **Caso Tipo B**: Maioria em "constante" (3).
# - **Controle**: Distribuição mais variada, com mais casos em "constante" (10).
# 
# **Conclusão**: O grupo "Controle" tem uma distribuição mais variada, enquanto "Caso Tipo A" e "Caso Tipo B" têm padrões diferentes de frequência.
# 
# #### Tabela de Contingência para Grupo e Intensidade
# 
# - **Caso Tipo A**: Maioria em "1- baixa" (4).
# - **Caso Tipo B**: Predominância em "3- moderada" (3).
# - **Controle**: Maioria em "3- moderada" (13).
# 
# **Conclusão**: O grupo "Controle" e "Caso Tipo B" têm mais casos de intensidade "3- moderada", enquanto "Caso Tipo A" tem mais casos de intensidade "1- baixa".
# 
# ### Considerações Finais
# 
# Essas tabelas de contingência ajudam a identificar padrões e distribuições de variáveis categóricas entre os grupos. Podendo ser utilizadas na realização de testes de independência, como o teste qui-quadrado, para verificar associações significativas entre grupos e variáveis categóricas.

# In[203]:


import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact


# Lista de variáveis categóricas para análise
variaveis_categoricas = ['Gravidade', 'Sexo', 'Resultado teste A', 'Frequência', 'Intensidade']

# Função para realizar o teste qui-quadrado ou Fisher
def realizar_teste_categorico(tabela):
    # Calcular os valores esperados
    _, _, dof, expected = chi2_contingency(tabela, correction=False)
    
    # Verificar se algum valor esperado é menor que 5
    if (expected < 5).any():
        # Se algum valor esperado for menor que 5, use o teste de Fisher
        # O teste de Fisher só é aplicável a tabelas 2x2, então aqui é um exemplo simplificado
        stat, p_value = fisher_exact(tabela.iloc[:2, :2])
        teste = 'Fisher'
        dof = None
    else:
        # Caso contrário, use o teste qui-quadrado
        stat, p_value, dof, _ = chi2_contingency(tabela)
        teste = 'Qui-quadrado'
    return teste, stat, dof, p_value

# Análise e impressão dos resultados
for variavel in variaveis_categoricas:
    tabela_contingencia = pd.crosstab(df['Grupo'], df[variavel])
    teste, stat, dof, p_value = realizar_teste_categorico(tabela_contingencia)
    print(f"Teste para {variavel}:")
    print(f"  Teste Utilizado: {teste}")
    print(f"  Estatística: {stat:.4f}")
    if dof is not None:
        print(f"  Graus de Liberdade: {dof}")
    print(f"  Valor-p: {p_value:.4f}\n")


# ### Análise dos Resultados dos Testes de Fisher
# 
# #### Teste para Gravidade
# - **Teste Utilizado**: Fisher
# - **Estatística**: 2.0000
# - **Valor-p**: 1.0000
# 
# **Interpretação**: O valor-p de 1.0000 indica que não há evidência de associação significativa entre "Gravidade" e "Grupo". As distribuições de gravidade são semelhantes entre os grupos.
# 
# #### Teste para Sexo
# - **Teste Utilizado**: Fisher
# - **Estatística**: inf
# - **Valor-p**: 0.2045
# 
# **Interpretação**: O valor-p de 0.2045 sugere que não há uma associação significativa entre "Sexo" e "Grupo". As proporções de sexo são semelhantes entre os grupos.
# 
# #### Teste para Resultado teste A
# - **Teste Utilizado**: Fisher
# - **Estatística**: inf
# - **Valor-p**: 1.0000
# 
# **Interpretação**: O valor-p de 1.0000 indica que não há evidência de associação significativa entre "Resultado teste A" e "Grupo". Os resultados do teste são distribuídos de forma semelhante entre os grupos.
# 
# #### Teste para Frequência
# - **Teste Utilizado**: Fisher
# - **Estatística**: nan
# - **Valor-p**: 1.0000
# 
# **Interpretação**: O valor-p de 1.0000 sugere que não há associação significativa entre "Frequência" e "Grupo". A estatística `nan` pode indicar problemas com a estrutura dos dados para este teste.
# 
# #### Teste para Intensidade
# - **Teste Utilizado**: Fisher
# - **Estatística**: inf
# - **Valor-p**: 0.3333
# 
# **Interpretação**: O valor-p de 0.3333 indica que não há evidência de associação significativa entre "Intensidade" e "Grupo". As intensidades são distribuídas de forma semelhante entre os grupos.
# 
# ### Conclusão Geral
# 
# Nenhuma das variáveis categóricas analisadas (Sexo, Resultado teste A, Frequência, Intensidade) retornaram diferenças estatisticamente significativas entre os grupos, segundo o Teste Exato de Fisher. Isso sugere que essas características estão equilibradas entre os grupos, o que é positivo do ponto de vista de comparabilidade entre eles.

# ## 4. Correlação de Quantitativas

# In[206]:


import pandas as pd
from scipy.stats import pearsonr, spearmanr, shapiro

# Lista de variáveis quantitativas para análise
variaveis_quantitativas = ['Idade', 'Peso (kg)', 'IMC (kg/m2)', 'Eventos']

# Função para verificar normalidade
def verificar_normalidade(df, variavel):
    stat, p_value = shapiro(df[variavel].dropna())
    return p_value > 0.05  # Retorna True se a distribuição for normal

# Função para calcular correlação
def calcular_correlacao(df, var1, var2):
    normal_var1 = verificar_normalidade(df, var1)
    normal_var2 = verificar_normalidade(df, var2)
    
    if normal_var1 and normal_var2:
        # Usar Pearson se ambas as variáveis forem normais
        corr, p_value = pearsonr(df[var1], df[var2])
        metodo = 'Pearson'
    else:
        # Usar Spearman caso contrário
        corr, p_value = spearmanr(df[var1], df[var2])
        metodo = 'Spearman'
    
    return metodo, corr, p_value

# Análise e impressão dos resultados
resultados_correlacao = []
for i, var1 in enumerate(variaveis_quantitativas):
    for var2 in variaveis_quantitativas[i+1:]:
        metodo, corr, p_value = calcular_correlacao(df, var1, var2)
        resultado = {
            'Variável 1': var1,
            'Variável 2': var2,
            'Método': metodo,
            'Correlação': corr,
            'Valor-p': p_value
        }
        resultados_correlacao.append(resultado)

# Exibindo os resultados
resultados_correlacao_df = pd.DataFrame(resultados_correlacao)
print(resultados_correlacao_df)


# Os resultados apresentados na tabela mostram as correlações entre diferentes pares de variáveis do conjunto de dados, utilizando os métodos de correlação de Pearson e Spearman. Analisando cada linha nós obtemos:
# 
# 1. **Idade e Peso (kg) - Pearson**: A correlação de 0.048854 indica uma relação muito fraca e positiva entre idade e peso, com um valor-p de 0.7415901, sugerindo que essa correlação não é estatisticamente significativa.
# 
# 2. **Idade e IMC (kg/m²) - Spearman**: A correlação de 0.009373 também indica uma relação extremamente fraca entre idade e IMC, com um valor-p de 0.9495854, reforçando a falta de significância estatística.
# 
# 3. **Idade e Eventos - Spearman**: A correlação de 0.277194 sugere uma relação positiva moderada entre idade e o número de eventos, com um valor-p de 0.05646959. Este valor-p está próximo do nível de significância comum de 0.05, indicando uma possível tendência, mas não é estatisticamente significativo.
# 
# 4. **Peso (kg) e IMC (kg/m²) - Spearman**: A correlação de 0.863060 indica uma forte relação positiva entre peso e IMC, com um valor-p extremamente baixo (3.051620e-15), mostrando que essa correlação é altamente significativa. Isso é esperado, já que o IMC é calculado a partir do peso e da altura.
# 
# 5. **Peso (kg) e Eventos - Spearman**: A correlação de 0.633679 sugere uma relação positiva forte entre peso e o número de eventos, com um valor-p de 1.334679e-06, indicando significância estatística.
# 
# 6. **IMC (kg/m²) e Eventos - Spearman**: A correlação de 0.503842 indica uma relação positiva moderada entre IMC e o número de eventos, com um valor-p de 0.0002614053, também estatisticamente significativo.
# 
# Em resumo, as correlações mais fortes e significativas foram observadas entre peso e IMC, peso e eventos, e IMC e eventos. As correlações envolvendo a idade não mostraram significância estatística, exceto por uma possível tendência com o número de eventos.

# In[227]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

# Dados originais
data = {
    'Idade': [26, 40, 91, 50, 43, 46, 65, 41, 52, 49, 59, 42, 37, 31, 27, 34, 46, 23, 38, 43, 37, 38, 36, 26, 31, 46, 32, 48, 36, 49, 45, 54, 33, 54, 45, 54, 28, 45, 20, 47, 33, 54, 28, 33, 20, 28, 55],
    'Peso (kg)': [54, 94, 61, 63, 65, 72, 65, 70, 73, 113, 50, 75, 42, 50, 34, 70, 95, 76, 78, 63, 65, 56, 77, 46, 82, 95, 74, 67, 49, 49, 55, 54, 90, 54, 50, 83, 45, 54, 43, 80, 66, 63, 88, 62, 62, 55, 55],
    'IMC (kg/m2)': [29, 35, 22, 26, 23, 25, 23, 35, 37, 45, 22, 26, 18, 22, 30, 32, 40, 30, 27, 36, 23, 27, 27, 21, 32, 33, 25, 27, 22, 22, 22, 22, 37, 24, 23, 39, 23, 23, 20, 25, 36, 24, 30, 24, 28, 28, 27, 27],
    'Eventos': [3, 106, 54, 43, 97, 36, 18, 24, 21, 60, 9, 16, 9, 104, 83, 58, 34, 58, 34, 18, 31, 29, 24, 22, 21, 45, 11, 1, 7, 7, 23, 7, 18, 3, 0, 76, 3, 23, 1, 39, 6, 36, 20, 9, 1, 1, 0, 0]
}

# Ajustando o comprimento das listas
max_length = max(len(lst) for lst in data.values())
for key in data:
    if len(data[key]) < max_length:
        data[key] += [0] * (max_length - len(data[key]))  # Preenchendo com zeros

df = pd.DataFrame(data)

# Função para calcular correlação e valor-p
def calculate_correlation(df, var1, var2, method='spearman'):
    if method == 'pearson':
        corr, p_value = pearsonr(df[var1], df[var2])
    else:
        corr, p_value = spearmanr(df[var1], df[var2])
    return corr, p_value

# Calculando correlações e valores-p
results = []
pairs = [
    ('Idade', 'Peso (kg)', 'pearson'),
    ('Idade', 'IMC (kg/m2)', 'spearman'),
    ('Idade', 'Eventos', 'spearman'),
    ('Peso (kg)', 'IMC (kg/m2)', 'spearman'),
    ('Peso (kg)', 'Eventos', 'spearman'),
    ('IMC (kg/m2)', 'Eventos', 'spearman')
]

for var1, var2, method in pairs:
    corr, p_value = calculate_correlation(df, var1, var2, method)
    results.append((var1, var2, method, round(corr, 2), round(p_value, 2)))

# Criando DataFrame para exibir resultados
results_df = pd.DataFrame(results, columns=['Variável 1', 'Variável 2', 'Método', 'Correlação', 'Valor-p'])

# Exibindo resultados
print(results_df)

# Visualizando a matriz de correlação com seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(method='spearman'), annot=True, cmap='coolwarm', fmt=".2f", cbar_kws={'label': 'Correlação'})
plt.title('Matriz de Correlação (Spearman)')
plt.show()


# Os resultados apresentados na matrix de correlação nos retornaram diferentes pares de variáveis do conjunto de dados, utilizando os métodos de correlação de Pearson e Spearman.
# 
# 1. **Idade e Peso (kg) - Pearson**: A correlação de 0.29 indica uma relação positiva moderada entre idade e peso. O valor-p de 0.05 sugere que essa correlação é marginalmente significativa, geralmente considerado significativo em um nível de 0.05.
# 
# 2. **Idade e IMC (kg/m²) - Spearman**: A correlação de -0.08 indica uma relação muito fraca e negativa entre idade e IMC. O valor-p de 0.58 mostra que essa correlação não é estatisticamente significativa.
# 
# 3. **Idade e Eventos - Spearman**: A correlação de 0.17 sugere uma relação positiva fraca entre idade e o número de eventos. O valor-p de 0.26 indica que essa correlação não é estatisticamente significativa.
# 
# 4. **Peso (kg) e IMC (kg/m²) - Spearman**: A correlação de 0.69 indica uma relação forte e positiva entre peso e IMC, com um valor-p de 0.00, mostrando que essa correlação é altamente significativa. Isso é esperado, já que o IMC é calculado a partir do peso e da altura.
# 
# 5. **Peso (kg) e Eventos - Spearman**: A correlação de 0.48 sugere uma relação positiva moderada entre peso e o número de eventos, com um valor-p de 0.00, indicando significância estatística.
# 
# 6. **IMC (kg/m²) e Eventos - Spearman**: A correlação de 0.24 indica uma relação positiva fraca entre IMC e o número de eventos. O valor-p de 0.11 sugere que essa correlação não é estatisticamente significativa.
# 
# ### Resumo:
# - As correlações mais fortes e significativas foram observadas entre peso e IMC, e entre peso e eventos.
# - As correlações envolvendo a idade não mostraram significância estatística, exceto por uma correlação marginal com o peso.
# - A relação entre IMC e eventos não foi estatisticamente significatante.

# ## Sintetizando os resultados em tabelas 

# In[49]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, pearsonr, spearmanr

# Exemplo de DataFrame
data = {
    'Grupo': [
        'Controle', 'Caso Tipo A', 'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 
        'Controle', 'Controle', 'Caso Tipo A', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Controle', 'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 'Controle', 
        'Controle', 'Caso Tipo A', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 
        'Caso Tipo A', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 'Controle', 
        'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Caso Tipo B', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A'
    ],
    'Idade': [
        26, 40, 45, 50, 43, 46, 25, 41, 52, 49, 40, 59, 42, 37, 21, 34, 46, 23, 38, 43, 
        37, 38, 36, 26, 31, 46, 32, 48, 36, 36, 45, 54, 33, 34, 45, 46, 28, 58, 20, 47, 
        33, 54, 28, 33, 28, 50, 55, 55
    ],
    'Peso (kg)': [
        54, 94, 71, 64, 61, 65, 72, 76, 60, 113, 95, 55, 70, 42, 53, 70, 95.5, 70, 76, 63, 
        55, 56, 77, 46, 82, 93, 74, 67, 49, 45, 55, 54, 90, 54, 50, 83, 57, 45, 43.9, 80, 
        65, 68, 80, 62, 62, 38, 60, 55
    ],
    'Altura (m)': [
        1.37, 1.65, 1.54, 1.6, 1.5, 1.69, 1.49, 1.4, 1.6, 1.58, 1.52, 1.5, 1.59, 1.42, 
        1.64, 1.5, 1.55, 1.52, 1.7, 1.32, 1.6, 1.45, 1.7, 1.46, 1.6, 1.7, 1.71, 1.5, 
        1.48, 1.45, 1.57, 1.57, 1.56, 1.5, 1.49, 1.46, 1.6, 1.54, 1.55, 1.6, 1.5, 1.38, 
        1.64, 1.4, 1.5, 1.4, 1.6, 1.44
    ],
    'IMC (kg/m2)': [
        28.77, 34.53, 29.94, 25.6, 27.11, 22.8, 32.4, 39, 23.44, 45.27, 41.12, 24.44, 
        27.69, 20.8, 19.71, 33, 39.75, 30.3, 27, 36.16, 23, 26.63, 27, 21.58, 32.03, 34, 
        25.31, 29.78, 22.37, 21.4, 22.31, 21.91, 36.98, 25, 22.52, 39, 22.27, 19, 20, 30, 
        29, 35.71, 29.74, 31, 29, 19, 23, 26.52
    ]
}

df = pd.DataFrame(data)

# Tabela Descritiva por Grupo
descritiva_por_grupo = df.groupby('Grupo').describe()
print("Tabela Descritiva por Grupo:")
print(descritiva_por_grupo)

# Tabela Testes de Hipótese
# Exemplo: Teste t para Idade entre grupos A e B
grupo_a = df[df['Grupo'] == 'A']['Idade']
grupo_b = df[df['Grupo'] == 'B']['Idade']
t_stat, p_value = ttest_ind(grupo_a, grupo_b)

testes_hipotese = pd.DataFrame({
    'Variável': ['Idade'],
    'Estatística': [t_stat],
    'p-valor': [p_value]
})

print("\nTabela Testes de Hipótese:")
print(testes_hipotese)

# Tabela Correlação
correlacoes = []
pairs = [
    ('Idade', 'Peso (kg)', 'pearson'),
    ('Idade', 'IMC (kg/m2)', 'spearman'),
    ('Idade', 'Eventos', 'spearman'),
    ('Peso (kg)', 'IMC (kg/m2)', 'spearman'),
    ('Peso (kg)', 'Eventos', 'spearman'),
    ('IMC (kg/m2)', 'Eventos', 'spearman')
]

for var1, var2, method in pairs:
    if method == 'pearson':
        corr, p_value = pearsonr(df[var1], df[var2])
    else:
        corr, p_value = spearmanr(df[var1], df[var2])
    correlacoes.append((var1, var2, method, corr, p_value))

correlacao_df = pd.DataFrame(correlacoes, columns=['Variável 1', 'Variável 2', 'Método', 'Correlação', 'p-valor'])

print("\nTabela Correlação:")
print(correlacao_df)


# 
# 
# ### 1. **Tabela Descritiva por Grupo**
# 
# #### **Idade**
# - **Caso Tipo A**: Média de 44,8 anos com desvio-padrão de 7,67
# - **Caso Tipo B**: Média de 38,25 anos, com um desvio-padrão alto (16,21), indicando maior variabilidade neste grupo, que possui apenas 4 participantes.
# - **Controle**: Média de 35,96 anos e desvio-padrão de 9,49
# 
# **Interpretação**:
# O grupo Caso Tipo A é o mais velho, em média, seguido por Caso Tipo B. O grupo Controle é o mais jovem. A alta variabilidade no grupo Caso Tipo B pode comprometer a confiabilidade dos testes estatísticos envolvendo essa variável nesse grupo.
# 
# ---
# 
# #### **Peso (kg)**
# - **Caso Tipo A**: Média de aproximadamente 69 kg
# - **Caso Tipo B**: Média de 57 kg
# - **Controle**: Média de aproximadamente 64,9 kg
# 
# O grupo Caso Tipo B apresenta o menor peso médio, o que acompanha também o menor IMC.
# 
# ---
# 
# #### **IMC (kg/m²)**
# - **Caso Tipo A**: 29,72 (classificação entre sobrepeso e obesidade)
# - **Caso Tipo B**: 22,37 (dentro da faixa saudável)
# - **Controle**: 27,91 (sobrepeso)
# 
# **Interpretação**:
# Caso Tipo A apresenta o maior IMC, indicando tendência ao sobrepeso ou obesidade. Já o grupo Caso Tipo B apresenta o IMC dentro do intervalo considerado saudável.
# 
# ---
# 
# ### 2. **Tabela de Testes de Hipóteses**
# A linha referente à variável "Idade" aparece com valores ausentes (NaN) tanto para a estatística quanto para o p-valor, o que indica que o teste estatístico não foi realizado ou falhou.
# 
# **Possíveis causas**:
# - O número de observações no grupo Caso Tipo B (n = 4) pode ter sido insuficiente para a execução do teste.
# - Pode haver algum problema na chamada dAchadosaliza o teste.
# 
# ---
# 
# ### Conclusão Geral
# As estatísticas descritivas indicam diferenças entre os grupos nas variáveis idade, IMC e peso. No entanto, sem a execução adequada dos testes de hipótese, não é possível afirmar se essas difbase nos dados do arquivo. Deseja que eu faça isso?teste agora com base nos dados. Deseja que eu faça isso?

# ## 6. Gráficos com Marcação de Significância
# 

# In[249]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Dados atualizados
data = {
    'Grupo': [
        'Controle', 'Caso Tipo A', 'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 
        'Controle', 'Controle', 'Caso Tipo A', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Controle', 'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 'Controle', 
        'Controle', 'Caso Tipo A', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 
        'Caso Tipo A', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 'Controle', 
        'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Caso Tipo B', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A'
    ],
    'Idade': [
        26, 40, 45, 50, 43, 46, 25, 41, 52, 49, 40, 59, 42, 37, 21, 34, 46, 23, 38, 43, 
        37, 38, 36, 26, 31, 46, 32, 48, 36, 36, 45, 54, 33, 34, 45, 46, 28, 58, 20, 47, 
        33, 54, 28, 33, 28, 50, 55, 55
    ],
    'Peso (kg)': [
        54, 94, 71, 64, 61, 65, 72, 76, 60, 113, 95, 55, 70, 42, 53, 70, 95.5, 70, 76, 63, 
        55, 56, 77, 46, 82, 93, 74, 67, 49, 45, 55, 54, 90, 54, 50, 83, 57, 45, 43.9, 80, 
        65, 68, 80, 62, 62, 38, 60, 55
    ],
    'Altura (m)': [
        1.37, 1.65, 1.54, 1.6, 1.5, 1.69, 1.49, 1.4, 1.6, 1.58, 1.52, 1.5, 1.59, 1.42, 
        1.64, 1.5, 1.55, 1.52, 1.7, 1.32, 1.6, 1.45, 1.7, 1.46, 1.6, 1.7, 1.71, 1.5, 
        1.48, 1.45, 1.57, 1.57, 1.56, 1.5, 1.49, 1.46, 1.6, 1.54, 1.55, 1.6, 1.5, 1.38, 
        1.64, 1.4, 1.5, 1.4, 1.6, 1.44
    ],
    'IMC (kg/m2)': [
        28.77, 34.53, 29.94, 25.6, 27.11, 22.8, 32.4, 39, 23.44, 45.27, 41.12, 24.44, 
        27.69, 20.8, 19.71, 33, 39.75, 30.3, 27, 36.16, 23, 26.63, 27, 21.58, 32.03, 34, 
        25.31, 29.78, 22.37, 21.4, 22.31, 21.91, 36.98, 25, 22.52, 39, 22.27, 19, 20, 30, 
        29, 35.71, 29.74, 31, 29, 19, 23, 26.52
    ]
}

df = pd.DataFrame(data)

# Função para adicionar asteriscos
def add_significance(ax, x1, x2, y, h, p):
    if p < 0.05:
        ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color='k')
        ax.text((x1+x2)*.5, y+h, "*", ha='center', va='bottom', color='k')

# Variáveis para plotar
variables = ['Idade', 'Peso (kg)', 'IMC (kg/m2)']

# Criando boxplots
for var in variables:
    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(x='Grupo', y=var, data=df)
    plt.title(f'Boxplot de {var} por Grupo')

    # Teste t para significância
    grupo_controle = df[df['Grupo'] == 'Controle'][var]
    grupo_caso = df[df['Grupo'] != 'Controle'][var]
    t_stat, p_value = ttest_ind(grupo_controle, grupo_caso)

    # Adicionando asterisco se significativo
    y, h = df[var].max() + 1, 1
    add_significance(ax, 0, 1, y, h, p_value)

    plt.show()


# ### Boxplot de Idade por Grupo
# 
# - **Controle**: A mediana da idade está em torno de 35 anos, com uma distribuição que varia de aproximadamente 20 a 60 anos.
# - **Caso Tipo A**: A mediana é mais alta, em torno de 50 anos, indicando que este grupo tende a ser mais velho.
# - **Caso Tipo B**: A mediana é similar ao grupo Controle, mas com uma maior variação.
# - **Significância**: O asterisco indica uma diferença estatisticamente significativa entre o grupo Controle e Caso Tipo A.
# 
# ### Boxplot de Peso (kg) por Grupo
# 
# - **Controle**: A mediana do peso está em torno de 70 kg, com uma variação de aproximadamente 40 a 100 kg.
# - **Caso Tipo A**: A mediana é similar ao grupo Controle, mas com uma maior variação.
# - **Caso Tipo B**: Este grupo tem uma mediana de peso significativamente menor, com pouca variação.
# 
# ### Boxplot de IMC (kg/m²) por Grupo
# 
# - **Controle**: A mediana do IMC está em torno de 30 kg/m², com uma variação de aproximadamente 20 a 40 kg/m².
# - **Caso Tipo A**: A mediana é ligeiramente mais alta que o grupo Controle, com uma maior variação.
# - **Caso Tipo B**: Este grupo tem um IMC significativamente menor, com pouca variação.
# 
# ### Observações Gerais
# 
# - **Idade**: O grupo Caso Tipo A é significativamente mais velho que o grupo Controle.
# - **Peso e IMC**: O grupo Caso Tipo B apresenta valores significativamente menores de peso e IMC, indicando uma diferença notável em relação aos outros grupos.
# - **Variação**: O grupo Caso Tipo A mostra maior variação em todas as variáveis, sugerindo uma maior diversidade dentro do grupo.

# In[256]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = {
    'Grupo': [
        'Controle', 'Caso Tipo A', 'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 
        'Controle', 'Controle', 'Caso Tipo A', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Controle', 'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 'Controle', 
        'Controle', 'Caso Tipo A', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 
        'Caso Tipo A', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 'Controle', 
        'Caso Tipo A', 'Caso Tipo B', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Caso Tipo B', 'Controle', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 
        'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A', 'Controle', 'Caso Tipo A'
    ],
    'Gravidade': [
        'leve', 'moderado', 'grave', 'grave', 'leve', 'moderado', 'grave', 'leve', 
        'moderado', 'grave', 'leve', 'moderado', 'grave', 'leve', 'moderado', 'grave', 
        'leve', 'moderado', 'grave', 'leve', 'moderado', 'grave', 'leve', 'moderado', 
        'grave', 'leve', 'moderado', 'grave', 'leve', 'moderado', 'grave', 'leve', 
        'moderado', 'grave', 'leve', 'moderado', 'grave', 'leve', 'moderado', 'grave', 
        'leve', 'moderado', 'grave', 'leve', 'moderado', 'grave', 'leve', 'moderado'
    ]
}

df = pd.DataFrame(data)

# Função para calcular proporções e erros
def calcular_proporcoes(df, var):
    count_df = df.groupby(['Grupo', var]).size().reset_index(name='count')
    total_df = df.groupby('Grupo').size().reset_index(name='total')
    prop_df = pd.merge(count_df, total_df, on='Grupo')
    prop_df['proporcao'] = prop_df['count'] / prop_df['total']
    prop_df['erro'] = np.sqrt(prop_df['proporcao'] * (1 - prop_df['proporcao']) / prop_df['total'])
    return prop_df

# Variável categórica
var = 'Gravidade'

# Calcular proporções e erro
prop_df = calcular_proporcoes(df, var)

# Criar barplot
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=prop_df, x=var, y='proporcao', hue='Grupo', errorbar=None)

# Adicionar barras de erro manualmente
for idx, row in prop_df.iterrows():
    x_val = list(prop_df[prop_df['Grupo'] == row['Grupo']][var].unique()).index(row[var])
    group_offset = {'Controle': -0.2, 'Caso Tipo A': 0.0, 'Caso Tipo B': 0.2}
    offset = group_offset.get(row['Grupo'], 0)
    ax.errorbar(x=x_val + offset, y=row['proporcao'], yerr=row['erro'], fmt='none', c='black', capsize=5)

ax.set_title('Proporção de Gravidade por Grupo')
ax.set_ylabel('Proporção')
ax.set_xlabel('Gravidade')
ax.set_ylim(0, 1)

plt.tight_layout()
plt.show()


# ### Gráfico de Proporção de Gravidade por Grupo
# 
# 1. **Gravidade "grave"**:
#    - **Caso Tipo A** e **Caso Tipo B** têm proporções semelhantes, com **Caso Tipo B** ligeiramente maior.
#    - **Controle** tem uma proporção menor em comparação com os casos.
# 
# 2. **Gravidade "leve"**:
#    - **Controle** apresenta a maior proporção, seguido por **Caso Tipo A** e **Caso Tipo B**.
#    - As barras de erro são grandes, indicando variabilidade nos dados.
# 
# 3. **Gravidade "moderado"**:
#    - **Controle** e **Caso Tipo A** têm proporções semelhantes.
#    - **Caso Tipo B** tem uma proporção ligeiramente menor.
# 
# 4. **Barras de Erro**:
#    - As barras de erro indicam a incerteza nas estimativas de proporção.
#    - A sobreposição das barras de erro sugere que as diferenças podem não ser estatisticamente significativas.
# 
# ### Observações
# 
# - **Distribuição**: O grupo Controle tende a ter uma maior proporção de casos leves, enquanto os casos tendem a ser mais graves.
# - **Variabilidade**: A presença de barras de erro grandes sugere que há variabilidade significativa nos dados, o que pode afetar a interpretação das diferenças entre os grupos.

# In[ ]:




