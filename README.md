# 🏥 Análise de Internações Hospitalares — DATASUS

## 📌 Sobre o projeto
Este projeto tem como objetivo explorar dados públicos de internações hospitalares do Sistema Único de Saúde (SUS), disponibilizados pelo Departamento de Informação e Informática do SUS (DATASUS).

A proposta é desenvolver um fluxo de ingestão e tratamento de dados utilizando Databricks, SQL, PySpark e Delta Lake, transformando arquivos públicos em uma base estruturada para análises.

O projeto utiliza dados do **Sistema de Informações Hospitalares do SUS (SIH/SUS)**, com foco inicial nos arquivos **RD — AIH Reduzida** e nos arquivos complementares de **SP — Serviços Profissionais**, por local de internação.

> **Status:** em desenvolvimento. Os resultados, métricas e conclusões serão incluídos após a ingestão e validação dos dados.

## 🎯 Objetivos
- Obter dados públicos de internações hospitalares na fonte oficial do DATASUS.
- Construir uma pipeline de dados no Databricks.
- Aplicar uma arquitetura de duas camadas: **Bronze** e **Silver**.
- Preservar os dados brutos para permitir auditoria e reprocessamento.
- Tratar e padronizar os dados com SQL e/ou PySpark.
- Validar a qualidade dos dados antes de utilizá-los nas análises.
- Criar consultas e indicadores que ajudem a compreender os padrões das internações hospitalares.
- Documentar as decisões, limitações e resultados do projeto.

## 🗂️ Fonte dos dados
**Fonte:** DATASUS — Ministério da Saúde  
**Sistema:** Sistema de Informações Hospitalares do SUS (SIH/SUS)  
**Recorte inicial:** Paraná (PR), começando pela competência janeiro de 2025  
**Expansão prevista:** outros meses, anos e unidades da Federação, após validar o processo inicial.

