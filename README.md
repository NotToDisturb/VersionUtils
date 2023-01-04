# VersionUtils
VersionUtils is Python 3.8 script that allows the user to obtain information regarding VALORANT game versions, 
be it from the game's executable or from [WhiteOwlBot's (WOB) public data](https://github.com/WhiteOwlBot/WhiteOwl-public-data).

### Package usage
#### Installation

`pip install VersionUtils`

#### Documentation
There are 5 methods available for use:
>`get_versions()`<br />
> Returns a dictionary with the contents of [WOB's public data](https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json)

>`get_processed_versions()`<br />
> Returns a dictionary with the processed contents of WOB's public data, sorted in descending order by release timestamp

>`get_latest_version()`<br />
> Returns a dictionary with the processed contents of the latest version in WOB's public data

> `get_manifests(version: str = "")`<br />
> Returns a dictionary with all the manifests for the specified version, 
> or a dictionary with all the manifests grouped by version if no version is specified.
> Based on [CheckValor's data](https://twitter.com/CheckValor).

> `get_game_version(game_path: str)`<br />
> Returns a string containing the version present in the executable

The processed data for each version has the following attributes:
- `manifest`: a hexadecimal string that identifies a patch
- `version_number`: numeric representation of the patch version
- `client_version`: similar to `version_number`, but useful to distinguish between regular and PBE patches
- `release_timestamp`: an integer that represent the release time of the patch in milliseconds

## Example usage
Here is an example of how to use VersionUtils:
```
from versionutils import get_latest_version, get_game_version

GAME_PATH = "C:\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe"

print(get_latest_version()["client_version"])
print(get_manifests("5.12"))
print(get_game_version())
```
*Note: Replace `GAME_PATH` with the folder you installed VALORANT to*

### Standalone usage
It is also possible to use this script as a standalone script using these steps

- Have a Python installation with the following packages: `schedule`
- Download `versionutils\__init__.py` by clicking [here](https://raw.githubusercontent.com/NotToDisturb/VersionUtils/master/versionutils/__init__.py)
- Move and rename the downloaded file to your liking
- Execute the following command: `python <path to file>`

Once executed, you will be faced with two options
> `Check for new manifests`<br />
>Polls WOB's data every 5 seconds and notifies whether or not a new manifest is available
  

> `Query manifests for specific game version`<br />
>After inputting a version, the manifests available in CheckValor's data are displayed

## Credits
floxay [Go](https://github.com/floxay) <br />
Shiick [Go](https://github.com/Shiick)