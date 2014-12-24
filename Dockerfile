FROM busybox:latest
MAINTAINER Kévin Gomez <contact@kevingomez.fr>

ADD . /srv
# use ACL or some other shit.
RUN chmod 777 -R /srv/app/cache
