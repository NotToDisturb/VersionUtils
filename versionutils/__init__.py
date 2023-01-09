import json
import time
import schedule

from urllib.error import HTTPError
from urllib.request import Request, urlopen
from fake_useragent import UserAgent

CURRENT_VERSION = {}
CURRENT_MANIFEST = ""
LAST_MANIFEST = ""

WOB_URL = "https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json"
KA_URL = "http://51.178.18.16:8000/api/v1/manifests"
RIOT_URL = "https://clientconfig.rpg.riotgames.com/api/v1/config/public?namespace=keystone.products.valorant.patchlines"

# Key is the version in which the Unreal Engine version started to be used
UE_VERSIONS = {
    "5.03": {
        "unreal_engine": "4.26",
        "umodel": "valorant"
    },
    "2.11": {
        "unreal_engine": "4.25",
        "umodel": "ue4.25"
    },
    "2.0": {
        "unreal_engine": "4.24",
        "umodel": "ue4.24"
    },
    "0.49": {
        "unreal_engine": "4.23",
        "umodel": "ue4.23"
    },
    "0": {
        "unreal_engine": "4.22",
        "umodel": "ue4.22"
    },
}


def get_versions() -> list:
    response = urlopen(WOB_URL)
    versions_raw = response.read().decode("utf-8")
    return json.loads(versions_raw)


def get_manifests(version: str = ""):
    response = urlopen(KA_URL + ("" if version == "" else "?version=" + version))
    manifests = response.read().decode("utf-8")
    return json.loads(manifests)


def get_valorant_live():
    request = Request(RIOT_URL)
    request.add_header("User-Agent", UserAgent().random)
    response = urlopen(request)
    live_configs = response.read().decode("utf-8")
    return json.loads(live_configs)["keystone.products.valorant.patchlines.live"]


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


def get_latest_manifest() -> str:
    live_configs = get_valorant_live()
    for config in live_configs["platforms"]["win"]["configurations"]:
        if config["id"] == "na":
            return config["patch_url"]


def get_game_version(game_path: str) -> dict:
    # Get the version of the game from which the Locres is being extracted
    # Read the executable as bytes
    with open(game_path, 'rb') as game_file:
        # Find the sequence of bytes and extract relevant part
        client_ver_hex = game_file.read().hex().split('2b002b0041007200650073002d0043006f00720065002b00')[1][0:192]
        # Transform bytes into a readable list of strings
        client_ver_list = list(filter(None, bytes.fromhex(client_ver_hex).decode('utf-16-le').split('\x00')))
        # Compose the version string
        return {
            "branch": __clean_version_branch(client_ver_list[0]),
            "version": client_ver_list[3],
            "date": client_ver_list[1]
        }


def is_version_newer(version_a: str, version_b: str):
    split_version_a = version_a.split(".")
    split_version_b = version_b.split(".")
    for i in range(min(len(split_version_a), len(split_version_b))):
        if int(split_version_a[i]) > int(split_version_b[i]):
            return True
        if int(split_version_a[i]) < int(split_version_b[i]):
            return False
    return len(split_version_a) >= len(split_version_b)


def get_ue_version(version: str):
    for check_version, ue_version in UE_VERSIONS.items():
        if is_version_newer(version, check_version):
            return ue_version


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
    print(get_latest_manifest())

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
