## VersionUtils
VersionUtils is Python 3.8 script that allows the user to obtain information regarding VALORANT game versions, 
be it from the game's executable or from [WhiteOwlBot's (WOB) public data](https://github.com/WhiteOwlBot/WhiteOwl-public-data).

### Standalone usage
TO-DO

### Package usage
#### Installation
To install this package, run the following command:

`pip install git+https://github.com/NotToDisturb/VersionUtils.git#egg=VersionUtils`

#### Documentation
There are 4 methods available for use:
- `get_versions`
    - No arguments
    - Returns:
        - Dictionary with the contents of [WOB's public data](https://raw.githubusercontent.com/WhiteOwlBot/WhiteOwl-public-data/main/manifests.json)
    

- `get_processed_versions`
    - No arguments
    - Returns:
        - Dictionary with the processed contents of WOB's public data, sorted in descending order by release timestamp
    

- `get_latest_version`
    - No arguments
    - Returns:
        - Dictionary with the processed contents of the latest version in WOB's public data
    

- `get_game_version`
    - 1 argument:
        - `game_path`: A string containing the path to VALORANT's `VALORANT-Win64-Shipping.exe`
    - Returns:
        - String containing the version present in the executable
    
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
print(get_game_version())
```
*Note: Replace `GAME_PATH` with the folder you installed VALORANT to*

## Credits
floxay [Go](https://github.com/floxay)