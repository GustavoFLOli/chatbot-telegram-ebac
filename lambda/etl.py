import os
import json
import logging
from datetime import datetime, timedelta, timezone

import boto3
import pyarrow as pa
import pyarrow.parquet as pq


def parse_data(data: dict) -> dict:
    """
    Função para transformar os dados JSON no formato esperado para PyArrow.
    """
    parsed_data = {}
    for key, value in data.items():
        if key == 'from':
            parsed_data.update({
                f"user_{k}": [v] for k, v in value.items() if k in ['id', 'is_bot', 'first_name']
            })
        elif key == 'chat':
            parsed_data.update({
                f"chat_{k}": [v] for k, v in value.items() if k in ['id', 'type']
            })
        elif key in ['message_id', 'date', 'text']:
            parsed_data[key] = [value]

    parsed_data.setdefault('text', [None])
    return parsed_data


def lambda_handler(event: dict, context: dict) -> bool:
    """
    Função Lambda que processa os arquivos JSON do bucket RAW, compacta os dados
    em um único arquivo Parquet e faz o upload para o bucket ENRICHED.
    """
    # Variáveis de ambiente e lógicas
    client = boto3.client('s3')
    RAW_BUCKET = os.environ['AWS_S3_BUCKET']
    ENRICHED_BUCKET = os.environ['AWS_S3_ENRICHED']
    tzinfo = timezone(offset=timedelta(hours=-3))
    date = (datetime.now(tzinfo) - timedelta(days=1)).strftime('%Y-%m-%d')
    timestamp = datetime.now(tzinfo).strftime('%Y%m%d%H%M%S%f')

    table = None

    try:
        # Listar arquivos no bucket RAW
        response = client.list_objects_v2(Bucket=RAW_BUCKET, Prefix=f'telegram/context_date={date}')
        for content in response.get('Contents', []):
            key = content['Key']
            file_path = f"/tmp/{key.split('/')[-1]}"

            # Baixar o arquivo JSON e processar
            client.download_file(RAW_BUCKET, key, file_path)
            with open(file_path, mode='r', encoding='utf8') as fp:
                try:
                    data = json.load(fp).get("message", {})
                except json.JSONDecodeError as e:
                    logging.error(f"Erro ao decodificar JSON no arquivo {key}: {str(e)}")
                    continue

            parsed_data = parse_data(data)
            if parsed_data:
                iter_table = pa.Table.from_pydict(parsed_data)
                table = pa.concat_tables([table, iter_table]) if table else iter_table

        if table:
            parquet_file_path = f'/tmp/{timestamp}.parquet'
            pq.write_table(table, parquet_file_path)
            client.upload_file(parquet_file_path, ENRICHED_BUCKET, f"telegram/context_date={date}/{timestamp}.parquet")
        else:
            logging.warning(f"Nenhum dado processado para a data {date}")

        return True
    except Exception as exc:
        logging.error(f"Erro inesperado: {exc}")
        return False
