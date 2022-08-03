<div align="center">
<h1> carrotsh <br /> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh/blob/master/pyproject.toml" title="Version"><img src="https://img.shields.io/github/package-json/v/AnnikaV9/carrotsh?label=Version&color=red"></a> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh/blob/master/LICENSE" title="License"><img src="https://img.shields.io/static/v1?label=License&message=The%20Unlicense&color=blue"></a> <a href="https://github.com/AnnikaV9/carrotsh"><img src="https://img.shields.io/github/repo-size/AnnikaV9/carrotsh?color=purple&label=Repo size"></a><br /><a href="https://github.com/AnnikaV9/carrotsh/actions/workflows/codeql-analysis.yml"><img src="https://github.com/AnnikaV9/carrotsh/actions/workflows/codeql-analysis.yml/badge.svg?branch=master"></a> <a href="https://github.com/AnnikaV9/carrotsh/actions/workflows/pylint.yml"><img src="https://github.com/AnnikaV9/carrotsh/actions/workflows/pylint.yml/badge.svg"></a> <a href="https://github.com/AnnikaV9/carrotsh/actions/workflows/devskim.yml"><img src="https://github.com/AnnikaV9/carrotsh/actions/workflows/devskim.yml/badge.svg"></a> <a href="https://github.com/AnnikaV9/carrotsh/actions/workflows/ossar.yml"><img src="https://github.com/AnnikaV9/carrotsh/actions/workflows/ossar.yml/badge.svg"></a></h1>
A lightweight and secure remote access server that allows clients to connect through a browser.

<br />
<br />

<img src="https://user-images.githubusercontent.com/68383195/166842311-1eca5a8b-2d91-4f2f-a63f-606c76d630ee.gif" width="70%"></div>

<br />
<br />

