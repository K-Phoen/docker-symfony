FROM debian:jessie
MAINTAINER Kévin Gomez <contact@kevingomez.fr>

# Set correct environment variables.
ENV DEBIAN_FRONTEND noninteractive

# essential tools
RUN apt-get update -y
RUN apt-get install -y wget git curl

# additionnal repositories
RUN wget -O - http://dl.hhvm.com/conf/hhvm.gpg.key | apt-key add -
RUN echo deb http://dl.hhvm.com/debian jessie main | tee /etc/apt/sources.list.d/hhvm.list

RUN apt-get update -y

# Configure HHVM
RUN apt-get install -y hhvm
ADD config/php.ini /etc/hhvm/php.ini
RUN /usr/bin/update-alternatives --install /usr/bin/php php /usr/bin/hhvm 60

# Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
