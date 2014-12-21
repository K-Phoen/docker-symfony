from fabric.api import task, local

@task
def up():
    local('fig up -d')

    # register web backend into hipache
    if hipache_has_frontend('test_app.loc'):
        unregister_backends('test_app.loc')

    local('fig run rediscli rpush frontend:test_app.loc test_app')
    backend_containers = get_container_ids('web')
    register_backend_containers('test_app.loc', backend_containers)

@task
def scale(service, number):
    old_containers = get_container_ids(service)

    # create new containers
    local('fig scale %s=%s' % (service, number))

    current_containers = get_container_ids(service)
    new_containers = set(current_containers) - set(old_containers)

    register_backend_containers('test_app.loc', new_containers)


def register_backend_containers(domain, containers_ids):
    for container_id in containers_ids:
        ip = get_container_ip(container_id)
        register_backend(domain, ip)

def register_backend(domain, ip):
    local('fig run --rm rediscli rpush frontend:%s http://%s:80' % (domain, ip))

def unregister_backends(domain):
    local('fig run --rm rediscli ltrim frontend:%s 0 -1' % domain)

def get_container_ids(name):
    result = local('docker ps | grep %s | cut -d " " -f1' % name, capture=True)

    return result.stdout.split()

def get_container_ip(container_id):
    result = local("docker inspect --format '{{ .NetworkSettings.IPAddress }}' %s" % container_id, capture=True)

    return result.stdout

def hipache_has_frontend(domain):
    result = local('fig run --rm rediscli llen frontend:%s' % domain, capture=True)

    return result != "(integer) 0"

