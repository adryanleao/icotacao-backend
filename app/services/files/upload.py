import json

import requests

from config import Config
from werkzeug.utils import secure_filename


def upload_file3(image, aws_key, filename=0):
    if filename == 0:
        filename = secure_filename(image.filename)

    path = "{}/original/{}".format(aws_key, filename)

    api_endpoint = 'https://api.kraken.io/v1/upload'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    }
    files = {
        'file': image
    }
    params = {
        "auth": {
            "api_key": "cb65bbe68cd9b4b1f32f9a3f4fbfa10d",
            "api_secret": "c46556c41826746e381090974aac27c93e2a6d01"
        },
        "s3_store": {
            "key": Config.AWS_ACCESS_KEY_ID,
            "secret": Config.AWS_SECRET_ACCESS_KEY,
            "bucket": Config.AWS_BUCKET,
            "region": Config.AWS_BUCKET_LOCATION
        },
        "wait": True,
        "resize": [
            {
                "id": "original",
                "strategy": "none",
                "storage_path": path.lower()
            },
            {
                "id": "small",
                "strategy": "auto",
                "width": 180,
                "height": 180,
                "storage_path": path.replace('original', 'small').lower()
            },
            {
                "id": "medium",
                "strategy": "auto",
                "width": 450,
                "height": 450,
                "storage_path": path.replace('original', 'medium').lower()
            },
            {
                "id": "large",
                "strategy": "auto",
                "width": 850,
                "height": 850,
                "storage_path": path.replace('original', 'large').lower()
            }
        ]
    }

    r = requests.post(url=api_endpoint, headers=headers, files=files, data={
        'data': json.dumps(params)
    })

    r_json = r.json()
    success = r_json['success']

    if success:
        r_json['image_key'] = path.lower()
        return r_json
