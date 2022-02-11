__AUTHOR__ = "Soumil Shah "

try:
    import time
    import json
    import httplib2
    import io
    import boto3
    import datetime
    from faker import Faker
    import uuid
    import re
    import os
    from apiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import shutil
except Exception as e:
    print("Error : {}".format(e))


class Settings(object):
    def __init__(self):
        self.__API_KEY = "AIzaSyDekaPCaUmlgMGW5xqaoLgjgjNwHMTnnZ4"
        self.AWS_ACCESS_KEY = "AKIA2Q647PV4XC4UAYNK"
        self.AWS_SECRET_KEY = "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"
        self.AWS_REGION_NAME = "us-east-2"
        self.s3bucket_name = "avicennajelal"

    @property
    def API_KEY(self):
        return self.__API_KEY

    @API_KEY.setter
    def API_KEY(self, value):
        self.__API_KEY = value


class GoogleDrive(Settings):
    def __init__(self):

        Settings.__init__(self)
        self.service = build("drive", "v3", developerKey=self.API_KEY)

    def get_files(self, folder_id=""):

        if folder_id == "":
            return "Folder ID cannot be None"

        else:
            param = {
                "q": "'"
                + folder_id
                + "' in parents and mimeType != 'application/vnd.google-apps.folder'"
            }
            return [
                file
                for file in self.service.files().list(**param).execute().get("files")
            ]

    def download_file(self, file_id, mime_type="", file_name=""):

        request = self.service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        fh.seek(0)

        with open(file_name, "wb") as f:
            shutil.copyfileobj(fh, f, length=131072)
        return True


class Datetime(object):
    @staticmethod
    def get_year_month_day():
        """
        Return Year month and day
        :return: str str str
        """
        dt = datetime.datetime.now()
        year = dt.year
        month = dt.month
        day = dt.day
        return year, month, day


class AWSS3(Settings):

    """Helper class to which add functionality on top of boto3"""

    def __init__(self, bucket=None, **kwargs):
        Settings.__init__(self)

        self.BucketName = self.s3bucket_name

        self.client = boto3.client("s3",
                                   aws_access_key_id=self.AWS_ACCESS_KEY,
                                   aws_secret_access_key=self.AWS_SECRET_KEY,
            region_name=self.AWS_REGION_NAME
        )

    def put_files(self, Response=None, Key=None, over_ride=True):
        """
        Put the File on S3
        :return: Bool
        """
        try:
            if over_ride:
                Response = bytes(json.dumps(Response).encode("UTF-8"))

            response = self.client.put_object(
                ACL="private", Body=Response, Bucket=self.BucketName, Key=Key
            )
            return "ok"
        except Exception as e:
            print("Error : {} ".format(e))
            return "error"

    def item_exists(self, Key):
        """Given key check if the items exists on AWS S3"""
        try:
            response_new = self.client.get_object(Bucket=self.BucketName, Key=str(Key))
            return True
        except Exception as e:
            return False

    def get_item(self, Key):

        """Gets the Bytes Data from AWS S3"""

        try:
            response_new = self.client.get_object(Bucket=self.BucketName, Key=str(Key))
            return response_new["Body"].read()
        except Exception as e:
            return False

    def find_one_update(self, data=None, key=None):

        """
        This checks if Key is on S3 if it is return the data from s3
        else store on s3 and return it
        """

        flag = self.item_exists(Key=key)

        if flag:
            data = self.get_item(Key=key)
            return data

        else:
            self.put_files(Key=key, Response=data)
            return data

    def delete_object(self, Key):

        response = self.client.delete_object(Bucket=self.BucketName, Key=Key,)
        return response

    def get_all_keys(self, Prefix=""):

        """
        :param Prefix: Prefix string
        :return: Keys List
        """
        try:
            paginator = self.client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.BucketName, Prefix=Prefix)

            tmp = []

            for page in pages:
                for obj in page["Contents"]:
                    tmp.append(obj["Key"])

            return tmp
        except Exception as e:
            return []

    def print_tree(self):
        keys = self.get_all_keys()
        for key in keys:
            print(key)
        return None

    def find_one_similar_key(self, searchTerm=""):
        keys = self.get_all_keys()
        return [key for key in keys if re.search(searchTerm, key)]

    def __repr__(self):
        return "AWS S3 Helper class "


class Datalake(AWSS3):

    def __init__(self, base_folder):
        self.base_folder = base_folder
        AWSS3.__init__(self)

    def upload_json_data_lake(self, json_data, year="", month="", day=""):

        if year != "" and month != "" and day != "":

            """base_folder/YYYY/MM/DD"""

            file_name = "{}_{}_{}_{}.json".format(
                year, month, day, uuid.uuid4().__str__()
            )

            path = "{}/year={}/month={}/day={}/{}".format(
                self.base_folder, year, month, day, file_name
            )

            self.put_files(Response=json_data, Key=path)

        else:

            year, month, day = Datetime.get_year_month_day()

            """base_folder/YYYY/MM/DD"""

            file_name = "{}_{}_{}_{}.json".format(
                year, month, day, uuid.uuid4().__str__()
            )

            path = "{}/year={}/month={}/day={}/{}".format(
                self.base_folder, year, month, day, file_name
            )

            self.put_files(Response=json_data, Key=path)

        return True

    def upload_raw_data_lake(self, data, year="", month="", day="", file_extension=''):

        if year != "" and month != "" and day != "":

            """base_folder/YYYY/MM/DD"""

            file_name = "{}_{}_{}_{}.{}".format(
                year, month, day, uuid.uuid4().__str__(), file_extension
            )

            path = "{}/year={}/month={}/day={}/{}".format(
                self.base_folder, year, month, day, file_name
            )

            self.put_files(Response=data, Key=path, over_ride=False)

        else:

            year, month, day = Datetime.get_year_month_day()

            """base_folder/YYYY/MM/DD"""

            file_name = "{}_{}_{}_{}.{}".format(
                year, month, day, uuid.uuid4().__str__(), file_extension
            )

            path = "{}/year={}/month={}/day={}/{}".format(
                self.base_folder, year, month, day, file_name
            )

            self.put_files(Response=data, Key=path, over_ride=False)

        return True


if __name__ == "__main__":

    helper = GoogleDrive()
    files = helper.get_files(folder_id="1f4R4KNvIR3QhEmTMac9kvSCKIMCjywsh")
    
    for file in files:
        time.sleep(5)
        helper.download_file(
            file_id=file.get("id"),
            mime_type=file.get("mimeType"),
            file_name=file.get("name"),
        )

        helper_data_lake  = Datalake(base_folder='googleDriveFiles')

        full_file_path = os.path.join(os.getcwd(), file.get("name"))
        file_extension = file.get("name").split(".")[1]
        print('1')
        with open(full_file_path, "rb") as f:
            blob_data = f.read()
            helper_data_lake.upload_raw_data_lake(data=blob_data, file_extension=file_extension)

        try:os.remove(full_file_path)
        except Exception as e:pass