Links oficiais:
- [Produção Hospitalar — SIH/SUS](https://datasus.saude.gov.br/acesso-a-informacao/producao-hospitalar-sih-sus/)
- [Transferência de Arquivos do DATASUS](https://datasus.saude.gov.br/transferencia-de-arquivos/)

### Por que utilizar dados por local de internação?
O recorte por local de internação considera a localização do estabelecimento onde ocorreu a internação. Essa escolha é adequada para explorar a distribuição da produção hospitalar por território.

A competência e as regras de contabilização devem ser consideradas na interpretação dos resultados. Os registros administrativos de AIH não devem ser tratados automaticamente como uma contagem perfeita de pessoas únicas.

## 📘 Dicionário de Dados (Arquivos SP - Serviços Profissionais)
Os arquivos do tipo **SP** contêm o detalhamento de cada procedimento e honorário médico realizado dentro de uma internação. Abaixo estão listados os principais campos mapeados nesta estrutura de dados:

| Nome da Coluna | Significado Técnico / Descrição | Tipo / Exemplo |
| :--- | :--- | :--- |
| **SP_GESTOR** | Código do Gestor de Saúde responsável pela validação (`410000` = Paraná) | Alfanumérico |
| **SP_UF** | Unidade da Federação onde ocorreu a internação (`41` = Paraná) | Inteiro |
| **SP_AA** | Ano de processamento do dado no sistema (`2025`) | Inteiro |
| **SP_MM** | Mês de processamento do dado no sistema (`01` = Janeiro) | Alfanumérico |
| **SP_CNES** | Cadastro Nacional de Estabelecimentos de Saúde (Código único do hospital) | Alfanumérico |
| **SP_NAIH** | Número da AIH (Código identificador único daquela internação) | Alfanumérico |
| **SP_PROCREA** | Código do procedimento principal unificado do SUS que gerou a internação | Alfanumérico |
| **SP_DTINTER** | Data de entrada / internação do paciente (Formato AAAAMMDD) | Data |
| **SP_DTSAIDA** | Data de saída / alta do paciente (Formato AAAAMMDD) | Data |
| **SP_ATOPROF** | Código do ato profissional específico realizado pelo especialista ou equipe | Alfanumérico |
| **SP_QTD_ATO** | Quantidade de atos profissionais executados dentro do mesmo registro | Inteiro |
| **SP_VALATO** | Valor monetário pago especificamente por aquele ato profissional (R$) | Decimal |
| **SP_PTSP** | Pontuação do Serviço Profissional para regras internas de cálculo do SUS | Inteiro |
| **SP_M_HOSP** | Código IBGE do Município de localização do Hospital (`411125` = Irati) | Inteiro |
| **SP_M_PAC** | Código IBGE do Município de residência habitual do Paciente | Inteiro |
| **SP_COMPLEX** | Nível de complexidade do procedimento (`02` = Média Complexidade) | Alfanumérico |
| **SP_FINANC** | Tipo de bloco de financiamento federal (`06` = Bloco MAC) | Alfanumérico |
| **SP_PF_CBO** | Código da ocupação (CBO) do profissional de saúde (`225125` = Clínico) | Alfanumérico |
| **SP_PF_DOC** | Documento de identificação do profissional (CNS criptografado/mascarado) | Alfanumérico |
| **SP_PJ_DOC** | CNPJ da instituição ou hospital associado ao ato médico | Alfanumérico |
| **IN_TP_VAL** | Indicador do tipo de valor (`1` = Serviço Hospitalar, `2` = Serviço Profissional) | Inteiro |
| **SP_CIDPRI** | Diagnóstico Principal codificado segundo a classificação CID-10 | Alfanumérico |
| **SP_CIDSEC** | Diagnóstico Secundário (comorbidades ou causas associadas) | Alfanumérico |
| **REMESSA** | Nome do arquivo bruto original gerado pelo DATASUS (`.DTS`) | Alfanumérico |
| **_rescued_data** | Coluna técnica gerada no Spark para capturar dados corrompidos | Estrutura |

## 🧰 Tecnologias e ferramentas
- **Databricks:** ambiente para desenvolvimento e processamento dos dados.
- **Apache Spark / PySpark:** leitura, transformação e validação dos dados.
- **SQL:** consultas exploratórias e construção de indicadores.
- **Delta Lake:** armazenamento das tabelas em formato Delta.
- **Git e GitHub:** versionamento do código e documentação.

As ferramentas serão utilizadas conforme a necessidade de cada etapa; o projeto não depende de usar PySpark e SQL em todas as transformações.

## 🏗️ Arquitetura da solução
A pipeline utilizará duas camadas de dados. A camada Gold não será criada nesta versão inicial: as análises serão realizadas diretamente sobre a Silver por meio de consultas SQL.

```text
        DATASUS — SIH/SUS
                 |
                 v
          Arquivos RD / SP
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

### 🥉 Bronze — dados brutos
A Bronze será responsável por armazenar os dados de origem em uma estrutura persistente no Databricks.

Princípios desta camada:
- Preservar os valores e campos originais sempre que possível.
- Registrar a origem e a competência do arquivo.
- Evitar aplicar regras analíticas ou excluir registros sem documentação.
- Permitir rastreabilidade e reprocessamento.
- Utilizar Delta Lake para persistência, quando os dados já estiverem preparados para leitura e gravação nesse formato.

A forma de ingestão dependerá do formato disponibilizado pelo DATASUS. Arquivos compactados em formato `.dbc` exigirão uma etapa prévia de conversão/extração (usando ferramentas ou bibliotecas como `PySUS`) antes da gravação estável em Delta.

### 🥈 Silver — dados tratados
A Silver será a camada de dados preparados para consultas e análises.

Transformações previstas:
- Conferir o esquema e os tipos de dados (converter strings de datas para o formato adequado).
- Padronizar nomes de colunas, quando apropriado.
- Tratar datas e campos numéricos (como a conversão de `SP_VALATO` para tipo decimal).
- Identificar valores nulos, inválidos e inconsistentes.
- Verificar possíveis duplicidades, sem removê-las automaticamente sem entender a regra de negócio.
- Validar códigos geográficos (IBGE) e demais códigos categóricos.
- Documentar as regras aplicadas e as limitações encontradas.

## 📊 Perguntas de análise
Após validar os campos disponíveis, o projeto buscará responder a perguntas como:
- Como varia o volume de internações ao longo das competências?
- Quais municípios ou estabelecimentos concentram maior volume de internações e procedimentos?
- Como se distribuem os custos de atos profissionais por especialidade médica (CBO)?
- Qual é o valor total aprovado e o custo médio dos procedimentos executados?
- Quais são as principais causas de internação hospitalar mapeadas pelo código CID-10 principal?
- Como os indicadores mudam entre períodos?

## 📈 Indicadores planejados
Os indicadores abaixo são possibilidades a validar após a inspeção do esquema:
- **Quantidade de AIHs processadas:** Volume total de faturamento por período.
- **Gasto com Serviços Profissionais (SP):** Somatório dos valores pagos por atos médicos.
- **Distribuição epidemiológica:** Rank das principais patologias encontradas no campo `SP_CIDPRI`.
- **Concentração Regional:** Análise volumétrica utilizando os códigos do município do hospital (`SP_M_HOSP`).

## 🧪 Qualidade e validação dos dados
A qualidade será avaliada antes de publicar indicadores. Verificações previstas:
- Quantidade de registros carregados.
- Conferência das colunas e dos tipos de dados.
- Identificação de valores nulos nos campos relevantes.
- Verificação de datas e valores fora do esperado.
- Análise de possíveis duplicidades.
- Comparação de contagens entre origem e camadas, quando aplicável.
- Registro das regras de tratamento e das limitações.

## 📁 Estrutura prevista do repositório
```text
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

## 🚀 Etapas de desenvolvimento
1. Selecionar e baixar os arquivos brutos (`.dbc`) diretamente na página oficial de transferência de arquivos do DATASUS.
2. Converter ou ler os arquivos estruturando-os no Databricks com o suporte de bibliotecas de ecossistema Python de saúde pública.
3. Criar e persistir as tabelas Delta na camada Bronze.
4. Aplicar o pipeline de limpeza, parseamento de tipos e enriquecimento para popular a camada Silver.
5. Desenvolver cadernos de análise e queries SQL para a consolidação dos indicadores de saúde definidos.