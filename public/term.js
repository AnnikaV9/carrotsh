const term = new Terminal({
    theme:{
        background:"#181a1b"
    }
});
const socket = new WebSocket(`${document.location.protocol === "http:" ? "ws" : "wss"}://${document.location.host }/ws/`);
const websocketAddon = new AttachAddon.AttachAddon(socket);
const resizeAddon = new FitAddon.FitAddon();
term.loadAddon(websocketAddon);
term.loadAddon(resizeAddon);
term.open(document.getElementById("terminal"));
resizeAddon.fit();
socket.addEventListener("open", () => {
    socket.send(`{"columns": ${term.cols}, "rows": ${term.rows}}`)
});
window.addEventListener("resize", () => {
    resizeAddon.fit()
    socket.send(`{"columns": ${term.cols}, "rows": ${term.rows}}`)
})
