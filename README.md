
# carrotsh <br /> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh" title="Version"><img src="https://img.shields.io/static/v1?label=Version&message=0.4.1&color=red"></a> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh/blob/master/LICENSE" title="License"><img src="https://img.shields.io/static/v1?label=License&message=The%20Unlicense&color=blue"></a>
A lightweight server that allows clients to connect securely and launch a shell or program remotely through a browser. Uses [xterm.js](https://github.com/xtermjs/xterm.js/) for the frontend.


![Screenshot](https://raw.githubusercontent.com/AnnikaV9/carrotsh/master/preview.gif)

<br />
<br />

## Table of Contents
- [Requirements](#requirements)
- [Installation & Usage](#installation)
- [Configuration](#configuration)
- [Blocklists](#blocklists)
- [Reverse proxies](#reverseproxies)
- [Todo](#todo)
- [Contributing](#contributing)

<br />
<br />

## Requirements <a name="requirements"></a>
 - node.js
 - npm
 - python
 - python-cryptography
 - make & g++ (GNU/Linux) or Xcode (MacOS) - (For compiling node-pty when running `npm install`)
 
<br />
<br />
 
## Installation & Usage <a name="installation"></a>
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
python3 setpass.py

# Start the server
node index.js
```

<br />
<br />

## Configuration <a name="configuration"></a>
carrotsh uses [config.json](https://github.com/AnnikaV9/carrotsh/blob/master/config.json) as the primary configuration file.

Available options:
| Option |Description | Type | Default |
|--|--|--|--|
| port | The port the server should listen for requests on | integer | 6060 |
| shell | Path to the shell executable. This does not actually have to be a valid shell, any program can be used, interactive or not. For example, to launch a disposable container with podman, you could set this as `podman run --rm -it myimage` | string | /bin/bash |
| shell_timeout_milliseconds | The max age (milliseconds) of the spawned shell session | integer | 3600000 |
| python_path | Path to your python interpreter, which will be used to run [login.py](https://github.com/AnnikaV9/carrotsh/blob/master/login.py) | string | /usr/bin/python3 |
| password_auth | Enables or disables password authentication | boolean | true |
| salt (Under password_auth_options) | The salt used when hashing the password for storage. Please change the default value. After changing, make sure to run [setpass.py](https://github.com/AnnikaV9/carrotsh/blob/master/setpass.py) again to generate a new hash | string | carrots |
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

## Blocklists <a name="blocklists"></a>
Blocklists allow you to prevent clients with blocked remote addresses from ever reaching the login prompt. There are two blocklists carrotsh uses:

#### [auto_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/auto_blocklist.json)
The auto blocklist is used when `auto_blocklist` in the configuration is set to true. It will automatically add addresses when clients perform a set number of incorrect password attempts (Default: 5), and remove them from the list after a set period (Default: 1 week). The auto blocklist should only be modified if there are false positives. (eg. You get yourself blocked after entering the incorrect password)

#### [user_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/user_blocklist.json)

The user blocklist is for you to edit and add addresses manually. For a small number of addresses, editing the blocklist directly should be fine. For larger lists, you can use [blocklist_install.py]():
```
python3 blocklist_install.py /path/to/large/list
```
This will automatically format and append the addresses to the user blocklist, removing any `#` comments.

<br />
<br />

## Reverse proxies <a name="reverseproxies"></a>
carrotsh currently does not have proper support for use with reverse proxies like nginx. It may work, but the auto blocklist may end up blocking everyone from connecting since it only sees the proxy's address. Using X-Forwarded-For requires a significant change to the code, as the header can be easily spoofed when connecting directly past the proxy. Until a proper solution is implemented, it is not recommended to run carrotsh behind a reverse proxy. If you do have a working solution, feel free to [contribute](#contributing).

<br />
<br />

## Todo <a name="todo"></a>
- Implement a launcher system that checks configuration and blocklists for syntax errors before running the server
- Create a CLI program that can connect directly to carrotsh's websocket backend for an ssh-like experience

<br />
<br />

## Contributing <a name="contributing"></a>
Feel like something can be improved? Found a bug? Open an issue!

Want to contribute directly? Feel free to make a pull request!
