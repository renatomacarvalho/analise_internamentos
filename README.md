# 🏥 Análise de Internações Hospitalares --- DATASUS

## 📌 Sobre o projeto

Este projeto tem como objetivo explorar dados públicos de internações
hospitalares do Sistema Único de Saúde (SUS), disponibilizados pelo
Departamento de Informação e Informática do SUS (DATASUS).

A proposta é desenvolver um fluxo de ingestão e tratamento de dados
utilizando Databricks, SQL, PySpark e Delta Lake, transformando arquivos
públicos em uma base estruturada para análises.

O projeto utiliza dados do **Sistema de Informações Hospitalares do SUS
(SIH/SUS)**, com foco inicial nos arquivos **RD --- AIH Reduzida**, por
local de internação.

> **Status:** em desenvolvimento. Os resultados, métricas e conclusões
> serão incluídos após a ingestão e validação dos dados.

## 🎯 Objetivos

-   Obter dados públicos de internações hospitalares na fonte oficial do
    DATASUS.
-   Construir uma pipeline de dados no Databricks.
-   Aplicar uma arquitetura de duas camadas: **Bronze** e **Silver**.
-   Preservar os dados brutos para permitir auditoria e reprocessamento.
-   Tratar e padronizar os dados com SQL e/ou PySpark.
-   Validar a qualidade dos dados antes de utilizá-los nas análises.
-   Criar consultas e indicadores que ajudem a compreender os padrões
    das internações hospitalares.
-   Documentar as decisões, limitações e resultados do projeto.

## 🗂️ Fonte dos dados

**Fonte:** DATASUS --- Ministério da Saúde\
**Sistema:** Sistema de Informações Hospitalares do SUS (SIH/SUS)\
**Arquivo:** RD --- AIH Reduzida\
**Recorte inicial:** Paraná (PR), começando pela competência janeiro de
2025\
**Expansão prevista:** outros meses, anos e unidades da Federação, após
validar o processo inicial.

Links oficiais:

