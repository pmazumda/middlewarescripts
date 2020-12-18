const app = require('http');
const port = process.env.port || 4000

const server = app.createServer((req, res) => {
    res.end(`Hi TCGUSER! this is response from application on  port ${port}.`);
});

server.listen(port);
