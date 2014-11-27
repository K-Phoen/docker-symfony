Symfony development environment using Docker
============================================

My Symfony development environment using [Docker](https://www.docker.com/) and
orchestrated with [Fig](http://fig.sh/).

## What's inside

The environment will set up two containers:
  * one with Nginx and PHP 5 FPM (`web`) ;
  * another with MySQL (`db`).

[Composer](https://getcomposer.org/) is also globally installed in the `web`
container. The following alias can be used to ease the use from the host.

```bash
alias composer="fig run web composer"
```

## Usage

Building the images:

```bash
fig build
```

Starting the containers

```bash
fig up
```
