
# carrotsh <br /> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh" title="Version"><img src="https://img.shields.io/static/v1?label=Version&message=1.0.1&color=red"></a> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh/blob/master/LICENSE" title="License"><img src="https://img.shields.io/static/v1?label=License&message=The%20Unlicense&color=blue"></a>
A lightweight server that allows clients to connect securely and launch a shell or program remotely through a browser.


![Screenshot](https://raw.githubusercontent.com/AnnikaV9/carrotsh/master/preview.gif)

<br />
<br />

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Encryption](#encryption)
- [Blocklists](#blocklists)
- [Reverse proxies](#reverseproxies)
- [Contributing](#contributing)

<br />
<br />

## Introduction <a name="introduction"></a>
carrotsh is a lightweight and secure remote access server that uses the [websocket protocol](https://en.wikipedia.org/wiki/WebSocket), with full https support for encrypted connections. It aims to provide an ssh-like experience, but through a browser. The backend primarily runs on node.js, while the login manager and various scripts use python. [xterm.js](https://github.com/xtermjs/xterm.js/) is used as the frontend terminal. No installation of extensions or userscripts is necessary on the client side to access a carrotsh instance, only a modern browser with javascript support is required.

<br />
<br />

## Prerequisites <a name="prerequisites"></a>

Supported operating systems:
 - macOS (Tested on Big Sur)
 - GNU/Linux (Tested on Arch & Debian)
 - musl/Linux (Tested on Alpine Linux)
 - Android (Tested on Android 11 & 12 using [Termux](https://github.com/termux/termux-app))


Required software:
 - node.js
 - npm
 - python
 - python-cryptography
 - make & g++ (Linux, Android) or Xcode (MacOS) - (For compiling node-pty when running `npm install`)
 
<br />
<br />
 
## Installation <a name="installation"></a>
```
# Clone the repository
git clone https://github.com/AnnikaV9/carrotsh.git
 
# Change the working directory
cd carrotsh

# Install the dependencies
npm install

# Edit the configuration file
vim config.json

# Set the server password
python3 carrotsh.py setpass
```

<br />
<br />

## Usage <a name="usage"></a>

```
$ python3 carrotsh.py --help

Usage: python3 carrotsh.py <COMMAND> [args]

Commands:

version                               output the version information
start                                 run a syntax check and start the carrosh server
stop                                  stop the carrotsh server
status                                show the current status of the server
setpass                               set the server password
clear-auto-blocklist                  clear the auto blocklist
clear-user-blocklist                  clear the user blocklist
add-blocklist-address <address>       add an address to the user blocklist
install-blocklist </path/to/list>     copy addresses in a file to the user blocklist
config-dump                           output all configuration options to the terminal

```
Note: Do not run carrotsh as root/admin. It is unnecessary and only reduces security.

<br />
<br />

## Configuration <a name="configuration"></a>
[config.json](https://github.com/AnnikaV9/carrotsh/blob/master/config.json) is the primary configuration file.

Available options:
| Option |Description | Type | Default |
|--|--|--|--|
| port | The port the server should listen for requests on | integer | 6060 |
| shell | Path to the shell executable. This does not actually have to be a valid shell, any program can be used, interactive or not. For example, to launch a disposable container with podman, you could set this as `podman run --rm -it myimage` | string | /bin/bash |
| shell_timeout_milliseconds | The max age (milliseconds) of the spawned shell session | integer | 3600000 |
| python_path | Path to your python interpreter, which will be used to run [login.py](https://github.com/AnnikaV9/carrotsh/blob/master/login/login.py) | string | /usr/bin/python3 |
| password_auth | Enables or disables password authentication | boolean | true |
| salt (Under password_auth_options) | The salt used when hashing the password for storage. Please change the default value. After changing, make sure to run `python3 carrotsh.py setpass` again to generate a new hash | string | carrots |
| show_username (Under password_auth_options) | Shows or hides username in the login prompt | boolean | true |
| https | Enables or disables TLS/SSL | boolean | false |
| path_to_cert (Under https_options) | Path to your certificate file | string | ./cert.pem |
| path_to_key (Under https_options) | Path to your key file | string | ./key.pem |
| blocklist_shadow_mode | Shadow mode does not reveal if the client is blocked when they connect. It will spawn a fake login prompt, that will fail to authenticate even if the correct password is given | boolean | false |
| auto_blocklist | Automatically add and remove addresses to the auto blocklist depending on the configuration. | boolean | true |
| max_incorrect_attempts (Under auto_blocklist_options) | The maximum number of incorrect password attempts a client can make before their address is added to the auto blocklist | integer | 5 |
| unblock_after_minutes (Under auto_blocklist_options) | The number of minutes to wait before unblocking an address in the auto blocklist | integer | 10080 |

<br />
<br />

## Encryption <a name="encryption"></a>
carrotsh requires proper usage and configuration in order to be secure. Make sure to set up https, so connections are encrypted and cannot be sniffed. Here's an example process of creating a self-signed ssl certificate:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
```
And then add the two files to the [configuration](#configuration).

<br />
<br />

## Blocklists <a name="blocklists"></a>
Blocklists allow you to prevent clients with blocked remote addresses from ever reaching the login prompt. There are two blocklists carrotsh uses:

#### [auto_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/blocklists/auto_blocklist.json)
The auto blocklist is used when `auto_blocklist` in the configuration is set to true. It will automatically add addresses when clients perform a set number of incorrect password attempts (Default: 5), and remove them from the list after a set period (Default: 1 week). The auto blocklist should only be modified if there are false positives. (eg. You get yourself blocked after entering the incorrect password)

To clear the auto blocklist:
```
python3 carrotsh.py clear-auto-blocklist
```


#### [user_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/blocklists/user_blocklist.json)

The user blocklist is for you to edit and add addresses manually.
To add a single address:
```
python3 carrotsh.py add-blocklist-address <address>
```
To add a list with multiple addresses:
```
python3 carrotsh.py install-blocklist </path/to/list>
```
This will append the addresses in the list to the user blocklist, removing any `#` comments.

The user blocklist can be cleared the same way as the auto blocklist:
```
python3 carrotsh.py clear-user-blocklist
```

<br />
<br />

## Reverse proxies <a name="reverseproxies"></a>
carrotsh currently does not have proper support for use with reverse proxies like nginx. It may work, but the auto blocklist may end up blocking everyone from connecting since it only sees the proxy's address. Using X-Forwarded-For requires a significant change to the code, as the header can be easily spoofed when connecting directly past the proxy. Until a proper solution is implemented, it is not recommended to run carrotsh behind a reverse proxy. If you do have a working solution, feel free to [contribute](#contributing).

<br />
<br />

## Contributing <a name="contributing"></a>
Feel like something can be improved? Found a bug? Open an issue!

Want to contribute directly? Feel free to make a pull request!

Feature requests are also welcome! :D
