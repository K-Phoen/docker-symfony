Symfony development environment using Docker
============================================

My Symfony development environment using [Docker](https://www.docker.com/) and
orchestrated with [Fig](http://fig.sh/).

## What's inside

The environment will set up the following containers:
  * `web` with Nginx and PHP 5 FPM ;
  * `memcached` with a Memcached instanced used to store PHP sessions ;
  * `db` with MySQL ;
  * and `hipache` as frontend to the `web` containers.

**NOTE:** this setup integrates well with
[willdurand](https://github.com/willdurand/)'s
[docker-buildtools](https://github.com/willdurand/docker-buildtools)
container.

You can create the following aliases to easily access your build tools:

```bash
alias composer="docker run --rm -v $(pwd)/code:/srv willdurand/buildtools composer --ansi"
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

Starting the containers:

```bash
fab up
```
