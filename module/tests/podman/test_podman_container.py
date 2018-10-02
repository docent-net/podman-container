import unittest

from ansible.modules.cloud.oci.podman_container import TaskParameters


class TestTaskParameters(unittest.TestCase):
    """Unit tests for TaskParameters."""

    def test_set_default_parameters(self):
        """
        Ensure setting default params works like expected
        """
        task_params = TaskParameters.__new__(TaskParameters)
        task_params._set_default_parameters()

        self.assertEqual(task_params.image, False)