# 🏥 Análise de Dados Hospitalares — DATASUS

## 📌 Sobre o projeto

Este projeto tem como objetivo explorar dados públicos do Sistema Único de Saúde (SUS), disponibilizados pelo Departamento de Informação e Informática do SUS (DATASUS), utilizando o Databricks e SQL.

A análise utiliza inicialmente o arquivo `SPPR2501`, referente ao Paraná (PR), competência janeiro de 2025, com registros do tipo **SP — Serviços Profissionais**, associado ao sistema SIH/SUS.

O projeto busca explorar os dados, identificar padrões, construir indicadores e documentar as etapas de análise, respeitando a estrutura e as limitações da fonte original.

**Status:** primeira versão em desenvolvimento, com leitura dos arquivos CSV, criação de views e consultas exploratórias implementadas.

## 🎯 Objetivos

- Explorar dados públicos do DATASUS.
- Utilizar o Databricks para leitura e análise dos arquivos.
- Criar views SQL para facilitar a consulta dos dados.
- Investigar a distribuição dos registros por período e município.
- Identificar os códigos de procedimentos mais frequentes.
- Explorar os campos disponíveis para construir novos indicadores.
- Documentar as consultas, os resultados e as limitações da análise.
- Evoluir o projeto gradualmente, conforme a validação dos dados.

## 🗂️ Fonte dos dados

- **Fonte:** DATASUS — Ministério da Saúde.
- **Sistema:** Sistema de Informações Hospitalares do SUS (SIH/SUS).
- **Arquivo de origem:** `SPPR2501.dbc`, convertido para CSV para leitura no Databricks.
- **Tipo de registro:** SP — Serviços Profissionais.
- **Abrangência inicial:** Paraná (PR).
- **Competência:** janeiro de 2025.

Links oficiais:

