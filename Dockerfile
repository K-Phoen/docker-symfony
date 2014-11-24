# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:0.9.15

# Set correct environment variables.
ENV HOME /root

# Regenerate SSH host keys. baseimage-docker does not contain any, so you
# have to do that yourself. You may also comment out this instruction; the
# init system will auto-generate one during boot.
#RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# additionnal repositories
RUN add-apt-repository ppa:ondrej/php5
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update

# essential tools
RUN apt-get install -y vim curl wget git zsh

# install PHP and Composer
RUN apt-get install -y --allow-unauthenticated php5 php5-cli php5-sqlite php5-curl php5-gd php5-mcrypt php5-intl php5-memcached php5-xsl php5-xdebug php5-fpm
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN sed -e 's/;daemonize = yes/daemonize = no/' -i /etc/php5/fpm/php-fpm.conf
RUN sed -e 's/;listen\.owner/listen.owner/' -i /etc/php5/fpm/pool.d/www.conf
RUN sed -e 's/;listen\.group/listen.group/' -i /etc/php5/fpm/pool.d/www.conf

RUN mkdir /etc/service/php-fpm
ADD services/php-fpm /etc/service/php-fpm/run

# install nginx
RUN apt-get install -y nginx

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
ADD config/vhost.conf /etc/nginx/sites-available/default

RUN mkdir /etc/service/nginx
ADD services/nginx /etc/service/nginx/run

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# generate an insecure SSH key
RUN /usr/sbin/enable_insecure_key
