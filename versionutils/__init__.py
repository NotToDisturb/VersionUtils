import json
import time

import schedule
import urllib.request

CURRENT_VERSION = {}
CURRENT_MANIFEST = ""
LAST_MANIFEST = ""
URL = "https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json"


def get_versions():
    response = urllib.request.urlopen(URL)
    versions_raw = response.read().decode("utf-8")
    return json.loads(versions_raw)


def __process_version(version: dict):
    return {
        "manifest": version["id"],
        "version_number": version["build_info"]["version"],
        "client_version": version["build_info"]["client_version"],
        "release_timestamp": version["release_timestamp"]
    }


def get_processed_versions():
    versions = get_versions()
    extracted_versions = [__process_version(version) for version in versions]
    return sorted(extracted_versions, key=lambda v: v["release_timestamp"], reverse=True)


def get_latest_version():
    return __process_version(get_versions()[-1])


def get_game_version(game_path: str):
    # Get the version of the game from which the Locres is being extracted
    # Read the executable as bytes
    with open(game_path, 'rb') as game_file:
        # Find the sequence of bytes and extract relevant part
        client_ver_hex = game_file.read().hex().split('2b002b0041007200650073002d0043006f00720065002b00')[1][0:192]
        # Transform bytes into a readable list of strings
        client_ver_list = list(filter(None, bytes.fromhex(client_ver_hex).decode('utf-16-le').split('\x00')))
        # Compose the version string
        return client_ver_list[0] + '-' + client_ver_list[2] + '-' + \
               client_ver_list[3].rsplit('.')[-1].lstrip('0')


def __check_manifests():
    global CURRENT_VERSION, CURRENT_MANIFEST, LAST_MANIFEST

    versions = get_processed_versions()
    check_manifest = versions[0]["manifest"]
    if check_manifest != CURRENT_MANIFEST:
        LAST_MANIFEST = CURRENT_MANIFEST
        CURRENT_MANIFEST = check_manifest
        CURRENT_VERSION = versions[0]
        info_message = "Manifest initialized:" if LAST_MANIFEST == "" else "Manifest updated"
        print("[INFO]", info_message, check_manifest)
    else:
        print("[INFO] No new manifest")


def __main():
    print("[INFO] ManifestChecker started\n")

    schedule.every(5).seconds.do(__check_manifests)
    __check_manifests()

    found_new = False
    while not found_new:
        schedule.run_pending()
        time.sleep(1)
        if CURRENT_MANIFEST != "" and LAST_MANIFEST != "":
            print("\n[INFO] NEW MANIFEST FOUND")
            print(" - Manifest:", CURRENT_VERSION["manifest"])
            print(" - Client version:", CURRENT_VERSION["client_version"])
            found_new = True


if __name__ == "__main__":
    __main()
