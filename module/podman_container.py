#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: podman_container

short_description: manage podman / OCI containers

description:
  - Manage the life cycle of podman containers.

version_added: "2.6"

options:
  force_kill:
    description:
      - Use the kill command when stopping a running container.
    type: bool
    default: 'no'
    aliases:
      - forcekill
  keep_volumes:
    description:
      - Retain volumes associated with a removed container.
    type: bool
    default: 'yes'
  image:
    description:
      - Repository path and tag used to create the container. If an image is not found or pull is true, the image
        will be pulled from the registry. If no tag is included, 'latest' will be used.
  name:
    description:
      - Assign a name to a new container or match an existing container.
      - When identifying an existing container name may be a name or a long or short container ID.
    required: true
  pull:
    description:
       - If true, always pull the latest version of an image. Otherwise, will only pull an image when missing.
    type: bool
    default: 'no'
  state:
    description:
      - 'I(absent) - A container matching the specified name will be stopped and removed. Use force_kill to kill the container
         rather than stopping it. Use keep_volumes to retain volumes associated with the removed container.'
      - 'I(present) - Asserts the existence of a container matching the name and any provided configuration parameters. If no
        container matches the name, a container will be created. If a container matches the name but the provided configuration
        does not match, the container will be updated, if it can be. If it cannot be updated, it will be removed and re-created
        with the requested config. Image version will be taken into account when comparing configuration. To ignore image
        version use the ignore_image option. Use the recreate option to force the re-creation of the matching container. Use
        force_kill to kill the container rather than stopping it. Use keep_volumes to retain volumes associated with a removed
        container.'
      - 'I(started) - Asserts there is a running container matching the name and any provided configuration. If no container
        matches the name, a container will be created and started. If a container matching the name is found but the
        configuration does not match, the container will be updated, if it can be. If it cannot be updated, it will be removed
        and a new container will be created with the requested configuration and started. Image version will be taken into
        account when comparing configuration. To ignore image version use the ignore_image option. Use recreate to always
        re-create a matching container, even if it is running. Use restart to force a matching container to be stopped and
        restarted. Use force_kill to kill a container rather than stopping it. Use keep_volumes to retain volumes associated
        with a removed container.'
      - 'I(stopped) - Asserts that the container is first I(present), and then if the container is running moves it to a stopped
        state. Use force_kill to kill a container rather than stopping it.'
    default: started
    choices:
      - absent
      - present
      - stopped
      - started|
author:
    - "Maciej Lasyk (@docent-net)"

requirements:
    - "python >= 3.5 (Python bindings for Varlink are Py3)"
    - "Podman >= 0.9.1"
    - "varlink >= 27.1.1"
    - "Varlink >= 12 (not tested w/older)"
'''

EXAMPLES = '''
- name: Create Nginx container
  podman_container:
    name: nginx
    image: docker.io/library/nginx

- name: Create and start nginx container
  podman_container:
    name: nginx
    image: docker.io/library/nginx
    state: started

- name: Remove nginx container
  podman_container:
    name: nginx
    state: 
'''

RETURN = '''
podman_container:
    description:
      - Facts representing the current state of the container. Matches the podman inspection output.
      - Note that facts are not part of registered vars but accessible directly.
      - Empty if C(state) is I(absent)
      - If detached is I(False), will include Output attribute containing any output from container run.
    returned: always
    type: dict
    sample: '{
        "Args": [],
        "Config": {
            "AttachStderr": false,
            "AttachStdin": false,
            "AttachStdout": false,
            "Cmd": [
                "/usr/bin/nginx"
            ],
            "Domainname": "",
            "Entrypoint": null,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "ExposedPorts": {
                "443/tcp": {},
                "80/tcp": {}
            },
            "Hostname": "8e47bf643eb9",
            "Image": "nginx:v1",
            "Labels": {},
            "OnBuild": null,
            "OpenStdin": false,
            "StdinOnce": false,
            "Tty": false,
            "User": "",
            "Volumes": {
                "/tmp/nginx-sites/logs/": {}
            },
            ...
    }'
