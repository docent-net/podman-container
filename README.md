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

- Python 3 (no Python bindings for Valink for Py < 3))
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
  
## Examples

```bash
- name: Create nginx container
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