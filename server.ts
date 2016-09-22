import Hapi = require("hapi");
let rethink = require("rethinkdbdash")();

let server = new Hapi.Server();
server.connection({port: 3000});

server.route({
  method: 'GET',
  path: '/',
  handler(request: Hapi.Request, reply: Hapi.IReply) {
    reply('Hello, world!');
  }
});

server.route({
  method: 'GET',
  path: '/{name}',
  handler(request: Hapi.Request, reply: Hapi.IReply) {
    reply(`Hello, ${encodeURIComponent(request.params['name'])}`);
  }
});

server.start(() => {
  console.log(`Server running at ${server.info.uri}`);
});