'''

from ansible.module_utils.podman_common import sanitize_result, AnsiblePodmanClient


class AnsiblePodmanClientContainer(AnsiblePodmanClient):

    def __init__(self, **kwargs):
        super(AnsiblePodmanClientContainer, self).__init__(**kwargs)

        pass

class ContainerManager(PodmanBaseClass):
    '''
    Perform container management tasks
    '''

    def __init__(self, client):

        super(ContainerManager, self).__init__()

        self.client = client
        self.parameters = TaskParameters(client)
        self.check_mode = self.client.check_mode
        self.results = {'changed': False, 'actions': []}
        self.diff = {}
        self.facts = {}

        state = self.parameters.state
        if state in ('stopped', 'started', 'present'):
            self.present(state)
        elif state == 'absent':
            self.absent()

        if not self.check_mode and not self.parameters.debug:
            self.results.pop('actions')

        if self.client.module._diff or self.parameters.debug:
            self.results['diff'] = self.diff

        if self.facts:
            self.results['ansible_facts'] = {'podman_container': self.facts}

    def present(self, state):
        pass

    def absent(self):
        pass

    def fail(self, msg, **kwargs):
        pass

    def container_create(self, image, create_parameters):
        pass

    def container_start(self, container_id):
        pass

    def container_remove(self, container_id, link=False, force=False):
        pass

    def container_update(self, container_id, update_parameters):
        pass

    def container_kill(self, container_id):
        pass

    def container_stop(self, container_id):
        pass


def main():
    argument_spec = dict(
        # TODO commented out what's left to be implemented
        # auto_remove=dict(type='bool', default=False),
        # blkio_weight=dict(type='int'),
        # capabilities=dict(type='list'),
        # cap_drop=dict(type='list'),
        # cleanup=dict(type='bool', default=False),
        # command=dict(type='raw'),
        # cpu_period=dict(type='int'),
        # cpu_quota=dict(type='int'),
        # cpuset_cpus=dict(type='str'),
        # cpuset_mems=dict(type='str'),
        # cpu_shares=dict(type='int'),
        # detach=dict(type='bool', default=True),
        # devices=dict(type='list'),
        # dns_servers=dict(type='list'),
        # dns_opts=dict(type='list'),
        # dns_search_domains=dict(type='list'),
        # domainname=dict(type='str'),
        # env=dict(type='dict'),
        # env_file=dict(type='path'),
        # entrypoint=dict(type='list'),
        # etc_hosts=dict(type='dict'),
        # exposed_ports=dict(type='list', aliases=['exposed', 'expose']),
        force_kill=dict(type='bool', default=False, aliases=['forcekill']),
        # groups=dict(type='list'),
        # hostname=dict(type='str'),
        # ignore_image=dict(type='bool', default=False),
        image=dict(type='str'),
        # init=dict(type='bool', default=False),
        # interactive=dict(type='bool', default=False),
        # ipc_mode=dict(type='str'),
        keep_volumes=dict(type='bool', default=True),
        # kernel_memory=dict(type='str'),
        # kill_signal=dict(type='str'),
        # labels=dict(type='dict'),
        # links=dict(type='list'),
        # log_driver=dict(type='str'),
        # log_options=dict(type='dict', aliases=['log_opt']),
        # mac_address=dict(type='str'),
        # memory=dict(type='str', default='0'),
        # memory_reservation=dict(type='str'),
        # memory_swap=dict(type='str'),
        # memory_swappiness=dict(type='int'),
        name=dict(type='str', required=True),
        # network_mode=dict(type='str'),
        # userns_mode=dict(type='str'),
        # networks=dict(type='list'),
        # oom_killer=dict(type='bool'),
        # oom_score_adj=dict(type='int'),
        # output_logs=dict(type='bool', default=False),
        # paused=dict(type='bool', default=False),
        # pid_mode=dict(type='str'),
        # privileged=dict(type='bool', default=False),
        # published_ports=dict(type='list', aliases=['ports']),
        # pull=dict(type='bool', default=False),
        # purge_networks=dict(type='bool', default=False),
        # read_only=dict(type='bool', default=False),
        # recreate=dict(type='bool', default=False),
        # restart=dict(type='bool', default=False),
        # restart_policy=dict(type='str', choices=['no', 'on-failure', 'always', 'unless-stopped']),
        # restart_retries=dict(type='int', default=None),
        # shm_size=dict(type='str'),
        # security_opts=dict(type='list'),
        state=dict(type='str', choices=['absent', 'present', 'started', 'stopped'], default='started'),
        # stop_signal=dict(type='str'),
        # stop_timeout=dict(type='int'),
        # tmpfs=dict(type='list'),
        # trust_image_content=dict(type='bool', default=False),
        # tty=dict(type='bool', default=False),
        # ulimits=dict(type='list'),
        # sysctls=dict(type='dict'),
        # user=dict(type='str'),
        # uts=dict(type='str'),
        # volumes=dict(type='list'),
        # volumes_from=dict(type='list'),
        # volume_driver=dict(type='str'),
        # working_dir=dict(type='str'),
    )

    required_if = [
        ('state', 'present', ['image'])
    ]

    client = AnsiblePodmanClientContainer(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True
    )

    cm = ContainerManager(client)
    client.module.exit_json(**sanitize_result(cm.results))


if __name__ == '__main__':
    main()
