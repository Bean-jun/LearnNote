from datetime import datetime

from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from sts.sts import Sts


def create_bucket(bucket, region="ap-shanghai"):
    """创建桶"""
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)
    client.create_bucket(
        Bucket=bucket,
        ACL="public-read"  # private  /  public-read / public-read-write
    )
    # 创建桶时，设置cors规则，避免跨域问题
    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config
    )


def upload_file(bucket, image_obj, region):
    """文件上传"""
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)

    # 图片名称
    file_end = image_obj.name.rsplit('.')[-1]
    key = '{}.{}'.format(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), file_end)

    client.upload_file_from_buffer(Bucket=bucket,
                                   Key=key,
                                   Body=image_obj)

    return f'https://{bucket}.cos.{region}.myqcloud.com/{key}'


def delete_file(bucket, key, region):
    """文件删除"""
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)

    client.delete_object(Bucket=bucket,
                         Key=key)


def delete_file_list(bucket, key_list, region):
    """文件批量删除"""
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)

    objects = {
        "Quiet": "true",
        "Object": key_list
    }
    client.delete_objects(Bucket=bucket,
                          Delete=objects)


def credentials(bucket, region="ap-shanghai"):
    """获取临时凭证"""
    config = {
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': settings.TENCENT_SECRET_ID,
        # 固定密钥
        'secret_key': settings.TENCENT_SECRET_KEY,
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': region,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            # 'name/cos:PutObject',
            # 'name/cos:PostObject',
            # 分片上传
            # 'name/cos:InitiateMultipartUpload',
            # 'name/cos:ListMultipartUploads',
            # 'name/cos:ListParts',
            # 'name/cos:UploadPart',
            # 'name/cos:CompleteMultipartUpload'
            '*',
        ],

    }

    sts = Sts(config)
    response = sts.get_credential()
    return response


def delete_bucket(bucket, region):
    """删除桶"""
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)

    # 处理桶中的文件
    while True:
        # 找到桶中的文件
        part_objs = client.list_objects(bucket)

        # 查询还有多少文件
        contents = part_objs.get('Contents')
        if not contents:
            break
        # 批量删除
        objects = {
            "Quiet": "true",
            "Object": [{"Key": item["Key"]} for item in contents]
        }
        client.delete_objects(bucket, objects)

    # 处理桶中的碎片
    while True:
        # 找到桶中的碎片
        part_upload = client.list_multipart_uploads(bucket)

        uploads = part_upload.get('Upload')

        if not uploads:
            break

        for item in uploads:
            client.abort_multipart_upload(bucket, item['Key'], item['UploadId'])

    # 删除桶
    client.delete_bucket(bucket)
