import json
import boto3
from PIL import Image

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract the bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Download the image file from S3
    download_path = '/tmp/{}'.format(file_key)
    s3.download_file(bucket_name, file_key, download_path)
    
    # Open the image using Pillow
    image = Image.open(download_path)
    
    # Convert the image to PDF
    pdf_path = '/tmp/converted_{}.pdf'.format(file_key)
    image.save(pdf_path, 'PDF')

    # Upload the converted PDF back to S3
    output_key = 'converted/{}'.format(file_key.replace('.jpg', '.pdf'))
    s3.upload_file(pdf_path, bucket_name, output_key)

    return {
        'statusCode': 200,
        'body': json.dumps('File converted and uploaded to {}'.format(output_key))
    }
