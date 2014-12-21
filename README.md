Symfony development environment using Docker
============================================

My Symfony development environment using [Docker](https://www.docker.com/) and
orchestrated with [Fig](http://fig.sh/).

## What's inside

The environment will set up three containers:
  * one with Nginx and PHP 5 FPM (`web`) ;
  * and another one with MySQL (`db`).

**NOTE:** this setup integrates well with
[willdurand](https://github.com/willdurand/)'s
[docker-buildtools](https://github.com/willdurand/docker-buildtools)
container.

You can create the following aliases to easily access your build tools:

```bash
alias composer="docker run --rm -v $(pwd)/code:/srv willdurand/buildtools composer"
```

```bash
alias bundle="docker run --rm -v $(pwd)/code:/srv willdurand/buildtools bundle"
```

etc.

## Usage

Building the images:

```bash
fig build
```

Starting the containers

```bash
fig up
```