- [Produção Hospitalar — SIH/SUS](https://datasus.saude.gov.br/acesso-a-informacao/producao-hospitalar-sih-sus/)
- [Transferência de Arquivos do DATASUS](https://datasus.saude.gov.br/transferencia-de-arquivos2/)

### Sobre o arquivo analisado

O arquivo utilizado nesta versão contém campos como `SP_PROCREA`, `SP_QT_PROC`, `SP_CIDPRI`, `SP_M_HOSP` e `SP_M_PAC`.

A identificação do arquivo como SP é importante para interpretar corretamente os resultados. **Os registros de Serviços Profissionais não devem ser tratados automaticamente como internações únicas**, pois a granularidade do arquivo precisa ser considerada em cada indicador.

## 🧰 Tecnologias e ferramentas

- **Databricks:** ambiente de desenvolvimento e execução das consultas.
- **SQL:** leitura, agregação e análise exploratória dos dados.
- **Apache Spark:** mecanismo de processamento utilizado pelo Databricks.
- **CSV:** formato dos arquivos utilizados na leitura atual.
- **Git e GitHub:** versionamento do código e documentação do projeto.

Nesta primeira versão, a leitura dos dados é feita com `read_files`, e as consultas utilizam views SQL. A implementação de transformações com PySpark, persistência em Delta Lake e camadas de dados poderá ser considerada em etapas futuras.

## 🔄 Fluxo atual de processamento

O fluxo implementado nesta versão é:

```text
         Arquivos DATASUS
                |
                v
       Conversão para CSV
                |
                v
        Databricks Volume
                |
                v
       Leitura com read_files
                |
          +-----+------+
          |            |
          v            v
    View sppr2501   View municipios
          |            |
          +-----+------+
                |
                v
          Consultas SQL
                |
                v
      Indicadores e análises
```

### Views utilizadas

**`workspace.default.sppr2501`**

View criada a partir do arquivo `SPPR2501.csv`, utilizando leitura com cabeçalho e inferência de esquema.

**`workspace.default.municipios`**

View criada a partir do arquivo `RELATORIO_DTB_BRASIL_MUNICIPIO.csv`, utilizado como referência para análises geográficas.

As views facilitam a consulta dos dados, mas não representam, por si só, tabelas persistidas em Delta Lake.

## 📊 Análises implementadas

### 1. Quantidade geral de registros

Consulta utilizada para identificar o volume total de linhas no arquivo:

```sql
SELECT COUNT(*) AS quantidade_registros
FROM workspace.default.sppr2501;
```

**Resultado:** 1.214.393 registros.

Essa métrica representa a quantidade de linhas do arquivo analisado, não necessariamente o número de internações únicas, pessoas ou procedimentos realizados.

### 2. Distribuição por dia da semana

Análise da distribuição dos registros conforme o dia da semana associado ao campo `SP_DTINTER`.

O objetivo é observar como os registros se distribuem entre os dias da semana.

A interpretação depende da confirmação do significado do campo no layout oficial e da validade das datas.

### 3. Distribuição geográfica por município

Análise dos municípios associados ao campo `SP_M_HOSP`, utilizando a tabela de referência municipal.

O objetivo é identificar os municípios com maior quantidade de registros no arquivo.

A associação entre os códigos municipais deve considerar o formato dos códigos, eventuais zeros à esquerda e a correspondência com a tabela de referência.

### 4. Códigos de procedimentos por quantidade registrada

Análise dos dez códigos do campo `SP_PROCREA` com maior soma dos valores registrados em `SP_QT_PROC`.

Consulta utilizada:

```sql
SELECT
    SP_PROCREA AS codigo_procedimento,
    SUM(TRY_CAST(SP_QT_PROC AS DOUBLE))
        AS quantidade_procedimentos
FROM workspace.default.sppr2501
WHERE SP_PROCREA IS NOT NULL
GROUP BY SP_PROCREA
ORDER BY quantidade_procedimentos DESC
LIMIT 10;
```

Os dez códigos com maior soma na consulta executada foram:

| Código do procedimento | Quantidade registrada |
|---|---:|
| `0303010037` | 226.664 |
| `0303140151` | 133.292 |
| `0303060212` | 96.429 |
| `0303040149` | 79.182 |
| `0415010012` | 78.972 |
| `0304100021` | 65.538 |
| `0415020034` | 49.094 |
| `0303070102` | 44.150 |
| `0415040035` | 44.103 |
| `0303170190` | 43.992 |

O resultado permite comparar os códigos com maior quantidade registrada no campo analisado.

**Limitação:** os códigos ainda não estão associados às respectivas descrições textuais. Além disso, a interpretação da soma como quantidade efetiva de procedimentos depende da confirmação da definição oficial de `SP_QT_PROC`.

## 🧪 Verificações realizadas

Foi executada uma consulta exploratória para avaliar o preenchimento e a distribuição numérica do campo `SP_QT_PROC`.

| Indicador | Resultado |
|---|---:|
| Total de registros | 1.214.393 |
| Registros com quantidade preenchida | 1.214.393 |
| Valores nulos ou inválidos após conversão | 0 |
| Menor valor | 0 |
| Maior valor | 609 |
| Soma dos valores | 2.590.836 |

Essas verificações ajudam a compreender o conteúdo do campo e a identificar possíveis problemas de preenchimento.

A ausência de valores nulos ou inválidos após a conversão não garante, isoladamente, que todos os valores sejam semanticamente corretos. A interpretação definitiva depende do dicionário oficial e das regras da fonte.

## 📚 Dicionário preliminar de dados

A tabela abaixo reúne os principais campos utilizados ou considerados nas análises. As descrições devem ser conferidas com o layout oficial do arquivo antes de serem tratadas como definitivas.

| Campo | Uso ou significado preliminar |
|---|---|
| `SP_GESTOR` | Código relacionado ao gestor responsável pelo registro |
| `SP_UF` | Código da unidade da Federação |
| `SP_AA` | Campo de ano do arquivo |
| `SP_MM` | Campo de mês do arquivo |
| `SP_CNES` | Código associado ao estabelecimento de saúde |
| `SP_NAIH` | Número relacionado à AIH |
| `SP_PROCREA` | Código de procedimento utilizado no registro |
| `SP_DTINTER` | Campo de data associado à internação |
| `SP_DTSAIDA` | Campo de data associado à saída |
| `SP_M_HOSP` | Código de município associado ao hospital |
| `SP_M_PAC` | Código de município associado ao paciente |
| `SP_CIDPRI` | Código CID principal informado no registro |
| `SP_CIDSEC` | Código CID secundário informado no registro |
| `SP_QT_PROC` | Campo numérico utilizado na análise de quantidade, pendente de confirmação documental |
| `SP_VALATO` | Campo de valor associado ao ato profissional, pendente de confirmação da regra de cálculo |
| `SP_QTD_ATO` | Campo relacionado à quantidade de atos, pendente de confirmação documental |
| `_rescued_data` | Campo utilizado pelo mecanismo de leitura do Spark para dados que não se ajustam ao esquema esperado |

Os demais campos serão documentados à medida que forem necessários às análises e suas definições forem verificadas.

## ⚠️ Limitações e cuidados de interpretação

- A análise inicial utiliza um arquivo e uma competência específicos, não representando automaticamente todo o histórico do SUS.
- Os registros do arquivo SP não devem ser interpretados automaticamente como internações únicas ou pessoas únicas.
- A contagem de linhas e a soma de um campo de quantidade são métricas diferentes.
- O significado dos campos e as regras de contabilização devem ser confirmados no layout oficial.
- As análises geográficas dependem da correspondência correta entre os códigos municipais e a tabela de referência.
- Os códigos de procedimentos ainda não possuem descrições textuais associadas nesta versão.
- A leitura por meio de views não equivale à implementação de uma arquitetura de armazenamento em camadas.
- Os resultados descrevem os dados observados e, isoladamente, não demonstram relações de causa e efeito.

## 🚀 Próximas etapas

- [x] Seleção do arquivo inicial do DATASUS.
- [x] Conversão do arquivo para CSV.
- [x] Leitura dos arquivos no Databricks.
- [x] Criação das views `sppr2501` e `municipios`.
- [x] Consulta da quantidade geral de registros.
- [x] Análise exploratória por dia da semana.
- [x] Consulta de registros por município.
- [x] Ranking de códigos por soma de `SP_QT_PROC`.
- [x] Verificação inicial do preenchimento de `SP_QT_PROC`.
- [ ] Confirmar as definições dos campos no layout oficial.
- [ ] Validar o relacionamento com a tabela de municípios.
- [ ] Associar códigos CID e procedimentos às respectivas descrições, quando aplicável.
- [ ] Ampliar as análises e documentar novos resultados.
- [ ] Avaliar a implementação de tratamento com PySpark e persistência em Delta Lake.
- [ ] Considerar a expansão para outras competências e unidades da Federação.

## 👤 Autor

Projeto de portfólio desenvolvido para praticar e demonstrar conhecimentos em análise exploratória de dados, SQL e Databricks, utilizando dados públicos do DATASUS.

- **LinkedIn:** https://linkedin.com/in/renatomcarvalho
- **GitHub:** https://github.com/renatomacarvalho

---

*Projeto educacional com dados públicos. O código, as análises e a documentação serão aprimorados conforme a validação das informações e a evolução do projeto.*