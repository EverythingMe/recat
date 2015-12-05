"""
logcat-color

Copyright 2012, Marshall Culpepper
Licensed under the Apache License, Version 2.0

Layouts for mapping logcat log data into a colorful terminal interface
"""
from colorama import Fore, Back, Style
from lxml.etree import strip_tags
from logcatcolor.column import *
from logcatcolor.format import Format
import re
from cStringIO import StringIO

def layout(cls):
    Layout.TYPES[cls.NAME] = cls
    return cls

class Layout(object):
    TYPES = {}
    MARKER_LAYOUT = Fore.WHITE + Back.BLACK + Style.DIM + "%s" + Style.RESET_ALL

    def __init__(self, config=None, profile=None, width=2000, tag_prefixes=[], retracer=None):
        self.columns = []
        self.config = config
        self.profile = profile
        self.tag_prefixes = tag_prefixes
        self.width = width
        self.retracer = retracer

        self.total_column_width = 0
        if self.COLUMNS:
            # first get the total column width, then construct each column
            for ColumnType in self.COLUMNS:
                if config:
                    self.total_column_width += config.get_column_width(ColumnType)
                else:
                    self.total_column_width += ColumnType.DEFAULT_WIDTH

            for ColumnType in self.COLUMNS:
                column = ColumnType(self)
                self.columns.append(column)

        self.column_count = len(self.columns)

    def layout_marker(self, line):
        return self.MARKER_LAYOUT % line

    def layout_data(self, data):
        formatted = StringIO()
        for index in range(0, self.column_count):
            column = self.columns[index]
            if self.retracer:
                if column.NAME is 'tag':
                    data[column.NAME] = self.retracer.tags_retracer.deobfuscate(data[column.NAME], True)
                elif column.NAME is 'message':
                    data[column.NAME] = self.retracer.basic_retracer.deobfuscate(data[column.NAME], False)
            formatted.write(column.format(data[column.NAME]))
            if index < self.column_count - 1:
                formatted.write(" ")

        return formatted.getvalue()

    def strip_tag(self, tag):
        for prefix in self.tag_prefixes:
            if tag.startswith(prefix + '.'):
                tag = tag[0: tag.find('.')] + tag[tag.rfind('.'): len(tag)]

        return tag

@layout
class RawLayout(Layout):
    NAME = "raw"
    COLUMNS = None

    def layout_marker(self, line):
        return line

    def layout_data(self, data):
       return data["line"]

@layout
class BriefLayout(Layout):
    NAME = "brief"
    COLUMNS = (PIDColumn, TagColumn, PriorityColumn, MessageColumn)

@layout
class ProcessLayout(Layout):
    NAME = "process"
    COLUMNS = BriefLayout.COLUMNS

@layout
class TagLayout(Layout):
    NAME = "tag"
    COLUMNS = (TagColumn, PriorityColumn, MessageColumn)

@layout
class ThreadLayout(Layout):
    NAME = "thread"
    COLUMNS = (PIDColumn, TIDColumn, PriorityColumn, MessageColumn)

@layout
class TimeLayout(Layout):
    NAME = "time"
    COLUMNS = (DateColumn, TimeColumn, ) + BriefLayout.COLUMNS

@layout
class ThreadTimeLayout(Layout):
    NAME = "threadtime"
    COLUMNS = (DateColumn, TimeColumn, PIDColumn, TIDColumn, TagColumn, PriorityColumn, MessageColumn)

@layout
class LongLayout(Layout):
    NAME = "long"
    COLUMNS = ThreadTimeLayout.COLUMNS
