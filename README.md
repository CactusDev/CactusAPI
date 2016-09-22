Hapi-TS-Experiment
=====================
> Experimenting using TypeScript with Hapi

## Setup
1. Run `git clone https://github.com/dustinspecker/hapi-ts-experiment` to clone the repository.
1. Run `npm i` to install dependencies.
1. Run `npm i -g tsd typescript@^1.5.0-beta` to install TSD and TypeScript.
1. Run `tsd reinstall --save` to download typings.
1. Run `tsc` to compile TypeScript.
1. Run `node server` to start the Hapi Server on port 3000.

## Routes

`GET /` returns "Hello, world!"

`GET /{name}` returns "Hello, {name}!"