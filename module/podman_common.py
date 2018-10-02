import os

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.parsing.convert_bool import BOOLEANS_TRUE, BOOLEANS_FALSE

HAS_VARLINK = False
HAS_VARLINK_ERROR = None
DEFAULT_VARLINK_SOCKET = 'unix:/run/podman/io.podman'

# TODO: handling Varlink, Podman versions
try:
    import varlink
    HAS_VARLINK = True
#     # from docker import __version__ as docker_version
#     # from docker.errors import APIError, TLSParameterError, NotFound
#     # from docker.constants import DEFAULT_DOCKER_API_VERSION
#
#     if LooseVersion(docker_version) >= LooseVersion('3.0.0'):
#         HAS_DOCKER_PY_3 = True
#         from docker import APIClient as Client
#         from docker.types import Ulimit, LogConfig
#     elif LooseVersion(docker_version) >= LooseVersion('2.0.0'):
#         HAS_DOCKER_PY_2 = True
#         from docker import APIClient as Client
#         from docker.types import Ulimit, LogConfig
#     else:
#         from docker import Client
#         from docker.utils.types import Ulimit, LogConfig
#
except ImportError as exc:
    HAS_VARLINK_ERROR = str(exc)
    HAS_VARLINK = False


if not HAS_VARLINK:
    # No varlink. Create a place holder client to allow
    # instantiation of AnsibleModule and proper error handing
    class PodmanClient(object):
        def __init__(self, **kwargs):
            pass

    class APIError(Exception):
        pass
else:
    class PodmanClient(object):
        def __init__(self, **kwargs):
            pass

    class APIError(Exception):
        pass



def sanitize_result(data):
    """Sanitize data object for return to Ansible.

    This function sanitizes data structures by recursively converting
    everything derived from dict to dict and everything derived from list (and tuple)
    to a list.
    """
    if isinstance(data, dict):
        return dict((k, sanitize_result(v)) for k, v in data.items())
    elif isinstance(data, (list, tuple)):
        return [sanitize_result(v) for v in data]
    else:
        return data


class PodmanBaseClass(object):

    def __init__(self):
        self.debug = False

    def log(self, msg, pretty_print=False):
        pass
        # if self.debug:
        #     log_file = open('podman.log', 'a')
        #     if pretty_print:
        #         log_file.write(json.dumps(msg, sort_keys=True, indent=4, separators=(',', ': ')))
        #         log_file.write(u'\n')
        #     else:
        #         log_file.write(msg + u'\n')


class AnsiblePodmanClient(PodmanClient):

    def __init__(self, argument_spec=None, supports_check_mode=False,
                 required_if=None):

        self.module = AnsibleModule(
            argument_spec=argument_spec,
            supports_check_mode=supports_check_mode,
            required_if=required_if)

        if not HAS_VARLINK:
            self.fail("Failed to import varlink - %s. Try `pip install varlink` (Python 3.x)" % HAS_DOCKER_ERROR)

        # TODO: when version handling is done
        # if LooseVersion(docker_version) < LooseVersion(MIN_DOCKER_VERSION):
        #     self.fail("Error: docker / docker-py version is %s. Minimum version required is %s." % (docker_version,
        #                                                                                             MIN_DOCKER_VERSION))
        self.debug = self.module.params.get('debug')
        self.check_mode = self.module.check_mode
        self._connect_params = {
            'PODMAN_VARLINK_SOCKET': DEFAULT_VARLINK_SOCKET
        }

        try:
            super(AnsiblePodmanClient, self).__init__(**self._connect_params)
        except APIError as exc:
            self.fail("Podman API error: %s" % exc)
        except Exception as exc:
            self.fail("Error connecting: %s" % exc)

    def log(self, msg, pretty_print=False):
        pass
        # if self.debug:
        #     log_file = open('docker.log', 'a')
        #     if pretty_print:
        #         log_file.write(json.dumps(msg, sort_keys=True, indent=4, separators=(',', ': ')))
        #         log_file.write(u'\n')
        #     else:
        #         log_file.write(msg + u'\n')

    def fail(self, msg):
        self.module.fail_json(msg=msg)

    @staticmethod
    def _get_value(param_name, param_value, env_variable, default_value):
        if param_value is not None:
            # take module parameter value
            if param_value in BOOLEANS_TRUE:
                return True
            if param_value in BOOLEANS_FALSE:
                return False
            return param_value

        if env_variable is not None:
            env_value = os.environ.get(env_variable)
            if env_value is not None:
                # take the env variable value
                if env_value in BOOLEANS_TRUE:
                    return True
                if env_value in BOOLEANS_FALSE:
                    return False
                return env_value

        # take the default
        return default_value

    def get_container(self, name=None):
        '''
        Lookup a container and return the inspection results.
        '''
        return 123
        if name is None:
            return None

        search_name = name
        if not name.startswith('/'):
            search_name = '/' + name

        result = None
        try:
            for container in self.containers(all=True):
                self.log("testing container: %s" % (container['Names']))
                if isinstance(container['Names'], list) and search_name in container['Names']:
                    result = container
                    break
                if container['Id'].startswith(name):
                    result = container
                    break
                if container['Id'] == name:
                    result = container
                    break
        except SSLError as exc:
            self._handle_ssl_error(exc)
        except Exception as exc:
            self.fail("Error retrieving container list: %s" % exc)

        if result is not None:
            try:
                self.log("Inspecting container Id %s" % result['Id'])
                result = self.inspect_container(container=result['Id'])
                self.log("Completed container inspection")
            except Exception as exc:
                self.fail("Error inspecting container: %s" % exc)

        return result

    def find_image(self, name, tag):
        pass

    def pull_image(self, name, tag="latest"):
        pass