from weasyprint import HTML

from python_downloader.general_download import GeneralPageDownloader
# from weasyprint import HTML
#
# # Convert an HTML file to a PDF
# HTML('your_page.html').write_pdf('output.pdf')
#
# # Or convert a string containing HTML
# html_content = "<h1>Hello, PDF!</h1><p>This is a sample PDF with WeasyPrint.</p>"
# HTML(string=html_content).write_pdf("output.pdf")


class StackoverflowPageDownload(GeneralPageDownloader):
    def write_pdf(self):
        print("writing PDF")
        soap = self.get_soap()
        print(repr(soap))
        HTML(string=str(soap)).write_pdf("test.pdf")
