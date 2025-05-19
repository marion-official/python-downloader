from python_downloader.general_download import GeneralPageDownloader


from weasyprint import HTML

class StackoverflowPageDownload(GeneralPageDownloader):
    def write_pdf(self):
        print("writing PDF")
        soap = self.get_soap()
        print(repr(soap))
        file_name = self.url_info.get_local_url(extension='pdf')
        print(file_name)
        HTML(string=str(soap)).write_pdf(file_name)
