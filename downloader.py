import re
import subprocess
import platform
import os
import requests
from bs4 import BeautifulSoup
import config
import lib
import urllib.parse
import urllib3
import utils
import time
from datetime import datetime


class Downloader:

    def __init__(self):
        self.base_url = config.BASE_URL
        self.music_path_prefix = config.MUSIC_PATH_PREFIX
        self.download_domain = config.DOWNLOAD_DOMAIN
        self.endpoint = config.ENDPOINT
        self.query_params = config.QUERY_PARAMS
        self.request_timeout = config.REQUEST_TIMEOUT
        self.download_timeout = config.DOWNLOAD_TIMEOUT

    def shutdown_system(self, delay_minutes=0):
        system_name = platform.system()

        if system_name == "Windows":
            delay_minutes = delay_minutes * 60
            subprocess.run(
                ["shutdown", "/s", "/t", str(delay_minutes)], check=False)
        elif system_name == "Linux" or system_name == "Darwin":
            if delay_minutes == 0:
                subprocess.run(["shutdown", "-h", "now"], check=False)
            else:
                subprocess.run(
                    ["shutdown", "-h", f"+{delay_minutes}"], check=False)
        else:
            raise OSError(config.LOG_SHUTDOWN_ERROR.format(system_name))

    def cancel_shutdown(self):
        system_name = platform.system()

        if system_name == "Windows":
            os.system("shutdown /a")
        elif system_name in ("Linux", "Darwin"):
            os.system("shutdown -c")
        else:
            raise OSError(config.LOG_SHUTDOWN_ERROR.format(system_name))

    def _should_disable_ssl_verification(self, url):
        try:
            hostname = (urllib.parse.urlparse(url).hostname or "").lower()
            return hostname == "irolive.ir" or hostname.endswith(".irolive.ir")
        except Exception:
            return False

    def _get_html_web(self, url, query_params=None, page_count=None, log=print):
        if query_params is not None:
            query_params['page'] = page_count

        try:
            response = requests.get(
                url, params=query_params, timeout=self.request_timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            log(e)
            return None

    def _extraction_url_musics(self, html_soup):

        links, names = [], []
        for a in html_soup.find_all("a", href=True):
            href = a.get("href")
            if (
                href
                and isinstance(href, str)
                and href.startswith(self.music_path_prefix)
                and href != self.music_path_prefix
            ):
                links.append(f"{self.base_url}{href}")
                names.append(href)

        return links, names

    def _extraction_link_download(self, html_soup):

        link_download = []
        link = ""
        genre = "Unknown"

        for a in html_soup.find_all("a", href=True):
            href = a.get("href")

            if href and href.startswith(self.download_domain):
                link = href

            if href and href.startswith("/genre/"):
                genre = href.replace("/genre/", "")

        if link:
            link_download.append([link, genre])

        return link_download

    def download_one(self, link_download, name_music, genre, path_download,  log=print):
        temp_path = None

        try:
            name_music = name_music.replace(
                self.music_path_prefix, "").replace("-", " ")
            name_music = utils.sanitize_filename(name_music)

            log(config.LOG_DOWNLOADING.format(name_music))

            verify_ssl = not self._should_disable_ssl_verification(
                link_download)

            if not verify_ssl:
                urllib3.disable_warnings(
                    urllib3.exceptions.InsecureRequestWarning)

            response = requests.get(
                link_download, stream=True, timeout=self.download_timeout, verify=verify_ssl)

            response.raise_for_status()

            name_music = utils.sanitize_filename(name_music)

            genre = genre.strip().upper()
            folder_map = {
                "RAPHIP-HOP": path_download["rap_path"],
                "POP": path_download["pop_path"],
                "REMIX": path_download["remix_path"],
            }
            target_folder = folder_map.get(
                genre, path_download["other_path"])

            os.makedirs(target_folder, exist_ok=True)

            name_music = utils.sanitize_filename(name_music)
            file_path = os.path.join(target_folder, f"{name_music}.mp3")
            temp_path = f"{file_path}.part"

            total_size = int(response.headers.get("Content-Length", 0))

            downloaded_size = 0

            with open(temp_path, "wb") as mp3:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        mp3.write(chunk)
                        downloaded_size += len(chunk)

            if total_size and downloaded_size != total_size:
                raise IOError(
                    f"Incomplete download: "
                    f"{downloaded_size}/{total_size} bytes"
                )

            os.replace(temp_path, file_path)

            now = datetime.now()

            lib.add_record(
                name_music,
                genre,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S")
            )

            log(config.LOG_DOWNLOAD_SUCCESS.format(name_music))

            return True

        except requests.RequestException as error:
            log(config.LOG_ERROR_DOWNLOAD.format(name_music, error))
            return False

        except IOError as error:
            log(config.LOG_ERROR_DOWNLOAD.format(name_music, error))
            return False

        except Exception as error:
            log(config.LOG_ERROR_DOWNLOAD.format(name_music, error))
            return False

        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def find_musics(self, page_count, log=print):

        all_links, all_names = [], []

        log(config.LOG_READING_PAGE.format(page_count))
        html_soup = self._get_html_web(
            f"{self.base_url}{self.endpoint}", self.query_params, page_count
        )

        if html_soup is None:
            log(config.LOG_PAGE_NOT_FOUND.format(page_count))
            return None, None

        links, names = self._extraction_url_musics(html_soup)
        all_links.extend(links)
        all_names.extend(names)

        return all_links, all_names

    def _pause(self, is_paused):
        while is_paused():
            time.sleep(0.5)

    def download_all(self, page_count, adr_folder, progress, log=print, is_paused=lambda: False,):
        utils.save_json(config.JSON_PATH, adr_folder)
        dict_path = utils.set_address(config.JSON_PATH)
        for page in range(1, page_count + 1):
            all_links, all_names = self.find_musics(page, log)

            if all_links is None or all_names is None:
                continue

            total = len(all_links)
            if total == 0:
                log(config.LOG_MUSIC_NOT_FOUND)
                return

            log(config.LOG_DOWNLOADING_MUSIC.format(total))

            for index, (url, name) in enumerate(
                zip(all_links, all_names), start=1
            ):
                if is_paused():
                    log(config.LOG_DOWNLOAD_PAUSSED)
                    self._pause(is_paused)

                html_soup = self._get_html_web(url)

                if html_soup is None:
                    log(config.LOG_PAGE_MUSIC_NOT_FOUND)
                    progress(index / total)
                    continue

                links = self._extraction_link_download(html_soup)

                if links:
                    link = links[0][0]
                    genre = links[0][1]

                    name = (
                        name.replace(self.music_path_prefix, "")
                        .replace("-", " ")
                    )

                    if not lib.find_record(name):
                        self.download_one(
                            link,
                            name,
                            genre,
                            dict_path,
                            log
                        )
                    else:
                        log(config.LOG_DUPLICATE_MUSIC.format(name))

                progress(index / total)
