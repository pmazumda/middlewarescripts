const app = require('http');
const port = process.env.port || 15000 

const server = app.createServer((req, res) => {
    res.end(`Hi user this is response from bheem ohs on port ${port}.`);
});

server.listen(port);
