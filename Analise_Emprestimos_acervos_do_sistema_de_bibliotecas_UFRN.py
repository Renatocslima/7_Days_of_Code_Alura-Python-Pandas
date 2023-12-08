import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

#Pegar dados
##Peguei o Último semestre disponivel que era quebrado diretamente 
##Os demais fiz o for para não ter que ficar pegando cada link
raw='https://raw.githubusercontent.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/main/Dia_1-Importando_dados/Datasets/dados_emprestimos/emprestimos-20201.csv'
emprestimos_biblioteca = pd.read_csv(raw)

for ano in range(2010,2020):
    for semestre in range(1,3):
        ref=str(ano)+str(semestre)
        raw=(f'https://raw.githubusercontent.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/main/Dia_1-Importando_dados/Datasets/dados_emprestimos/emprestimos-{ref}.csv')
        dados = pd.read_csv(raw)
        emprestimos_biblioteca=pd.concat([emprestimos_biblioteca,dados],ignore_index=True)
emprestimos_biblioteca

emprestimos_biblioteca = emprestimos_biblioteca.drop_duplicates()

#Pegar dados dos exemplares
#Em caso de erro com o read_parquet, instale o pyarrow 
dados_exemplares = pd.read_parquet('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_1-Importando_dados/Datasets/dados_exemplares.parquet')
dados_exemplares

#Juntando os dados de emprestimo com o dos exemplares
emprestimos_completos = pd.merge(emprestimos_biblioteca,dados_exemplares)
emprestimos_completos

#Tratando dados
emprestimos_completos.info()

emprestimos_completos = emprestimos_completos.drop('registro_sistema', axis=1)
emprestimos_completos['matricula_ou_siape'] = emprestimos_completos['matricula_ou_siape'].to_string("#########.0")
emprestimos_completos.info()

# Definição das condições da CDU
condicoes = [
    (emprestimos_completos['localizacao'] >= 900),
    (emprestimos_completos['localizacao'] >= 800) & (emprestimos_completos['localizacao'] < 900),
    (emprestimos_completos['localizacao'] >= 700) & (emprestimos_completos['localizacao'] < 800),
    (emprestimos_completos['localizacao'] >= 600) & (emprestimos_completos['localizacao'] < 700),
    (emprestimos_completos['localizacao'] >= 500) & (emprestimos_completos['localizacao'] < 600),
    (emprestimos_completos['localizacao'] >= 400) & (emprestimos_completos['localizacao'] < 500),
    (emprestimos_completos['localizacao'] >= 300) & (emprestimos_completos['localizacao'] < 400),
    (emprestimos_completos['localizacao'] >= 200) & (emprestimos_completos['localizacao'] < 300),
    (emprestimos_completos['localizacao'] >= 100) & (emprestimos_completos['localizacao'] < 200),
    (emprestimos_completos['localizacao'] < 100)
]

CDU = ['Geografia. Biografia. História', 'Linguagem. Língua. Linguística', 'Belas artes', 
       'Ciências aplicadas','Matemática e ciências naturais',
       'Classe vaga. Provisoriamente não ocupada.','Ciências sociais.','Religião.',
       'Filosofia e psicologia.','Generalidades. Ciência e conhecimento.']

# Aplicação das condições usando numpy.select()
emprestimos_completos['CDU'] = np.select(condicoes, CDU)
emprestimos_completos['data_emprestimo'] = pd.to_datetime(emprestimos_completos['data_emprestimo'])
emprestimos_completos['data_devolucao'] = pd.to_datetime(emprestimos_completos['data_devolucao'])
emprestimos_completos['data_renovacao'] = pd.to_datetime(emprestimos_completos['data_renovacao'])
emprestimos_completos.info()

#Quantidade de emprestimos e exemplares
emprestimos = len(emprestimos_completos)
emprestimos
exemplares = len(emprestimos_completos['id_emprestimo'].drop_duplicates())
exemplares

#Separação por DataTime
emprestimos_data = pd.DataFrame(emprestimos_completos['data_emprestimo'].value_counts()).reset_index()
emprestimos_data.columns = ['data','quantidade']
emprestimos_data['Ano'] = emprestimos_data['data'].dt.year
emprestimos_data['Mês'] = emprestimos_data['data'].dt.month
emprestimos_data['Dia'] = emprestimos_data['data'].dt.day
emprestimos_data['Hora'] = emprestimos_data['data'].dt.hour
emprestimos_data

