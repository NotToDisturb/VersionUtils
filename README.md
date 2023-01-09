# VersionUtils
VersionUtils is Python 3.8 script that allows the user to obtain information regarding VALORANT game versions, 
be it from the game's executable, from [WhiteOwlBot's (WOB) public data](https://github.com/WhiteOwlBot/WhiteOwl-public-data)
or from [VersionArchive](https://github.com/NotToDisturb/VersionArchive/).

## Package usage
### Installation

`pip install git+https://github.com/NotToDisturb/VersionUtils.git#egg=VersionUtils`
<br><br>
### Documentation
- [`get_wob_versions`](#get_wob_versions---list)
- [`get_va_versions`](#get_va_versions---list)
- [`get_live_configs`](#get_live_configs---dict)
- [`get_processed_wob_versions`](#get_processed_wob_versions---list)
- [`get_latest_version`](#get_latest_version---dict)
- [`get_manifests`](#get_manifestsversion-str---branch-str-----list)
- [`get_latest_manifest`](#get_latest_manifest---str)
- [`get_game_version`](#get_game_versiongame_path-str---str)
- [`get_ue_version`](#get_ue_versiongame_version-str---str)
- [`is_version_newer`](#is_version_newerversion_a-str-version_b-str---bool)

<br>

> ##### `get_wob_versions() -> list`
> 
> Returns a `list` of `dict`s with the contents of [WOB's public data](https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json). See the [version structure](#wob-version).

<br>

> ##### `get_va_versions() -> list`
>
> Returns a `list` of `dict`s with the contents of [VersionArchive's data](https://raw.githubusercontent.com/NotToDisturb/VersionArchive/master/out/manifests.json). See the [version structure](#processed-version).

<br>

> ##### `get_live_configs() -> dict`
>
> Returns a `dict` with the contents of [Riot's Client Config API](https://clientconfig.rpg.riotgames.com/api/v1/config/public?namespace=keystone.products.valorant.patchlines). 

<br>

> ##### `get_processed_wob_versions() -> list`
> 
> Returns a `list` of `dict`s with the processed contents of WOB's public data, 
> sorted in descending order by `release_timestamp`. See the [processed structure](#processed-version).

<br>

> ##### `get_versions() -> list`
>
> Returns a `list` of `dict`s with the combined versions from VersionArchive and the processed WOB's public data, 
> sorted in descending order by `release_timestamp`. See the [version structure](#processed-version).

<br>

> ##### `get_latest_version() -> dict`
> 
> Returns a `dict` with the processed contents of the latest version in WOB's public data. 
> If you are just looking for the latest manifest, use [`get_latest_manifest`](#get_latest_manifest---str). See the [version structure](#processed-version).

<br>

> ##### `get_manifests(version: str = "", branch: str = "") -> list`
> 
> Returns a `list` with all the manifests for the specified version and branch.

<br>

> ##### `get_latest_manifest() -> str`
>
> Returns a `str` containing the url to the latest manifest.

<br>

> ##### `get_game_version(game_path: str) -> str`
> 
> Returns a `dict` containing version data present in the game's executable. See the [game version structure](#game-version).

<br>

> ##### `get_ue_version(game_version: str) -> str`
>
> Returns a `dict` containing data about the Unreal Engine version used in that version. See the [UE version structure](#unreal-engine-version).

<br>

> ##### `is_version_newer(version_a: str, version_b: str) -> bool`
>
> Returns a `bool` representing whether `version_a` is newer than `version_b`,
> where the versions are numbers separated by periods, such as `05.12.00.808353`.
>
> If both versions are of different lengths and are equal up to where the length differs,
> the newer will be the longer version. For instance `05.12.00.808353` is newer than `05.12`.

<br>

### Return structures
#### WOB version
|**Attribute**              |Type |**Description**|
|---------------------------|-----|---------------|
|`id`                       |`str`|A hexadecimal string that identifies a patch|
|`upload_timestamp`         |`int`|An integer that represent the upload time of the patch in milliseconds|
|`release_timestamp`        |`int`|An integer that represent the release time of the patch in milliseconds|
|`build_info.branch`        |`str`|Either `release-X.YY` or `pbe`, where `X.YY` is an umbrella version number|
|`build_info.version`       |`str`|The client version visible in-game|
|`build_info.build_version` |`int`|Unclear what this represents|
|`build_info.build_date`    |`str`|The date of the build|
|`build_info.client_version`|`str`|A composition of the other `build_info` attributes|

#### Processed version
|**Attribute**      |Type |**Description**|
|-------------------|-----|---------------|
|`manifest`         |`str`|A hexadecimal string that identifies a patch|
|`branch`           |`str`|Either `release` or `pbe`|
|`version`          |`str`|The client version visible in-game|
|`date`             |`int`|The date of the build|
|`release_timestamp`|`int`|An integer that represent the release time of the patch in milliseconds|

#### Game version
|**Attribute**|Type |**Description**|
|-------------|-----|---------------|
|`branch`     |`str`|Either `release` or `pbe`|
|`version`    |`str`|The client version visible in-game|
|`date`       |`int`|The date of the build in `MM/DD/YYYY` format|

#### Unreal Engine version
|**Attribute**  |Type |**Description**|
|---------------|-----|---------------|
|`unreal_engine`|`str`|An Unreal Engine version|
|`umodel`       |`str`|The `game` argument to use when opening this version in UModel|

<br>

### Example usage
Here is an example of how to use VersionUtils:
```
from versionutils import get_latest_version, get_game_version

GAME_PATH = "C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Binaries\\Win64\\VALORANT-Win64-Shipping.exe"

print(get_latest_version()["client_version"])
print(get_manifests("5.12", "pbe"))
print(get_game_version())
```
*Note: Replace `GAME_PATH` with the folder you installed VALORANT to*

## Standalone usage
It is also possible to use VersionUtils as a standalone script:

1. Download the [latest release](https://github.com/NotToDisturb/VersionUtils/releases/latest)
1. Extract the zip file
1. Open a console inside the extracted folder
1. Install the required packages using `pip install -r requirements.txt`
1. Run the script using `python versionutils.py`

Once executed, you will be faced with two options
> `Check for new manifests`<br>
>Polls WOB's data every 5 seconds and notifies whether or not a new manifest is available

<br>

> `Query manifests for specific game version`<br>
>After inputting a version and branch, the manifests available are displayed

## Credits
floxay [Go](https://github.com/floxay) <br>
Shiick [Go](https://github.com/Shiick) <br>
PixelButts [Go](https://twitter.com/PixelButts)