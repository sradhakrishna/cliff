"""Discover and lookup command plugins.
"""

import logging

import pkg_resources


LOG = logging.getLogger(__name__)


class CommandManager(object):
    """Discovers commands and handles lookup based on argv data.
    """
    def __init__(self, namespace):
        self.commands = {}
        self.namespace = namespace
        self._load_commands()

    def _load_commands(self):
        for ep in pkg_resources.iter_entry_points(self.namespace):
            LOG.debug('found command %r', ep.name)
            self.commands[ep.name.replace('_', ' ')] = ep
        return

    def __iter__(self):
        return iter(self.commands.items())

    def find_command(self, argv):
        """Given an argument list, find a command and
        return the processor and any remaining arguments.
        """
        search_args = argv[:]
        name = ''
        while search_args:
            if search_args[0].startswith('-'):
                raise ValueError('Invalid command %r' % search_args[0])
            next_val = search_args.pop(0)
            name = '%s %s' % (name, next_val) if name else next_val
            if name in self.commands:
                cmd_ep = self.commands[name]
                cmd_factory = cmd_ep.load()
                return (cmd_factory, name, search_args)
        else:
            raise ValueError('Did not find command processor for %r' %
                             (argv,))