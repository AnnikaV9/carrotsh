# carrotsh
A simple and lightweight server that allows clients to connect and launch a shell remotely through a browser. Uses [xterm.js](https://github.com/xtermjs/xterm.js/) for the frontend and [express](https://github.com/expressjs/express) for the backend.


![Screenshot](https://cdn.discordapp.com/attachments/699852562505138236/916156149143842906/record1.gif)
<br />

## Requirements
 - node.js
 - npm
 - python
 - python-cryptography
 
<br />
 
## Installation
```
# Clone the repository
git clone https://github.com/AnnikaV9/carrotsh.git
 
# Change the working directory
cd carrotsh

# Install the dependencies
npm install

# Start the server
node index.js
```

<br />

## Configuration
carrotsh uses [config.json](https://github.com/AnnikaV9/carrotsh/blob/master/config.json) as the primary configuration file.

Available options:
 - port: The port the server should listen on.
 - shell: Path to the shell executable.
 - shell_timeout: The max age (ms) of the spawned shell session.
 - python_path: Path to your python interpreter.
 - salt: The password hashing salt.

<br />

Setting a password:

`npm install` will run [setpass.py](https://github.com/AnnikaV9/carrotsh/blob/master/setpass.py) initially, but you will have to run it again if you change the password salt:
```
python3 setpass.py
```

<br />
<br />
<br />

**Note:** Before using carrotsh in production, it is highly recommended to enable TLS support by using a reverse proxy like [ngnix](https://github.com/nginx/nginx).
