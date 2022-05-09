module.exports = {
    apps : [{
      name        : "carrotsh",
      script      : "./server/server.js",
      instances   : 1,
      autorestart : false,
      exec_mode   : "fork",
      watch       : false,
      error_file  : "./pm2_logs/err.log",
      out_file    : "./pm2_logs/out.log"
    }]
};
