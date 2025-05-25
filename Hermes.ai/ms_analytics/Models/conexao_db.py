import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

bucket_name = 'bucket-ms-upload'
arquivo_s3 = 'Challenge_TOTVS_2025_MassaDados_v1/clientes_desde.csv'

# Baixar o arquivo do S3 em memória
obj = s3.get_object(Bucket=bucket_name, Key=arquivo_s3)
data = obj['Body'].read()

# Ler o conteúdo com pandas (exemplo CSV)
df = pd.read_csv(BytesIO(data),delimiter=";")

print(df.head())
