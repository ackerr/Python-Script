import os
import re
import sys

import requests
import qiniu


class Qiniu:

    ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')
    SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')
    BUCKET_KEY = os.environ.get('QINIU_BUCKET_KEY')
    BASE_URL = os.environ.get('QINIU_BASE_URL')

    def get_qiniu_token(self, file_name, bucket_name=BUCKET_KEY):
        client = qiniu.Auth(access_key=self.ACCESS_KEY, secret_key=self.SECRET_KEY)
        token = client.upload_token(bucket=bucket_name, key=file_name, expires=5 * 60)
        return token

    @staticmethod
    def download_file(image_url, file_name):
        """ download file from url"""
        response = requests.get(image_url, timeout=4)
        path = os.path.dirname(os.path.abspath(__file__)) + '/{}.jpg'.format(file_name or 'image')
        with open(path, 'wb') as f:
            f.write(response.content)
        return path

    def upload_file(self, local_file_path, file_name):
        """ upload file to qiniu """
        file_name = file_name or os.path.basename(local_file_path)
        token = self.get_qiniu_token(file_name)
        _, message = qiniu.put_file(token, file_name, local_file_path)
        if message.status_code != 200:
            raise Exception(f'upload error \n {message.exception}')
        return f'{self.BASE_URL}/{file_name}'

    def main(self, path, image_name):
        if re.match('((http|ftp|https)://)([a-zA-Z0-9.-]*)', path):
            path = self.download_file(path, image_name)
        return self.upload_file(path, image_name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('请输入文件路径')
    name = sys.argv[2] if len(sys.argv) > 2 else None
    print(Qiniu().main(sys.argv[1], name))
