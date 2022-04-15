console.log("carrotsh v0.3.2\n");

const fs = require("fs");
const express = require("express");
const http = require("http");
const https = require("https");
const ws = require("ws");
const pty = require("node-pty");

const indexPage = fs.readFileSync("index.html");
const serverConfig = JSON.parse(fs.readFileSync("config.json"));

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
  console.log("Warning: HTTPS is disabled. Connections to this instance will not be secure.");
}

const WebsocketServer = new ws.Server({server: server, location: "/ws/"});

app.use("/public", express.static('public'));

WebsocketServer.on("connection", (connection, req) => {
  var dateTime = new Date()
  console.log(dateTime, "- Connection from ", req.socket.remoteAddress)
  const term = pty.spawn(serverConfig["python_path"], ["login.py", req.socket.remoteAddress], { name: "xterm-color" });
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
console.log("Listening on port %s\n---", serverConfig["port"]);