## Table of Contents <a name="contents"></a>
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Encryption](#encryption)
- [Two-Factor Authentication](#2fa)
- [Blocklists](#blocklists)
- [Start on boot](#startup)
- [Reverse proxies](#reverseproxies)
- [Todo](#todo)
- [Contributing](#contributing)

<br />
<br />

## Introduction <a name="introduction"></a>\[[^](#contents)]
carrotsh is a lightweight and secure remote access server that uses the [websocket protocol](https://en.wikipedia.org/wiki/WebSocket), with full https support for encrypted connections. It aims to provide an ssh-like experience, but through a browser. [xterm.js](https://github.com/xtermjs/xterm.js/) is used as the frontend terminal. No installation of extensions or userscripts is necessary on the client side to access a carrotsh instance, only a modern browser with javascript support is required.

#### Security features:
 - HTTPS support
 - Two-Factor authentication
 - Automatic and manual IP blocklisting
 
 <br />
 
[Try the interactive demo](https://carrotsh.herokuapp.com)

<br />
<br />

## Prerequisites <a name="prerequisites"></a>\[[^](#contents)]

#### Supported operating systems:
 - macOS (Tested on Big Sur)
 - GNU/Linux (Tested on Arch, Debian Bullseye, and RHEL 9)
 - BSD (Tested on FreeBSD 13.1 and OpenBSD 7.1)
 - musl/Linux (Tested on Alpine 3.16)
 - Android (Tested on Android 11 and 12 using [Termux](https://github.com/termux/termux-app))


#### Required software:
 - node.js v16 or above
 - npm v6 or above
 - python v3.7 or above
 - python-poetry v1 or above
 - make and g++ (Linux, Android) or Xcode (MacOS) - (For building node-pty during installation)
 - rustc - (Required only if there isn't a pre-built [cryptography](https://pypi.org/project/cryptography/) package for your architecture)
 
<br />
<br />
 
## Installation <a name="installation"></a>\[[^](#contents)]
```
# Clone the repository
git clone https://github.com/AnnikaV9/carrotsh.git
 
# Change the working directory
cd carrotsh

# Install the dependencies
python3 csh install-deps

# Edit the configuration file
vim config.yaml

# Activate the virtualenv
poetry shell

# Set the server password
python3 csh setpass
```
***Note:** Do not install or run carrotsh as root. It is unnecessary and only reduces security.*

<br />
<br />

## Usage <a name="usage"></a>\[[^](#contents)]

***Note:** Make sure to run `poetry shell` before interacting with the carrotsh cli.*
```
$ python3 csh --help

usage: python3 csh <COMMAND> [args]

commands:

    help                                  show this message
    version                               output the version information
    start                                 run a syntax check and start the carrosh server
    stop                                  stop the carrotsh server
    status                                show the current status of the server
    setpass                               set the server password
    setup-2fa                             setup 2-factor authentication
    clear-auto-blocklist                  clear the auto blocklist
    clear-user-blocklist                  clear the user blocklist
    add-blocklist-address <address>       add an address to the user blocklist
    install-blocklist </path/to/list>     copy addresses in a file to the user blocklist
    config-dump                           dump all configuration options to the terminal
    install-deps                          install npm and pip dependencies
```

<br />
<br />

## Configuration <a name="configuration"></a>\[[^](#contents)]
[config.yaml](https://github.com/AnnikaV9/carrotsh/blob/master/config.yaml) is the primary configuration file.

Available options:
| Option |Description | Type | Default |
|--|--|--|--|
| port | The port the server should listen for requests on | integer | 6060 |
| shell | Path to the shell executable and arguments. This does not actually have to be a valid shell, any program can be used, interactive or not. For example, to launch a disposable container with podman, you could set this as `["podman", "run", "--rm", "-it", "myimage"]` | array | ["/bin/bash", "--login"] |
| shell_timeout_milliseconds | The max age (milliseconds) of the spawned shell session | integer | 3600000 |
| python_path | Path to your python interpreter, which will be used to run [login.py](https://github.com/AnnikaV9/carrotsh/blob/master/login/login.py) | string | /usr/bin/python3 |
| password_auth | Enables or disables password authentication | boolean | true |
| salt (Under password_auth_options) | The salt used when hashing the password for storage. Please change the default value. After changing, make sure to run `python3 csh setpass` again to generate a new hash | string | carrots |
| show_username (Under password_auth_options) | Shows or hides username in the login prompt | boolean | true |
| 2fa | Enables or disables Two-Factor authentication | boolean | false |
| https | Enables or disables TLS/SSL | boolean | false |
| path_to_cert (Under https_options) | Path to your certificate file | string | ./cert.pem |
| path_to_key (Under https_options) | Path to your key file | string | ./key.pem |
| blocklist_shadow_mode | Shadow mode does not reveal if the client is blocked when they connect. It will spawn a fake login prompt, that will fail to authenticate even if the correct password is given | boolean | false |
| auto_blocklist | Automatically add and remove addresses to the auto blocklist depending on the configuration. | boolean | true |
| max_incorrect_attempts (Under auto_blocklist_options) | The maximum number of incorrect password attempts a client can make before their address is added to the auto blocklist | integer | 5 |
| unblock_after_minutes (Under auto_blocklist_options) | The number of minutes to wait before unblocking an address in the auto blocklist | integer | 10080 |

Most of these options can be changed without requiring you to restart carrotsh.

The below options however, do require a restart:
- port
- python_path
- https
- https_options

<br />
<br />

## Encryption <a name="encryption"></a>\[[^](#contents)]
carrotsh requires proper usage and configuration in order to be secure. Make sure to set up https, so connections are encrypted and cannot be sniffed. Here's an example openssl command for creating a self-signed ssl certificate:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
```
Enable https and add the two .pem files in the [configuration](#configuration).

An alternative to https would be a secure and trustable [VPN](https://en.wikipedia.org/wiki/Virtual_private_network).

<br />
<br />

## Two-Factor Authentication <a name="2fa"></a>\[[^](#contents)]
To set up TOTP 2fa, first enable it in the [configuration](#configuration). Then run:
```
python3 csh setup-2fa
```
This will save a base32 secret key and print it to the console. Add this secret key to your preferred authenticator  app and keep another copy somewhere safe in case you ever lose or reset your device.

A recommended open source authenticator app for android is [Aegis](https://github.com/beemdevelopment/Aegis)

<br />
<br />

## Blocklists <a name="blocklists"></a>\[[^](#contents)]
Blocklists allow you to prevent clients with blocked remote addresses from ever reaching the login prompt. There are two blocklists carrotsh uses:

#### [auto_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/blocklists/auto_blocklist.json)
The auto blocklist is used when `auto_blocklist` in the configuration is set to true. It will automatically add addresses when clients perform a set number of incorrect password attempts (Default: 5), and remove them from the list after a set period (Default: 1 week). The auto blocklist should only be modified if there are false positives. (eg. You get yourself blocked after entering the incorrect password)

To clear the auto blocklist:
```
python3 csh clear-auto-blocklist
```

<br />

#### [user_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/blocklists/user_blocklist.json)

The user blocklist is for you to edit and add addresses manually.
To add a single address:
```
python3 csh add-blocklist-address <address>
```

<br />

To add a list with multiple addresses:
```
python3 csh install-blocklist </path/to/list>
```
This will append the addresses in the list to the user blocklist, removing any `#` comments.

<br />

The user blocklist can be cleared the same way as the auto blocklist:
```
python3 csh clear-user-blocklist
```

<br />
<br />

## Start on boot <a name="startup"></a>\[[^](#contents)]
***Note:** This method has only been tested to work with [systemd](https://www.freedesktop.org/wiki/Software/systemd/).*

<br />

To start carrotsh's process manager on boot:
```
sudo ./node_modules/pm2/bin/pm2 startup -u $USER --hp $HOME
```

<br />

And after starting up carrotsh normally, run:
```
./node_modules/pm2/bin/pm2 save
```

<br />

Now pm2 wil start on system boot and run carrotsh. If you ever restart carrotsh manually, run the save command again.

<br />
<br />

## Reverse proxies <a name="reverseproxies"></a>\[[^](#contents)]
carrotsh currently does not have proper support for use with reverse proxies like nginx. It may work, but the auto blocklist may end up blocking everyone from connecting since it only sees the proxy's address. Using X-Forwarded-For requires a significant change to the code, as the header can be easily spoofed when connecting directly past the proxy. Until a proper solution is implemented, it is not recommended to run carrotsh behind a reverse proxy. If you do have a working solution, feel free to [contribute](#contributing).

<br />
<br />

## Todo <a name="todo"></a>\[[^](#contents)]

- Reverse proxy mode that only accepts connections from the configured proxy address
- Client side theme/font configuration interface &nbsp; **|** &nbsp; ***Currently WIP***
- Updater that doesn't break the config and blocklists
- Optional built-in shell with command access controls and other features that improve security

<br />
<br />

## Contributing <a name="contributing"></a>\[[^](#contents)]

All contributions are welcome, just create a pull request!

**Credits to everyone [here](https://github.com/AnnikaV9/carrotsh/graphs/contributors)**
