import pyretrace

__author__ = 'rotem'


class Retracer():
    """
    a pyretrace wrapper, managing multiple instances
    """

    def __init__(self, mapping_file, tag_prefixes):
        basic_retrace_regex = '(?:.*?\\bat\s+%c\.%m\s*\(.*?(?::%l)?\)\s*)|(?:(?:.*?[:"]\s+)?%c(?::.*)?)'

        # regex_list.append(basic_retrace_regex)
        # regex_list.append('.*%c.*')

        self.basic_retracer = pyretrace.Retrace(mapping_file=mapping_file, regular_expression=basic_retrace_regex)


        tag_prefix_regex = '.*%s\.+%%c.*'
        regex_list = []
        for tagprefix in tag_prefixes:
            regex_list.append(tag_prefix_regex % tagprefix)

        # add tag prefixes to pyretrace pattern map
        self.tags_retracer = pyretrace.Retrace(mapping_file=mapping_file, regular_expression='|'.join(regex_list))



