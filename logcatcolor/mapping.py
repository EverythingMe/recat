__author__ = 'rotem'


class MappingFetcher():
    """
    A mapping file auto downloader (not yet implemented)
    """

    def __init__(self, package, local_file=None):
        self.package = package
        self.local_file = local_file

    def get_app_version(self):
        """
        TODO - extract app version automatically.
        """
        return None

    def get_mapping_file(self):
        """
        # TODO - auto download mapping file from a file server by supplying a path template
        :return:
        """
        if self.local_file:
            print("Local mapping file supplied in arguments")
            return self.local_file

        return None
