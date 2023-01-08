import json
import time

import schedule
import urllib.request
from urllib.error import HTTPError

CURRENT_VERSION = {}
CURRENT_MANIFEST = ""
LAST_MANIFEST = ""
WOB_URL = "https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json"
KA_URL = "http://51.178.18.16:8000/api/v1/manifests"


def get_versions() -> list:
    response = urllib.request.urlopen(WOB_URL)
    versions_raw = response.read().decode("utf-8")
    return json.loads(versions_raw)


def get_manifests(version: str = ""):
    response = urllib.request.urlopen(KA_URL + ("" if version == "" else "?version=" + version))
    versions_raw = response.read().decode("utf-8")
    return json.loads(versions_raw)


def __clean_version_branch(branch: str):
    return branch if branch == "pbe" else branch.split("-")[0]


def __process_version(version: dict) -> dict:
    return {
        "manifest": version["id"],
        "branch": __clean_version_branch(version["build_info"]["branch"]),
        "version": version["build_info"]["version"],
        "release_timestamp": version["release_timestamp"]
    }


def get_processed_versions() -> list:
    versions = get_versions()
    extracted_versions = [__process_version(version) for version in versions]
    return sorted(extracted_versions, key=lambda v: v["release_timestamp"], reverse=True)


def get_latest_version() -> dict:
    return __process_version(get_versions()[-1])


def get_game_version(game_path: str) -> str:
    # Get the version of the game from which the Locres is being extracted
    # Read the executable as bytes
    with open(game_path, 'rb') as game_file:
        # Find the sequence of bytes and extract relevant part
        client_ver_hex = game_file.read().hex().split('2b002b0041007200650073002d0043006f00720065002b00')[1][0:192]
        # Transform bytes into a readable list of strings
        client_ver_list = list(filter(None, bytes.fromhex(client_ver_hex).decode('utf-16-le').split('\x00')))
        # Compose the version string
        return __clean_version_branch(client_ver_list[3]) + "-" + client_ver_list[3]


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


def __start_manifest_check():
    print("\n[INFO] New manifest checker started")
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


def __start_manifest_query():
    do_query = True
    while do_query:
        select_manifest = input("\n[INPUT] Select a version to query manifests for: ")
        while select_manifest == "":
            select_manifest = input("[INPUT] No version selected, select one to query manifests: ")
        try:
            manifests = get_manifests(select_manifest)
            print(f"[INFO]  {len(manifests)} manifest{'' if len(manifests) == 1 else 's'} found: "
                  f"'" + "', '".join(manifests) + "'")
        except HTTPError:
            print(f"[INFO]  No manifests found for version '{select_manifest}'")
        should_query = input("[INPUT] Do another query? (y/n) ")
        do_query = should_query.lower() == "y"


def __main():
    valid_selections = ["1", "2"]
    selection_to_function = {
        "1": __start_manifest_check,
        "2": __start_manifest_query
    }

    print("[INPUT] Started VersionUtils")
    print("        1. Check for new manifest")
    print("        2. Query manifests for specific game version")
    select = input("        Select an option: ")
    while select not in valid_selections:
        select = input("        Invalid input, select an option: ")
    selection_to_function[select]()


if __name__ == "__main__":
    __main()