#Quantidade de exemplares emprestados por ano
emprestimos_por_ano = emprestimos_data[['Ano','quantidade']].groupby(['Ano']).sum()
emprestimos_por_ano

emprestimos_por_ano.plot(kind='line',color="blue", linestyle="-", marker="", linewidth=3, markersize=8)
plt.title("Quantidade de exemplares emprestados do SISBI por ano"+"\n",weight='bold')
plt.grid(True)
plt.show()
#Adicionar comentarios sobre os resultados

#Quantos foram por cada mês?
emprestimos_por_mes = emprestimos_data[['Mês','quantidade']].groupby(['Mês']).sum()
meses = {1:'Jan',2:'Fev',3:'Mar',4:'Abr',
                    5:'Mai',6:'Jun',7:'Jul',8:'Ago',
                    9:'Set',10:'Out',11:'Nov',12:'Dez'}
emprestimos_por_mes.index = emprestimos_por_mes.index.map(meses)
emprestimos_por_mes

emprestimos_por_mes.plot(kind='line',color="blue", linestyle="-", marker=".", linewidth=3, markersize=12)
plt.title("Quantidade de exemplares emprestados do SISBI por mes"+"\n",weight='bold')
plt.grid(True)
plt.show()
#Adicionar comentarios

#Qual é a quantidade de empréstimos por hora ao longo do dia ?
emprestimos_por_hora = emprestimos_data[['Hora','quantidade']].groupby(['Hora']).sum()
emprestimos_por_hora

emprestimos_por_hora.plot(kind='bar')
plt.title("Quantidade de exemplares emprestados do SISBI por horario"+"\n",weight='bold')
plt.show()
#Adicionar comentarios

#-----------------------------------------------------------------------------------------------------------------------
#Categorização
emprestimos_completos.tipo_vinculo_usuario.unique()
emprestimos_completos.colecao.unique()
emprestimos_completos.biblioteca.unique()
emprestimos_completos.CDU.unique()

def frequencia(variavel):
  dataframe = pd.DataFrame(emprestimos_completos[variavel].value_counts())                      
  dataframe.columns = ['quantidade']
  dataframe['percentual'] = round((dataframe.quantidade / dataframe.quantidade.sum())*100,1)

  return dataframe

frequencia('tipo_vinculo_usuario')
frequencia('colecao')
frequencia('biblioteca')
frequencia('CDU')

aluno_graduacao = emprestimos_completos.query('tipo_vinculo_usuario == "ALUNO DE GRADUAÇÃO"')
aluno_graduacao.colecao.value_counts()

aluno_graduacao_acervo_circulante = aluno_graduacao.query('colecao == "Acervo Circulante"')
aluno_graduacao_acervo_circulante = pd.DataFrame(aluno_graduacao_acervo_circulante)
aluno_graduacao_acervo_circulante['data_emprestimo'] = pd.to_datetime(aluno_graduacao_acervo_circulante['data_emprestimo'])
aluno_graduacao_acervo_circulante['ano'] = aluno_graduacao_acervo_circulante['data_emprestimo'].dt.year
aluno_graduacao_acervo_circulante['mes'] = aluno_graduacao_acervo_circulante['data_emprestimo'].dt.month
aluno_graduacao_acervo_circulante = aluno_graduacao_acervo_circulante.loc[:,['ano','mes']]
aluno_graduacao_acervo_circulante = aluno_graduacao_acervo_circulante.value_counts().to_frame('quantidade').reset_index()
aluno_graduacao_acervo_circulante

def gera_box_plot(dataset,x,y,titulo,subtitulo):
  '''
  Esta função irá gerar um gráfico

  Dataset = conjunto de dados do gráfico
  x = valor do eixo x do gráfico
  y = valor do eixo y do gráfico
  título = título do gráfico
  subtitulo = subtitulo do texto
  '''

  sns.set_theme(style="darkgrid", palette="Blues", font_scale=1.3)                    
  plt.figure(figsize=(16,10))                                                           

  ax = sns.boxplot(y=y, x=x, data=dataset, palette="Blues")                                           
  ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',').replace(',','.')))                


  plt.ylim(0,max(dataset[y])*1.1) #Definir o limite do eixo y
  plt.xlabel(None)                                                                     
  plt.ylabel(None)                                                                    

  ax.set_title(titulo+"\n",size=20,loc='left',weight='bold')
  ax.text(s=subtitulo,x=-0.5,y=max(dataset[y])*1.11,fontsize=18, ha='left',color='gray')  
     
