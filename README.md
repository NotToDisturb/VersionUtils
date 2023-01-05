# VersionUtils
VersionUtils is Python 3.8 script that allows the user to obtain information regarding VALORANT game versions, 
be it from the game's executable or from [WhiteOwlBot's (WOB) public data](https://github.com/WhiteOwlBot/WhiteOwl-public-data).

## Package usage
#### Installation

`pip install git+https://github.com/NotToDisturb/VersionUtils.git#egg=VersionUtils`
<br><br>
#### Documentation
- [`get_versions`](#get_versions---list)
- [`get_processed_versions`](#get_processed_versions---list)
- [`get_latest_version`](#get_latest_version---dict)
- [`get_manifests`](#get_manifestsversion-str--)
- [`get_game_version`](#get_game_versiongame_path-str---str)

<br>

> ##### `get_versions() -> list`
> 
> Returns a `list` of `dict`s with the contents of [WOB's public data](https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json)

<br>

> ##### `get_processed_versions() -> list`
> 
> Returns a `list` of `dict`s with the processed contents of WOB's public data, sorted in descending order by release timestamp

<br>

> ##### `get_latest_version() -> dict`
> 
> Returns a `dict` with the processed contents of the latest version in WOB's public data

<br>

> ##### `get_manifests(version: str = "")`
> 
> Returns a `list` with all the manifests for the specified version, 
> or a `dict` with all the manifests grouped by version if no version is specified.
> Based on [CheckValor's data](https://twitter.com/CheckValor).

<br>

> ##### `get_game_version(game_path: str) -> str`
> 
> Returns a `str` containing the version present in the executable

<br>

The processed data for each version has the following attributes:

|**Attribute**      |Type |**Description**|
|-------------------|-----|---------------|
|`manifest`         |`str`|A hexadecimal string that identifies a patch|
|`version_number`   |`str`|Numeric representation of the patch version|
|`client_version`   |`str`|Similar to `version_number`, but useful to distinguish between regular and PBE patches|
|`release_timestamp`|`int`|An integer that represent the release time of the patch in milliseconds|

<br>

#### Example usage
Here is an example of how to use VersionUtils:
```
from versionutils import get_latest_version, get_game_version

GAME_PATH = "C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Binaries\\Win64\\VALORANT-Win64-Shipping.exe"

print(get_latest_version()["client_version"])
print(get_manifests("5.12"))
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
>After inputting a version, the manifests available in CheckValor's data are displayed

## Credits
floxay [Go](https://github.com/floxay) <br>
Shiick [Go](https://github.com/Shiick)