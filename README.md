Symfony development environment using Docker
============================================

My Symfony development environment using [Docker](https://www.docker.com/) and
orchestrated with [Fig](http://fig.sh/).

## What's inside

The environment will set up three containers:
  * one with Nginx and PHP 5 FPM (`web`) ;
  * one with MySQL (`db`) ;
  * and a last one with build tools such as [Composer](https://getcomposer.org/) (`tools`).

```bash
alias composer="fig run tools composer"
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