-   [Produção Hospitalar ---
    SIH/SUS](https://datasus.saude.gov.br/acesso-a-informacao/producao-hospitalar-sih-sus/)
-   [Transferência de Arquivos do
    DATASUS](https://datasus.saude.gov.br/transferencia-de-arquivos2/)

### Por que utilizar dados por local de internação?

O recorte por local de internação considera a localização do
estabelecimento onde ocorreu a internação. Essa escolha é adequada para
explorar a distribuição da produção hospitalar por território.

A competência e as regras de contabilização devem ser consideradas na
interpretação dos resultados. Os registros administrativos de AIH não
devem ser tratados automaticamente como uma contagem perfeita de pessoas
únicas.

## 🧰 Tecnologias e ferramentas

-   **Databricks:** ambiente para desenvolvimento e processamento dos
    dados.
-   **Apache Spark / PySpark:** leitura, transformação e validação dos
    dados.
-   **SQL:** consultas exploratórias e construção de indicadores.
-   **Delta Lake:** armazenamento das tabelas em formato Delta.
-   **Git e GitHub:** versionamento do código e documentação.

As ferramentas serão utilizadas conforme a necessidade de cada etapa; o
projeto não depende de usar PySpark e SQL em todas as transformações.

## 🏗️ Arquitetura da solução

A pipeline utilizará duas camadas de dados. A camada Gold não será
criada nesta versão inicial: as análises serão realizadas diretamente
sobre a Silver por meio de consultas SQL.

``` text
        DATASUS — SIH/SUS
                 |
                 v
          Arquivos RD
                 |
                 v
        +----------------+
        |     BRONZE     |
        | Dados brutos   |
        | Delta Lake     |
        +----------------+
                 |
                 v
        +----------------+
        |     SILVER     |
        | Dados tratados |
        | Delta Lake     |
        +----------------+
                 |
                 v
        Consultas SQL
        Indicadores e análises
```

### 🥉 Bronze --- dados brutos

A Bronze será responsável por armazenar os dados de origem em uma
estrutura persistente no Databricks.

Princípios desta camada:

-   Preservar os valores e campos originais sempre que possível.
-   Registrar a origem e a competência do arquivo.
-   Evitar aplicar regras analíticas ou excluir registros sem
    documentação.
-   Permitir rastreabilidade e reprocessamento.
-   Utilizar Delta Lake para persistência, quando os dados já estiverem
    preparados para leitura e gravação nesse formato.

A forma de ingestão dependerá do formato disponibilizado pelo DATASUS.
Arquivos compactados ou em formato específico poderão exigir uma etapa
de extração ou conversão antes da gravação em Delta.

### 🥈 Silver --- dados tratados

A Silver será a camada de dados preparados para consultas e análises.

Transformações previstas:

-   Conferir o esquema e os tipos de dados.
-   Padronizar nomes de colunas, quando apropriado.
-   Tratar datas e campos numéricos.
-   Identificar valores nulos, inválidos e inconsistentes.
-   Verificar possíveis duplicidades, sem removê-las automaticamente sem
    entender a regra de negócio.
-   Validar códigos geográficos e demais códigos categóricos.
-   Documentar as regras aplicadas e as limitações encontradas.

Os campos e as transformações finais serão definidos após a inspeção do
arquivo real e do respectivo dicionário de dados. Nenhuma coluna será
presumida antes dessa validação.

## 📊 Perguntas de análise

Após validar os campos disponíveis, o projeto buscará responder a
perguntas como:

-   Como varia o volume de internações ao longo das competências?
-   Quais municípios ou estabelecimentos concentram maior volume, se
    essas dimensões estiverem disponíveis?
-   Como se distribuem as internações por estado ou região, conforme a
    abrangência dos arquivos carregados?
-   Qual é o valor aprovado associado às internações, caso o campo
    esteja disponível?
-   Qual é o tempo de permanência hospitalar, se for possível calculá-lo
    com os campos existentes?
-   Quais são as principais causas de internação, caso os códigos CID e
    uma tabela de referência adequada sejam incorporados?
-   Como os indicadores mudam entre períodos?

As perguntas serão refinadas de acordo com o conteúdo e a granularidade
efetiva dos dados.

## 📈 Indicadores planejados

Os indicadores abaixo são possibilidades a validar após a inspeção do
esquema:

-   Quantidade de registros/AIHs, com definição explícita do que está
    sendo contado.
-   Evolução mensal e anual.
-   Distribuição geográfica das internações.
-   Valores aprovados e valor médio, se disponível.
-   Permanência hospitalar média, se os campos permitirem um cálculo
    consistente.
-   Distribuição por causa de internação, caso a dimensão CID-10 seja
    incorporada.

**Importante:** quantidade de registros, quantidade de AIHs e quantidade
de pessoas não são necessariamente medidas equivalentes. Cada indicador
terá sua definição documentada.

## 🧪 Qualidade e validação dos dados

A qualidade será avaliada antes de publicar indicadores. As verificações
previstas incluem:

-   Quantidade de registros carregados.
-   Conferência das colunas e dos tipos de dados.
-   Identificação de valores nulos nos campos relevantes.
-   Verificação de datas e valores fora do esperado.
-   Análise de possíveis duplicidades.
-   Comparação de contagens entre origem e camadas, quando aplicável.
-   Registro das regras de tratamento e das limitações.

Os registros não serão excluídos apenas por apresentarem valores
incomuns: cada regra de limpeza deverá ter uma justificativa
documentada.

## 📁 Estrutura prevista do repositório

``` text
analise-internacoes-datasus/
├── README.md
├── notebooks/
│   ├── 01_ingestao_bronze.py
│   └── 02_tratamento_silver.py
├── queries/
│   ├── 01_exploracao_dados.sql
│   ├── 02_analise_temporal.sql
│   └── 03_analise_geografica.sql
└── docs/
    ├── dicionario_dados.md
    └── regras_de_tratamento.md
```

Esta é uma estrutura planejada. Os arquivos serão adicionados ao
repositório à medida que forem desenvolvidos; a organização poderá mudar
conforme as necessidades do projeto.

## 🚀 Etapas de desenvolvimento

1.  Selecionar e baixar um arquivo RD na página oficial do DATASUS.
2.  Verificar formato, conteúdo, tamanho e dicionário de dados.
3.  Preparar o arquivo para leitura no Databricks.
4.  Criar a tabela Delta da camada Bronze.
5.  Implementar o tratamento e as validações da Silver.
6.  Executar consultas exploratórias em SQL.
7.  Construir indicadores e documentar os resultados.
8.  Ampliar o período e a abrangência geográfica, se necessário.
9.  Publicar exemplos de consultas, resultados e conclusões no
    repositório.

## ⚠️ Limitações e cuidados de interpretação

-   O SIH/SUS reúne informações administrativas relacionadas às
    internações financiadas pelo SUS; não representa automaticamente
    todas as internações realizadas no país, inclusive as exclusivamente
    privadas.
-   O significado de cada campo depende do dicionário e das regras
    oficiais da base.
-   Registros de AIH não devem ser interpretados automaticamente como
    pessoas únicas.
-   Comparações temporais e geográficas precisam considerar competência,
    cobertura e possíveis mudanças nos dados.
-   Indicadores de saúde descrevem padrões observados e, isoladamente,
    não demonstram relações de causa e efeito.
-   Os resultados só serão apresentados após a execução e validação das
    consultas.

## 📌 Progresso do projeto

-   [x] Definição do tema e da fonte pública.
-   [x] Seleção inicial da base SIH/SUS --- RD.
-   [x] Definição da arquitetura com duas camadas: Bronze e Silver.
-   [ ] Download e validação do primeiro arquivo.
-   [ ] Inspeção do esquema e do dicionário de dados.
-   [ ] Ingestão da camada Bronze no Databricks.
-   [ ] Tratamento e validação da camada Silver.
-   [ ] Consultas SQL e indicadores.
-   [ ] Documentação dos resultados e limitações.
-   [ ] Ampliação do período de análise.

## 👤 Autor

Projeto de portfólio desenvolvido para praticar e demonstrar
conhecimentos em análise e processamento de dados com Databricks, SQL,
PySpark e Delta Lake.

-   **LinkedIn:** \[adicione aqui o link do seu perfil\]
-   **GitHub:** \[adicione aqui o link do seu perfil ou repositório\]

------------------------------------------------------------------------

*Projeto educacional com dados públicos. A documentação será atualizada
à medida que a implementação avançar.*
