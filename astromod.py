from json import dumps
from urllib.parse import quote_plus

import requests
import typer
from bs4 import BeautifulSoup

astromod = typer.Typer()

meta = {
    "mods": [],
    "urls": [],
    "isSearch": False
}
urls = []


class HTTPError(Exception):
    """When another HTTP code rather than 200 is recived"""

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"{self.message} (HTTP Code: {self.error_code})"


def main():
    r = requests.get("https://astromod.space/")
    urls.append("https://astromod.space/")
    soup = BeautifulSoup(r.content, "html.parser")
    if r.status_code == 200:
        mods = soup.find_all("a", {"class": "svelte-tlnnuh"})
        for mod in mods:
            # Fetch page
            url = f"https://astromod.space/{mod['href']}"
            rmod = requests.get(url)
            modsoup = BeautifulSoup(rmod.content, "html.parser")

            # Metadata variables
            name = modsoup.find("h1").decode_contents()
            creator = modsoup.find_all("span")[1].decode_contents()
            desc = modsoup.find("div", {"class": "description-container"}).decode_contents()
            modpage = f"https://astromod.space{mod['href']}"
            lastupdated = modsoup.find_all("span")[5].decode_contents()
            firstupload = modsoup.find_all("span")[7].decode_contents()
            downloads = modsoup.find_all("span")[9].decode_contents()
            tags = modsoup.find_all("span")[11].decode_contents()
            version = modsoup.find_all("span")[13].decode_contents()
            modlicense = modsoup.find_all("span")[15].decode_contents()
            modid = modsoup.find_all("span")[16].decode_contents()[7:]
            fileurl = "https://astromod.space" + modsoup.find_all("a")[3]["href"]
            print(fileurl)
            urls.append(fileurl)
            urls.append(modpage)

            # Download mod's file
            filename = None
            modfile = requests.get(fileurl, allow_redirects=False)
            if modfile.status_code == 307:
                filetemp = modfile.headers["Location"]
                filename = filetemp.split("/")[-1]
                modfile = requests.get("https://astromod.space" + filetemp).content
            else:
                filename = fileurl.split("/")[-1]

            # Save mod's file
            with open(filename, mode="wb") as file:
                file.write(modfile)

            # Add mod metadata to global file
            modmeta = {
                    "name": name,
                    "creator": creator,
                    "desc": desc,
                    "modpage": modpage,
                    "lastupdated": lastupdated,
                    "firstupload": firstupload,
                    "downloads": downloads,
                    "tags": tags,
                    "version": version,
                    "license": modlicense,
                    "modid": modid,
                    "fileurl": fileurl,
                    "filename": filename
                }
            meta["mods"].append(modmeta)
        meta["urls"] = urls
    else:
        match r.status_code:
            case 400:
                raise HTTPError("Bad Request", 400)
            case 404:
                raise HTTPError("Not Found", 404)
            case 403:
                raise HTTPError("Forbidden", 403)
            case _:
                raise HTTPError("Other Code", r.status_code)

    # Save metadata
    with open("metadata.json", "w") as f:
        f.write(dumps(meta))


@astromod.command()
def search(query: str):
    meta["isSearch"] = True
    safe_query = quote_plus(query)
    r = requests.get("https://astromod.space/search?name=" + safe_query)
    urls.append("https://astromod.space/search?name=" + safe_query)
    soup = BeautifulSoup(r.content, "html.parser")
    if r.status_code == 200:
        mods = soup.find_all("a", {"class": "svelte-tlnnuh"})
        for mod in mods:
            # Fetch page
            url = f"https://astromod.space/{mod['href']}"
            rmod = requests.get(url)
            modsoup = BeautifulSoup(rmod.content, "html.parser")

            # Metadata variables
            name = modsoup.find("h1").decode_contents()
            creator = modsoup.find_all("span")[1].decode_contents()
            desc = modsoup.find("div", {"class": "description-container"}).decode_contents()
            modpage = f"https://astromod.space{mod['href']}"
            lastupdated = modsoup.find_all("span")[5].decode_contents()
            firstupload = modsoup.find_all("span")[7].decode_contents()
            downloads = modsoup.find_all("span")[9].decode_contents()
            tags = modsoup.find_all("span")[11].decode_contents()
            version = modsoup.find_all("span")[13].decode_contents()
            modlicense = modsoup.find_all("span")[15].decode_contents()
            modid = modsoup.find_all("span")[16].decode_contents()[7:]
            fileurl = "https://astromod.space" + modsoup.find_all("a")[3]["href"]
            print(fileurl)
            urls.append(fileurl)
            urls.append(modpage)

            # Download mod's file
            filename = None
            modfile = requests.get(fileurl, allow_redirects=False)
            if modfile.status_code == 307:
                filetemp = modfile.headers["Location"]
                filename = filetemp.split("/")[-1]
                modfile = requests.get("https://astromod.space" + filetemp).content
            else:
                filename = fileurl.split("/")[-1]

            # Save mod's file
            with open(filename, mode="wb") as file:
                file.write(modfile)

            # Add mod metadata to global file
            modmeta = {
                "name": name,
                "creator": creator,
                "desc": desc,
                "modpage": modpage,
                "lastupdated": lastupdated,
                "firstupload": firstupload,
                "downloads": downloads,
                "tags": tags,
                "version": version,
                "license": modlicense,
                "modid": modid,
                "fileurl": fileurl,
                "filename": filename
            }
            meta["mods"].append(modmeta)
        meta["urls"] = urls
    else:
        match r.status_code:
            case 400:
                raise HTTPError("Bad Request", 400)
            case 404:
                raise HTTPError("Not Found", 404)
            case 403:
                raise HTTPError("Forbidden", 403)
            case _:
                raise HTTPError("Other Code", r.status_code)

    # Save metadata
    with open("metadata.json", "w") as f:
        f.write(dumps(meta))