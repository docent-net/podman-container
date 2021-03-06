# podman-container

## Synopsis

Ansible module for managing OCI containers with Podman and Varlink (as drop-in replacement for docker_container module)

## History

This module was created during [All Systems Go 2018](https://all-systems-go.io/) 
hackathon. During the conference Dan Walsh's gave a presentation about
[Podman](https://github.com/containers/libpod/) describing it as drop-in
replacement for Docker. The only thing I was missing was an Ansible module
I could use instead of **docker_container** as I ship containers w/Ansible.

## How it works

Podman is a tool for managing OCI containers, containers images 
and pods. It exposes [Varlink](https://varlink.org) API. **podman_container**
module talks to the Podman (w/libpod beneath) via varlink API.

## Requirements

- Python 3.5 (no [Python-Varlink](https://github.com/varlink/python) Bindings for Py < 3, so no support for Py <3 is planned)
- Podman 0.9.1 (not tested w/older)
- Varlink == 12 (not tested w/older)

## Parameters

(not implemented)

- **name** [required]: Assign a name to a new container or match an existing 
  container. When identifying an existing container name may be a name or a long or short container ID. 
- **image**: Repository path and tag used to create the container. If an image 
  is not found or pull is true, the image will be pulled from the registry. If 
  no tag is included, 'latest' will be used.
- **pull**: If true, always pull the latest version of an image. Otherwise, 
  will only pull an image when missing.
- **state** [absent, present, stopped, started]:
- **force_kill**:
- **keep_volumes**: 
  
## Examples

```bash
- name: Create Nginx container
  podman_container:
    name: nginx
    image: docker.io/library/nginx
```

```bash
- name: Create and start nginx container
  podman_container:
    name: nginx
    image: docker.io/library/nginx
    state: started
```

```bash
- name: Remove nginx container
  podman_container:
    name: nginx
    state: absent
```

## Development

Clone ansible repo directly to the root directory of this repo (its contents 
will be excluded as per .gitignore settings). Then create required directories 
and symlinks:

```
mkdir -p ansible/lib/ansible/modules/cloud/oci/
mkdir -p ansible/test/units/modules/cloud/oci/
ln -s ln -s ../../../../module/podman ansible/lib/ansible/modules/cloud/oci/podman_container.py
ln -s ln -s ../../../../module/podman ansible/lib/ansible/module_utils/podman_common.py
ln -s ../../../../../../module/tests/podman/test_podman_container.py ansible/test/units/modules/cloud/oci/test_podman_container.py
```

Now simply follow the development practices described in [developing modules](https://docs.ansible.com/ansible/2.5/dev_guide/developing_modules_general.html)

Generally you should first initialize virtual environment:

```bash
cd podman_container/ansible
mkvirtualenv --python=/usr/bin/python3 ansible-modules-podman-container
pip install -r requirements.txt
```

And now everytime you start your work session simply:

```
. hacking/env-setup
cd ../module
python podman_container.py ../development_helpers/args.json
```

Of course this `. hacking/env-setup` is required only once on the very 
beginning of your work session.

### Testing

This repo also provides unit tests. See **module/tests** directory. Originally
Ansible keeps unit tests for modules in **ansible/test/units/modules/**
directory and that's where you'll find Podman's tests.

In order to run those tests also follow standard Ansible module development
practices described in [developing modules](https://docs.ansible.com/ansible/2.5/dev_guide/developing_modules_general.html).

In a nutshell - first initialize your tests virtual environment:

```
cd podman_container/ansible
mkvirtualenv --python=/usr/bin/python3 ansible-modules-podman-container-tests
pip3 install -r ./test/runner/requirements/units.txt
```

And every time you wanna work on tests simply run:
```
. hacking/env-setup
ansible-test units --python 3.5

``` 

Of course this `. hacking/env-setup` is required only once on the very 
beginning of your work session.