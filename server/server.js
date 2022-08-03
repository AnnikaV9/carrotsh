/* 
Backend server that connects with clients and then spawns a python
pty process that runs ogin/login.py 
*/

const fs = require("fs");
const express = require("express");
const http = require("http");
const https = require("https");
const ws = require("ws");
const pty = require("node-pty");
const yaml = require("js-yaml");

const indexPage = fs.readFileSync("server/index.html");
const serverConfig = yaml.load(fs.readFileSync("config.yaml", "utf8"));

const app = express();
var server;

if (serverConfig["https"]) {
  server = new https.createServer({
    cert: fs.readFileSync(serverConfig["https_options"]["path_to_cert"]),
    key: fs.readFileSync(serverConfig["https_options"]["path_to_key"])
  }, app);
}
else {
  server = new http.createServer(app);
}

const WebsocketServer = new ws.Server({server: server, location: "/ws/"});

app.use("/public", express.static('public'));

WebsocketServer.on("connection", (connection, req) => {
  var dateTime = new Date()
  console.log(dateTime, "- Connection from ", req.socket.remoteAddress)
  const term = pty.spawn(serverConfig["python_path"], ["login/login.py", req.socket.remoteAddress], { name: "xterm-color" });
  setTimeout(() => term.kill(), serverConfig["shell_timeout_milliseconds"]);
  setInterval(() => {
    try{
      connection.ping("heartbeat");
    } catch (err) {}
  }, 15000);
  term.on("data", (data) => {
    try {
      connection.send(data);
    } catch (err) {}
  });
  connection.on("message", (data) => term.write(data));
});

app.get("/", (req, res) => {
  res.setHeader("Content-Type", "text/html");
  res.send(indexPage);
});

server.listen(serverConfig["port"]);
