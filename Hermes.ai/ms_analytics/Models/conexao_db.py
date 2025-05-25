import boto3
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (credenciais e configs)
load_dotenv()

# Cria o cliente do S3 usando boto3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)


def listar_arquivos(bucket_name):
    """
    Lista os arquivos no bucket S3
    """
    response = s3.list_objects_v2(Bucket=bucket_name)
    arquivos = [obj['Key'] for obj in response.get('Contents', [])]
    return arquivos


def baixar_arquivo(bucket_name, file_key):
    """
    Baixa um arquivo específico do S3 e retorna como bytes
    """
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return obj['Body'].read()