gera_box_plot(aluno_graduacao_acervo_circulante,'ano','quantidade','Distribuição dos empréstimos mensais', 'Realizados pelos alunos de graduação no acervo circulante')

alunos_pos_graduacao = emprestimos_completos.query('tipo_vinculo_usuario == "ALUNO DE PÓS-GRADUAÇÃO"')
alunos_pos_graduacao.colecao.value_counts()    

alunos_pos_graduacao_acervo_circulante = alunos_pos_graduacao.query('colecao == "Acervo Circulante"')
alunos_pos_graduacao_acervo_circulante = pd.DataFrame(alunos_pos_graduacao_acervo_circulante)
alunos_pos_graduacao_acervo_circulante['data_emprestimo'] = pd.to_datetime(alunos_pos_graduacao_acervo_circulante['data_emprestimo'])
alunos_pos_graduacao_acervo_circulante['ano'] = alunos_pos_graduacao_acervo_circulante['data_emprestimo'].dt.year
alunos_pos_graduacao_acervo_circulante['mes'] = alunos_pos_graduacao_acervo_circulante['data_emprestimo'].dt.month
alunos_pos_graduacao_acervo_circulante = alunos_pos_graduacao_acervo_circulante.loc[:,['ano','mes']]
alunos_pos_graduacao_acervo_circulante = alunos_pos_graduacao_acervo_circulante.value_counts().to_frame('quantidade').reset_index()
alunos_pos_graduacao_acervo_circulante

gera_box_plot(alunos_pos_graduacao_acervo_circulante,'ano','quantidade','Distribuição dos empréstimos mensais', 'Realizados pelos alunos de pós graduação no acervo circulante')
     
cadastro_usuarios_antes_2010 = pd.read_excel('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_6-Novos_dados_novas_analises/Datasets/matricula_alunos.xlsx',
                                        sheet_name='Até 2010',skiprows=1)
cadastro_usuarios_depois_2010 = pd.read_excel('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_6-Novos_dados_novas_analises/Datasets/matricula_alunos.xlsx',
                                        sheet_name='Após 2010',skiprows=1)

cadastro_usuarios_antes_2010
cadastro_usuarios_antes_2010.columns = ['matricula_ou_siape','tipo_vinculo_usuario','curso']
cadastro_usuarios_depois_2010
cadastro_usuarios_depois_2010.columns= ['matricula_ou_siape','tipo_vinculo_usuario','curso']
cadastro_usuarios_excel = pd.concat([cadastro_usuarios_antes_2010,cadastro_usuarios_depois_2010],ignore_index=True)
cadastro_usuarios_excel.matricula_ou_siape = cadastro_usuarios_excel.matricula_ou_siape.astype('string')
cadastro_usuarios_excel

cadastro_usuarios_json = pd.read_json('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_6-Novos_dados_novas_analises/Datasets/cadastro_alunos.json')
cadastro_usuarios_json


cadastro_usuarios_graduacao_json = pd.read_json(cadastro_usuarios_json.registros[0])
cadastro_usuarios_graduacao_json
cadastro_usuarios_graduacao_json.matricula_ou_siape = cadastro_usuarios_graduacao_json.matricula_ou_siape.astype('float')
cadastro_usuarios_graduacao_json.matricula_ou_siape = cadastro_usuarios_graduacao_json.matricula_ou_siape.astype('string')

cadastro_usuarios_cursos = pd.concat([cadastro_usuarios_excel,cadastro_usuarios_graduacao_json],ignore_index=True)
cadastro_usuarios_cursos

matricula_data_de_emprestimo = emprestimos_completos.query("tipo_vinculo_usuario == 'ALUNO DE GRADUAÇÃO'")
matricula_data_de_emprestimo = matricula_data_de_emprestimo.loc[:,['matricula_ou_siape','data_emprestimo']]
matricula_data_de_emprestimo = matricula_data_de_emprestimo.query('data_emprestimo > 2015')
matricula_data_de_emprestimo = matricula_data_de_emprestimo.reset_index(drop=True)
matricula_data_de_emprestimo

