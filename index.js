const fs = require("fs");
const express = require("express");
const ws = require("express-ws");
const pty = require("node-pty");

const indexPage = fs.readFileSync("index.html");
const serverConfig = JSON.parse(fs.readFileSync("config.json"));

const app = express();

app.use("/public", express.static('public'));
ws(app);

app.ws("/ws", (ws) => {
  const term = pty.spawn(serverConfig["python_path"], ["login.py"], { name: "xterm-color" });
  setTimeout(() => term.kill(), 3600000);
  setInterval(() => {
    try{
      ws.ping("heartbeat");
    } catch (err) {}
  }, 15000);
  term.on("data", (data) => {
    try {
      ws.send(data);
    } catch (err) {}
  });
  ws.on("message", (data) => term.write(data));
});

app.get("/", (req, res) => {
  res.setHeader("Content-Type", "text/html");
  res.send(indexPage);
});

app.listen(serverConfig["port"], "0.0.0.0");
