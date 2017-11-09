"""
Modified PyYAML that supports !import keyword
=============================================
"""

import os.path
import yaml


IMPORT_TAG = "!import"


class ImportLoader(yaml.Loader):
    """
    Override default loader to support inclusion of YAML files.

    YAML file paths should be relative to original stream.

    https://stackoverflow.com/a/9577670/2855071
    """
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(ImportLoader, self).__init__(stream)

    def import_(self, node):
        """
        :param node: YAML file to be importd relative to original stream
        :returns: YAML file for inclusion
        :rtype: dict
        """
        yamal_name = os.path.join(self._root, self.construct_scalar(node))

        with open(yamal_name, 'r') as yamal_file:
            return yaml.load(yamal_file, ImportLoader)

ImportLoader.add_constructor(IMPORT_TAG, ImportLoader.import_)

def load(stream):
    """
    :param stream: YAML file to be loaded
    :type stream: Stream obj. File or str

    :returns: YAML file as nested dictionary
    :rtype: dict
    """
    return yaml.load(stream, ImportLoader)