matricula_data_de_emprestimo.isna().sum()

matricula_data_de_emprestimo = matricula_data_de_emprestimo.dropna()

matricula_data_de_emprestimo['matricula_ou_siape'] = matricula_data_de_emprestimo['matricula_ou_siape'].astype('string')
matricula_data_de_emprestimo

cadastro_usuarios_cursos_selecionados = cadastro_usuarios_cursos.query("curso == ['BIBLIOTECONOMIA','CIÊNCIAS SOCIAIS','COMUNICAÇÃO SOCIAL','DIREITO','FILOSOFIA','PEDAGOGIA']")
cadastro_usuarios_cursos_selecionados

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

cadastro_usuarios_cursos_selecionados_pv = pd.merge(matricula_data_de_emprestimo,cadastro_usuarios_cursos_selecionados,how='inner',on='matricula_ou_siape')
cadastro_usuarios_cursos_selecionados_pv
cadastro_usuarios_cursos_selecionados_pv['data_emprestimo'] = cadastro_usuarios_cursos_selecionados_pv["data_emprestimo"].dt.year
emprestimos_cursos_selecionados = cadastro_usuarios_cursos_selecionados_pv.iloc[:,[1,3]].value_counts().reset_index()
emprestimos_cursos_selecionados.columns = ['ANO','CURSO','QUANTIDADE_EMPRESTIMOS']
emprestimos_cursos_selecionados

emprestimos_tipo_usuario_curso_pivot = emprestimos_cursos_selecionados.pivot_table(
        index = 'CURSO',
        columns = 'ANO',
        values = 'QUANTIDADE_EMPRESTIMOS',
        fill_value = '-',
        aggfunc= sum,
        margins = True,
        margins_name = 'TOTAL',
)
emprestimos_tipo_usuario_curso_pivot

cadastro_usuarios_antes_2010 = pd.read_excel('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_6-Novos_dados_novas_analises/Datasets/matricula_alunos.xlsx',
                                        sheet_name='Até 2010',skiprows=1)
cadastro_usuarios_depois_2010 = pd.read_excel('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_6-Novos_dados_novas_analises/Datasets/matricula_alunos.xlsx',
                                        sheet_name='Após 2010',skiprows=1)
cadastro_usuarios_antes_2010

cadastro_usuarios_antes_2010.columns = ['matricula_ou_siape','tipo_vinculo_usuario','curso']
cadastro_usuarios_depois_2010
cadastro_usuarios_depois_2010.columns= ['matricula_ou_siape','tipo_vinculo_usuario','curso']
cadastro_usuarios_excel = pd.concat([cadastro_usuarios_antes_2010,cadastro_usuarios_depois_2010],ignore_index=True)
cadastro_usuarios_excel.matricula_ou_siape = cadastro_usuarios_excel.matricula_ou_siape.astype('string')
cadastro_usuarios_excel

cadastro_usuarios_json = pd.read_json('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_6-Novos_dados_novas_analises/Datasets/cadastro_alunos.json')
cadastro_usuarios_json

cadastro_usuarios_posgraduacao_json = pd.read_json(cadastro_usuarios_json.registros[1])
cadastro_usuarios_posgraduacao_json
cadastro_usuarios_posgraduacao_json.info()

cadastro_usuarios_posgraduacao_json.matricula_ou_siape = cadastro_usuarios_posgraduacao_json.matricula_ou_siape.astype('float')
cadastro_usuarios_posgraduacao_json.matricula_ou_siape = cadastro_usuarios_posgraduacao_json.matricula_ou_siape.astype('string')
cadastro_usuarios_posgraduacao_json.info()

cadastro_usuarios_cursos = pd.concat([cadastro_usuarios_excel,cadastro_usuarios_posgraduacao_json],ignore_index=True)
cadastro_usuarios_cursos

cadastro_usuarios_cursos_pos_graduacao = cadastro_usuarios_posgraduacao_json.query("tipo_vinculo_usuario == 'ALUNO DE PÓS-GRADUAÇÃO'")
cadastro_usuarios_cursos_pos_graduacao


