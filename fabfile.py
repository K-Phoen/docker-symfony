from os.path import basename, abspath
from itertools import islice
from time import sleep
from fabric.api import task, local, run, cd

BOOT_WAIT_DELAY = 10 # seconds
STOP_WAIT_DELAY = 5  # seconds

@task
def build():
    project_name = basename(abspath('.'))

    # build app
    local('git archive --format tar --prefix %s/ HEAD | (cd /tmp && tar xf -)' % project_name)

    # install vendors
    local('docker run --rm -v /tmp/%s:/srv --env-file=env-dist -e "SYMFONY_ENV=prod" willdurand/buildtools composer install --no-dev --optimize-autoloader --prefer-dist' % project_name)

    # remove useless files
    local('rm /tmp/%s/web/app_dev.php' % project_name)

    # build container
    local('fig -p %s build app' % project_name)

@task
def up():
    local('fig up -d')

    # wait for the services in the containers to start
    sleep(BOOT_WAIT_DELAY)

    # register web backend into hipache
    if hipache_has_frontend('test_app.loc'):
        unregister_all_backends('test_app.loc')

    rediscli('rpush frontend:test_app.loc test_app')
    backend_containers = get_container_ids('web')
    register_backend_containers('test_app.loc', backend_containers)

@task
def scale(service, number):
    if service != 'web':
        raise NotImplementedError('Only the "web" service can be scaled for now')

    number = int(number)
    old_containers = get_container_ids(service)

    # nothing to do
    if len(old_containers) == number:
        return

    if len(old_containers) < number:
        start_new_backends(number - len(old_containers))
    else:
        stop_old_backends(len(old_containers) - number)


def stop_old_backends(number, remove=False, wait=STOP_WAIT_DELAY):
    # retrieve the container IDs to remove
    containers_to_remove = take(number, get_container_ids('web'))

    # unregister them from hipache
    for cid in containers_to_remove:
        unregister_backend('test_app.loc', get_container_ip(cid))

    # wait a bit so that they have time to handle the ongoing requests
    sleep(wait)

    # and stop them
    local('docker stop %s' % ' '.join(containers_to_remove))

    # now we can safely remove them
    if remove:
        local('docker rm %s' % ' '.join(containers_to_remove))

def start_new_backends(number):
    old_containers = get_container_ids('web')

    # create the new containers
    local('fig scale web=%d' % (len(old_containers) + number))

    # retrieve the created container IDs
    current_containers = get_container_ids('web')
    added_containers = set(current_containers) - set(old_containers)

    # wait for the services in the containers to start
    sleep(BOOT_WAIT_DELAY)

    # register new backends
    register_backend_containers('test_app.loc', added_containers)

def register_backend_containers(domain, containers_ids):
    for container_id in containers_ids:
        ip = get_container_ip(container_id)
        register_backend(domain, ip)

def rediscli(command, redis_service_name='hipache', capture=False):
    redis_cid = get_container_id(redis_service_name)

    return local('docker exec %s redis-cli %s' % (redis_cid, command), capture=capture)

def register_backend(domain, ip):
    rediscli('rpush frontend:%s http://%s:80' % (domain, ip))

def unregister_backend(domain, ip):
    rediscli('lrem frontend:%s 0 http://%s:80' % (domain, ip))

def unregister_all_backends(domain):
    rediscli('ltrim frontend:%s 0 -1' % domain)

def get_container_id(name):
    return get_container_ids(name)[0]

def get_container_ids(name):
    result = local('docker ps | grep %s | cut -d " " -f1' % name, capture=True)

    return result.stdout.split()

def get_container_ip(container_id):
    result = local("docker inspect --format '{{ .NetworkSettings.IPAddress }}' %s" % container_id, capture=True)

    return result.stdout

def hipache_has_frontend(domain):
    result = rediscli('llen frontend:%s' % domain, capture=True)

    return result != "(integer) 0"

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
