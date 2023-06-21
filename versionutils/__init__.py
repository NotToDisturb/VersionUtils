import json
import os
import time
import schedule

from urllib.request import Request, urlopen
from fake_useragent import UserAgent

CURRENT_MANIFEST = ""
LAST_MANIFEST = ""

WOB_URL = "https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json"
VA_URL = "https://raw.githubusercontent.com/NotToDisturb/VersionArchive/master/out/manifests.json"
RIOT_URL = "https://clientconfig.rpg.riotgames.com/api/v1/config/public?namespace=keystone.products.valorant.patchlines"
VERSIONS_PATH = os.path.dirname(__file__) + "\\ue_versions.json"

# Key is the version in which the Unreal Engine version started to be used
UE_VERSIONS = json.load(open(VERSIONS_PATH, "rt"))["data"]


def get_wob_versions() -> list:
    response = urlopen(WOB_URL)
    versions_raw = response.read().decode("utf-8")
    return json.loads(versions_raw)


def get_va_versions() -> list:
    response = urlopen(VA_URL)
    versions = response.read().decode("utf-8")
    return json.loads(versions)


def get_live_configs() -> dict:
    request = Request(RIOT_URL)
    request.add_header("User-Agent", UserAgent().random)
    response = urlopen(request)
    live_configs = response.read().decode("utf-8")
    return json.loads(live_configs)["keystone.products.valorant.patchlines.live"]


def __clean_version_branch(branch: str):
    return branch if branch == "pbe" else branch.split("-")[0]


def __clean_version(branch: str, release_version, pbe_version):
    return pbe_version if branch == "pbe" else release_version


def __process_version(version: dict) -> dict:
    return {
        "manifest": version["id"],
        "branch": __clean_version_branch(version["build_info"]["branch"]),
        "version": version["build_info"]["version"],
        "date": version["build_info"]["build_date"],
        "upload_timestamp": version["upload_timestamp"],
        "release_timestamp": version["release_timestamp"]
    }


def get_processed_wob_versions() -> list:
    versions = get_wob_versions()
    processed_versions = [__process_version(version) for version in versions]
    return sorted(
        processed_versions,
        key=lambda v: v["upload_timestamp"] if v["release_timestamp"] == 0 else v["release_timestamp"],
        reverse=True
    )


def get_versions() -> list:
    va_versions = get_va_versions()
    wob_versions = get_processed_wob_versions()
    for wob_version in wob_versions:
        # Found the latest version in VersionArchive, stop searching for missing versions
        if wob_version["manifest"] == va_versions[0]["manifest"]:
            break
        va_versions.append(wob_version)
    return sorted(
        va_versions,
        key=lambda v: v["upload_timestamp"] if v["release_timestamp"] == 0 else v["release_timestamp"],
        reverse=True
    )


def get_latest_version() -> dict:
    return __process_version(get_wob_versions()[-1])


def get_manifests(version: str = "", branch: str = "") -> list:
    return [version_data["manifest"] for version_data in get_versions()
            if version in version_data["version"] and branch in version_data["branch"]]


def __get_release_manifest():
    live_configs = get_live_configs()
    for config in live_configs["platforms"]["win"]["configurations"]:
        if config["id"] == "na":
            return config["patch_url"]


def get_latest_manifest() -> str:
    """
    While this implementation does get the latest `live` manifest,
    it does not account for PBE manifests, so fallback on
    combination of this and WOB data.

    TODO: Get PBE data (need a PBE account for that lmao)

    live_configs = get_live_configs()
    for config in live_configs["platforms"]["win"]["configurations"]:
        if config["id"] == "na":
            return config["patch_url"]"""
    release_latest = extract_manifest_id(__get_release_manifest())
    wob_versions = get_processed_wob_versions()
    for wob_version in wob_versions[-2:]:
        if release_latest == wob_version["manifest"]:
            return wob_versions[-1]
    return release_latest


def extract_manifest_id(manifest_url: str) -> str:
    return os.path.basename(manifest_url.split(".manifest")[0])


def get_game_version(game_path: str) -> dict:
    # Read the executable as bytes
    with open(game_path, 'rb') as game_file:
        # Find the sequence of bytes and extract relevant part
        client_ver_hex = game_file.read().hex().split('2b002b0041007200650073002d0043006f00720065002b00')[1][0:192]
        # Transform bytes into a readable list of strings
        client_ver_list = list(filter(None, bytes.fromhex(client_ver_hex).decode('utf-16-le').split('\x00')))
        # Compose the version string
        branch = __clean_version_branch(client_ver_list[0])
        return {
            "branch": branch,
            "version": __clean_version(branch, client_ver_list[2], client_ver_list[3]),
            "date": client_ver_list[1]
        }


def get_ue_version(game_version: str):
    for check_version, ue_version in UE_VERSIONS.items():
        if is_version_newer(game_version, check_version):
            return ue_version


def is_version_newer(version_a: str, version_b: str):
    split_version_a = version_a.split(".")
    split_version_b = version_b.split(".")
    for i in range(min(len(split_version_a), len(split_version_b))):
        if int(split_version_a[i]) > int(split_version_b[i]):
            return True
        if int(split_version_a[i]) < int(split_version_b[i]):
            return False
    return len(split_version_a) >= len(split_version_b)


def __check_manifests():
    global CURRENT_MANIFEST, LAST_MANIFEST

    check_manifest = get_latest_manifest()
    if check_manifest != CURRENT_MANIFEST:
        LAST_MANIFEST = CURRENT_MANIFEST
        CURRENT_MANIFEST = check_manifest
        info_message = "Manifest initialized:" if LAST_MANIFEST == "" else "NEW MANIFEST FOUND: "
        print("[INFO]", info_message, check_manifest)
    else:
        print("[INFO] No new manifest")


def __start_manifest_check():
    global CURRENT_MANIFEST, LAST_MANIFEST
    print("\n==== MANIFEST CHECKER ====")
    schedule.every(10).seconds.do(__check_manifests)
    __check_manifests()

    found_new = False
    while not found_new:
        schedule.run_pending()
        time.sleep(1)
        if CURRENT_MANIFEST != "" and LAST_MANIFEST != "" and CURRENT_MANIFEST != LAST_MANIFEST:
            found_new = True


def __start_manifest_query():
    do_query = True
    print("\n==== MANIFEST QUERY ====")
    while do_query:
        select_version = input("\n[INPUT] Select a version: ")
        while select_version == "":
            select_version = input("[INPUT] No version selected: ")

        valid_branches = ["", "pbe", "release"]
        select_branch = input("[INPUT] Select a branch: ")
        while select_branch not in valid_branches:
            select_branch = input("[INPUT] Invalid branch: ")

        manifests = get_manifests(select_version, select_branch)
        print(f"[INFO]  {len(manifests)} manifest{'' if len(manifests) == 1 else 's'} found: "
              f"'" + "', '".join(manifests) + "'")
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
