FROM debian:wheezy
MAINTAINER Kévin Gomez <contact@kevingomez.fr>

# Set correct environment variables.
ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

# essential tools
RUN apt-get update -y
RUN apt-get install -y curl wget git zsh supervisor

# additionnal repositories
RUN echo "deb http://packages.dotdeb.org wheezy all\ndeb-src http://packages.dotdeb.org wheezy all" > /etc/apt/sources.list.d/dotdeb.list
RUN wget http://www.dotdeb.org/dotdeb.gpg && apt-key add dotdeb.gpg
RUN apt-get update -y

# Use supervisord as init system
ADD config/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
CMD ["/usr/bin/supervisord"]

# install PHP
RUN apt-get install -y --allow-unauthenticated php5 php5-cli php5-sqlite php5-curl php5-gd php5-mcrypt php5-intl php5-memcached php5-xsl php5-xdebug php5-fpm

RUN sed -e 's/;daemonize = yes/daemonize = no/' -i /etc/php5/fpm/php-fpm.conf
RUN sed -e 's/;listen\.owner/listen.owner/' -i /etc/php5/fpm/pool.d/www.conf
RUN sed -e 's/;listen\.group/listen.group/' -i /etc/php5/fpm/pool.d/www.conf
ADD config/php_custom.ini /etc/php5/mods-available/custom.ini
RUN php5enmod custom

# install nginx
RUN apt-get install -y nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
ADD config/vhost.conf /etc/nginx/sites-available/default

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
