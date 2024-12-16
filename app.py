import sys

from python_downloader.python_downloader import PythonDownloader

if __name__ == "__main__":
    argv: list[str] = sys.argv[1:]
    download_domain = PythonDownloader(argv)
    download_domain.run()
