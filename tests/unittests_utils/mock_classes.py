from _tests.unittests_utils.expected_html import *
from _tests.unittests_utils.company_numbers import cns


class FakeRequests:

    def __init__(self):
        pass

    def get(self, url):
        if url == "https://find-and-update.company-information.service.gov.uk/company/00048839/officers?page=1":
            return FakeResponse(html=barclays_html_1)
        elif url == "https://find-and-update.company-information.service.gov.uk/company/00048839/officers?page=2":
            return FakeResponse(html=barclays_html_2)
        elif url == "https://find-and-update.company-information.service.gov.uk/company/00048839/officers?page=3":
            return FakeResponse(html=barclays_html_3)
        elif url == "https://find-and-update.company-information.service.gov.uk/company/FC030435/officers?page=1":
            return FakeResponse(html=company_as_officer)


class FakeResponse:

    def __init__(self, html):
        self.content = html


class FakeStorageClient:

    def __init__(self, project=None):
        self.project = project

    def list_blobs(self, bucket_or_name, prefix):
        if (bucket_or_name == "konnector") and (prefix == "ingress/2020-11-01/BasicCompanyData-"):
            return [FakeBlob(name="ingress/2020-11-01/BasicCompanyData-2020-11-01-part1_6.csv"),
                    FakeBlob(name="ingress/2020-11-01/BasicCompanyData-2020-11-01-part2_6.csv"),
                    FakeBlob(name="ingress/2020-11-01/BasicCompanyData-2020-11-01-part3_6.csv"),
                    FakeBlob(name="ingress/2020-11-01/BasicCompanyData-2020-11-01-part4_6.csv"),
                    FakeBlob(name="ingress/2020-11-01/BasicCompanyData-2020-11-01-part5_6.csv"),
                    FakeBlob(name="ingress/2020-11-01/BasicCompanyData-2020-11-01-part6_6.csv")]

    def bucket(self, bucket_name):
        return FakeBucket(name=bucket_name, client=self)


class FakeBucket:

    def __init__(self, client, name):
        self.client = client
        self.bucket = name

    def blob(self, name):
        return FakeBlob(name=name)


class FakeBlob:

    def __init__(self, name):
        self.name = name

    def upload_from_file(self, file):
        pass

    def upload_from_string(self, data):
        pass

    def download_to_file(self, file_obj):
        file_obj.write("\n".join(cns).encode())


class FakeBQClient:

    def __init__(self, project=None):
        self.project = project


class FakeDatetimeDatetime:

    def now(self):
        return FakeDatetimeObject()


class FakeDatetimeObject:

    def strftime(self, style):
        if style == "%Y-%m-":
            return "2020-11-"

