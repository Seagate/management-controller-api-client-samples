# Storage-Devices
The purpose of this repository is to keep the scripts, tools, and other configuration used for Seagate Storage Devices. This project is licensed under Apache License 2.0.

**Disclaimer: "Quality matters not quantity."**

## Includes
* API as well as REST interface for management operations
* [CLI reference guide](./src/scripts/oldSamples/CLI_Reference_Guide.pdf)

## Repo Structure

```
.
├── CODE_OF_CONDUCT.md
├── CODEOWNERS
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── src
    └── scripts
        ├── const.py
        ├── login
        │   ├── loginFactory.py
        │   ├── login.py
        │   └── README.md
        ├── oldSamples
        │   ├── APIAccessBase64.py
        │   ├── APIAccessBase64SHA256.pl
        │   ├── APIAccessBase64SHA256.py
        │   ├── APIAccessSHA256.py
        │   ├── CLI_Reference_Guide.pdf
        │   ├── RESTAccessBase64.py
        │   ├── RESTAccessBase64SHA256.py
        │   └── RESTAccessSHA256.py
        └── README.md

```

## [Scripts](./src/scripts/)

Here our community is providing the very useful scripts for Seagate Storage Devices. 

### List of scripts in this repository:
Below you can find the list of all scripts which are very useful for the developers, so dive in:

#### [Module](./src/scripts/README.md)

* [Old Sample](./src/scripts/oldSamples/)
* [Login](./src/scripts/login/README.md)

## Requirements

* Python >= 3.6

## License
These scripts are offered under the Apache 2 license.

## Source Code
The latest developer version is available in a GitHub repository: https://github.com/Seagate/SAN-Scripts