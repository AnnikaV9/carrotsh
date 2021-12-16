
# carrotsh <br /> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh" title="Version"><img src="https://img.shields.io/static/v1?label=Version&message=0.1.1&color=red"></a> <a target="_blank" href="https://github.com/AnnikaV9/carrotsh/blob/master/LICENSE" title="License"><img src="https://img.shields.io/static/v1?label=License&message=The%20Unlicense&color=blue"></a>
A simple and lightweight server that allows clients to connect and launch a shell remotely through a browser. Uses [xterm.js](https://github.com/xtermjs/xterm.js/) for the frontend.


![Screenshot](https://cdn.discordapp.com/attachments/699852562505138236/916156149143842906/record1.gif)

<br />

## Requirements
 - node.js
 - npm
 - python
 - python-cryptography
 - make & g++ (For compiling node-pty when running `npm install`)
 
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
 - port: The port the server should listen on. *(Default: 6060)*
 - shell: Path to the shell executable. *(Default: `/bin/bash`)*
 - shell_timeout: The max age (ms) of the spawned shell session. *(Default: 3600000)*
 - python_path: Path to your python interpreter. *(Default: `/usr/bin/python3`)*
 - password_auth: Set as `false` to disable authentication. *(Default: `true`)*
 - password_auth_options
    * salt: The salt used when hashing the password for storage. Please change the default value. After changing, make sure to run [setpass.py](https://github.com/AnnikaV9/carrotsh/blob/master/setpass.py) again to generate a new hash.*(Default: carrots)*
 - https: Set as `true` to enable TLS/SSL. *(Default: `false`)*
 - https_options
    * path_to_cert: Path to your certificate file. *(Default: `./cert.pem`)*
    * path_to_key: Path to your key file. *(Default: `./key.pem`)*

<br />

## Todo
- Implement server logging
- Allow font/theme customization client-side, and setting of defaults server-side

<br />

## Contributing
Feel like something can be improved? Found a bug? Open an issue!

Want to contribute directly? Feel free to make a pull request!
