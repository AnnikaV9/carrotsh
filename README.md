# carrotsh
A simple and lightweight server that allows clients to connect and launch a shell remotely through a browser. Uses [xterm.js](https://github.com/xtermjs/xterm.js/) for the frontend and [express](https://github.com/expressjs/express) for the backend.

<br />

## Requirements
 - node.js
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
[config.json](https://github.com/AnnikaV9/carrotsh/blob/master/config.json) should be used as the config file.

Available options:
 - port: The port the server should listen on.
 - shell: Path to the shell executable.
 - salt: The password hashing salt.



Setting a password:

`npm install` will run `setpass.py` initially, however you will have to run it again if you change the password salt:
```
python3 setpass.py
```

