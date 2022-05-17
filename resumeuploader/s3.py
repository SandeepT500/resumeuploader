import os
from resumeuploader import settings
import boto3
def upload_doc_to_s3_bucket(doc_path, bucket, key):
    print("Uploading", doc_path)
    path1 = '/Users/rentsher/Desktop/resumeuploaderdj-master'
    basepath = path1 + doc_path
    print(basepath)
    if bucket == settings.AWS_STORAGE_BUCKET_NAME:
            s3_client = boto3.client('s3',
                                     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                     )

            s3_client.upload_file(basepath, bucket, key)
            region = s3_client.get_bucket_location(Bucket=bucket)['LocationConstraint']
            url = 'https://{0}.s3.{1}.amazonaws.com/{2}'.format(bucket, region, key)
            print(url)
            return url

