# Chatbot Telegram - Projeto de análise de dados

Este projeto visa analisar interações de usuários com um chatbot no Telegram utilizando AWS Lambda, AWS Athena e SQL. O objetivo é processar as mensagens dos usuários, aplicar transformações e gerar insights sobre as interações.

## Arquitetura do sistema

Abaixo, apresentamos um diagrama ilustrando a arquitetura do sistema:

![Arquitetura do sistema](images/arquitetura.png)

### Fluxo do sistema

- **Ingestão de dados**: As mensagens do Telegram são capturadas por um bot utilizando a API do Telegram e enviadas para um serviço Lambda, onde são processadas e armazenadas em um bucket do S3.
- **ETL**: Os dados brutos no S3 são extraídos e transformados pela função Lambda em um formato organizado para análise.
- **Apresentação**: O AWS Athena é utilizado para consultar os dados transformados, utilizando queries SQL, e gerar resultados para visualização.

## Estrutura do repositório

- **/lambda**: Contém os códigos Python para as funções do AWS Lambda, incluindo as etapas de ingestão e ETL.
- **/athena**: Contém as consultas SQL utilizadas no AWS Athena para a análise e apresentação dos dados.
- **/images**: Armazena as imagens utilizadas na documentação do projeto.
- **/results**: Contém arquivos CSV gerados a partir das consultas SQL realizadas no AWS Athena. Estes arquivos servem como exemplos dos resultados que podem ser gerados pelas queries.

## Como executar o projeto

### Etapa 1: Ingestão de dados
- As funções de ingestão do Lambda capturam mensagens do Telegram e as armazenam em um bucket do S3. O código da função `ingestao.py` está localizado em `/lambda/ingestao.py`.

### Etapa 2: Transformação e armazenamento
- O código de transformação dos dados, localizado em `/lambda/etl.py`, processa as mensagens armazenadas no S3 e as prepara para consultas no AWS Athena.

### Etapa 3: Análise e apresentação
- As consultas SQL são realizadas no AWS Athena para apresentar os dados analisados. As queries podem ser visualizadas no arquivo `/athena/sql_queries.sql`.

### Resultados gerados
- O diretório **`/results`** contém arquivos CSV que representam exemplos de resultados gerados a partir de algumas das consultas SQL realizadas no AWS Athena. Esses arquivos podem ser usados como referência para entender como os dados são apresentados após o processamento.

## Contribuições

Se você deseja contribuir para o projeto, por favor, envie um pull request com suas alterações.

