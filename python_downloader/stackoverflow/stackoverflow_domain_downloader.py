import logging

from python_downloader.general_download import GeneralDomainDownloader
from python_downloader.stackoverflow.stackoverflow_page_downloader import StackoverflowPageDownload

from python_downloader.utils import URLInfo

logger = logging.getLogger(__name__)

class StackoverflowDomainDownloader(GeneralDomainDownloader):

    def download_page(self, page_to_download_file: URLInfo, page_to_download_url: str) -> None:
        logger.debug(f"Downloading page: {page_to_download_url}")
        page = StackoverflowPageDownload(page_to_download_file)
        logger.debug("download the HTML")
        page.download_html()
        logger.debug("Deal with IMGs")
        page.deal_with_tag_img()
        logger.debug("Deal with tag links")
        page.deal_with_tag_links()
        logger.debug("Deal with scripts")
        page.deal_with_scripts()
        logger.debug("Deal with the hyperlinks to the same domain")
        self.hyperlinks_in_domain.update(page.get_links_in_domain())
        logger.debug("Print the page")
        page.write_html()
        logger.debug("Write the PDF")
        page.write_pdf()