matricula_data_de_emprestimo_pos_graduacao = emprestimos_completos.loc[:,['matricula_ou_siape','data_emprestimo']]
matricula_data_de_emprestimo_pos_graduacao = matricula_data_de_emprestimo_pos_graduacao.query('data_emprestimo > 2017')
matricula_data_de_emprestimo_pos_graduacao = matricula_data_de_emprestimo_pos_graduacao.reset_index(drop=True)
matricula_data_de_emprestimo_pos_graduacao

emprestimos_pos_graduacao_desde_2017 = matricula_data_de_emprestimo_pos_graduacao.merge(cadastro_usuarios_cursos_pos_graduacao)
emprestimos_pos_graduacao_desde_2017

emprestimos_pos_graduacao_desde_2017.data_emprestimo = emprestimos_pos_graduacao_desde_2017.data_emprestimo.dt.year
emprestimos_pos_graduacao_desde_2017 = emprestimos_pos_graduacao_desde_2017.iloc[:,[1,3]].value_counts().reset_index()
emprestimos_pos_graduacao_desde_2017.columns = ['ANO','CURSO','QUANTIDADE_EMPRESTIMOS']
emprestimos_pos_graduacao_desde_2017.head()

emprestimos_pos_graduacao_e_curso_pivot = emprestimos_pos_graduacao_desde_2017.pivot_table(
        index = 'CURSO',
        columns = 'ANO',
        values = 'QUANTIDADE_EMPRESTIMOS'
)
emprestimos_pos_graduacao_e_curso_pivot

previsao_2022 = pd.read_table('https://github.com/FranciscoFoz/7_Days_of_Code_Alura-Python-Pandas/raw/main/Dia_7-Apresentando_resultados_em_HTML/Dataset/previsao')
previsao_2022 = previsao_2022['curso previsao_2022'].str.split(' ',expand=True)
previsao_2022

previsao_2022.index = emprestimos_pos_graduacao_e_curso_pivot.index
emprestimos_pos_graduacao_e_curso_pivot['2022'] = previsao_2022.iloc[:,1]
emprestimos_pos_graduacao_e_curso_pivot

emprestimos_pos_graduacao_e_curso_pivot['2022'] = emprestimos_pos_graduacao_e_curso_pivot['2022'].astype('int')
emprestimos_pos_graduacao_e_curso_pivot

def diferenca_percentual_ano_anterior(x,y):
  return round(((x / y * 100) - 100),2)

percentual_2018 = diferenca_percentual_ano_anterior(emprestimos_pos_graduacao_e_curso_pivot.iloc[:,1],emprestimos_pos_graduacao_e_curso_pivot.iloc[:,0])
percentual_2019 = diferenca_percentual_ano_anterior(emprestimos_pos_graduacao_e_curso_pivot.iloc[:,2],emprestimos_pos_graduacao_e_curso_pivot.iloc[:,1])
percentual_2022 = diferenca_percentual_ano_anterior(emprestimos_pos_graduacao_e_curso_pivot.iloc[:,3],emprestimos_pos_graduacao_e_curso_pivot.iloc[:,2])
percentual = pd.DataFrame({'2018':percentual_2018,
                           '2019':percentual_2019,
                           '2022':percentual_2022})
percentual

percentual.reset_index(inplace=True)
percentual.columns = percentual.columns.str.capitalize()
percentual.Curso = percentual.Curso.str.capitalize()
percentual

th_props = [
  ('font-size', '1.4rem'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', 'whitesmoke'),
  ('background-color', '#001692'),
  ('border-radius', '0.25rem'),
  ('box-shadow','0 0 1rem gray')
  ]
td_props = [
  ('font-size', '1rem'),
  ('padding','0.5rem'),
  ('text-align', 'left'),
  ('font-weight', 'bold'),
  ('border-bottom','0.1rem solid lightgray')
  ]
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]

percentual.style.text_gradient(cmap='RdYlGn',low=1, axis=1,vmax=0.1,vmin=0)\
                              .format('{:.2f} %',subset=['2018','2019','2022'])\
                              .set_table_styles(styles)\
                              .to_html('tabela_front.html',doctype_html =True,
                                       table_attributes='ALIGN=LEFT WIDTH=50% CELLSPACING = 5')