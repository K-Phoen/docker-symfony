from fabric.api import task, local

@task
def up():
    local('fig up -d')

    # register web backend into hipache
    if hipache_has_frontend('test_app.loc'):
        unregister_all_backends('test_app.loc')

    local('fig run rediscli rpush frontend:test_app.loc test_app')
    backend_containers = get_container_ids('web')
    register_backend_containers('test_app.loc', backend_containers)

@task
def scale(service, number):
    """
    @todo: rewrite. Fig kills the containers before I can unregister them from
    hipache
    """

    old_containers = get_container_ids(service)
    # once containers are deleted, retrieving their IP inst' possible so we do
    # it now
    ips_map = {cid: get_container_ip(cid)  for cid in old_containers}

    local('fig scale %s=%s' % (service, number))

    current_containers = get_container_ids(service)
    added_containers = set(current_containers) - set(old_containers)
    removed_containers = set(old_containers) - set(current_containers)

    # register new backends
    register_backend_containers('test_app.loc', added_containers)

    # unregister stopped backends
    for cid in removed_containers:
        unregister_backend('test_app.loc', ips_map[cid])


def register_backend_containers(domain, containers_ids):
    for container_id in containers_ids:
        ip = get_container_ip(container_id)
        register_backend(domain, ip)

def register_backend(domain, ip):
    local('fig run --rm rediscli rpush frontend:%s http://%s:80' % (domain, ip))

def unregister_backend(domain, ip):
    local('fig run --rm rediscli lrem frontend:%s 0 http://%s:80' % (domain, ip))

def unregister_all_backends(domain):
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
