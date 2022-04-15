
# carrotsh <br /> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh" title="Version"><img src="https://img.shields.io/static/v1?label=Version&message=0.4.0&color=red"></a> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh/blob/master/LICENSE" title="License"><img src="https://img.shields.io/static/v1?label=License&message=The%20Unlicense&color=blue"></a>
A lightweight server that allows clients to connect securely and launch a shell or program remotely through a browser. Uses [xterm.js](https://github.com/xtermjs/xterm.js/) for the frontend.


![Screenshot](https://raw.githubusercontent.com/AnnikaV9/carrotsh/master/preview.gif)

<br />

## Requirements
 - node.js
 - npm
 - python
 - python-cryptography
 - make & g++ (GNU/Linux) or Xcode (MacOS) - (For compiling node-pty when running `npm install`)
 
<br />
 
## Installation & Usage
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

## Configuration
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
| auto_blocklist | Automatically block and unblock addresses depending on the configuration. The manual blocklist ([user_blocklist.json](https://github.com/AnnikaV9/carrotsh/blob/master/user_blocklist.json)) will override the auto blocklist | boolean | true |
| max_incorrect_attempts | The maximum number of incorrect password attempts a client can make before their address is added to the auto blocklist | integer | 5 |
| unblock_after_minutes | The number of minutes to wait before unblocking an address in the auto blocklist | integer | 10080 |

<br />

## Todo
- Implement server logging
- Allow font/theme customization client-side, and setting of defaults server-side

<br />

## Contributing
Feel like something can be improved? Found a bug? Open an issue!

Want to contribute directly? Feel free to make a pull request!
