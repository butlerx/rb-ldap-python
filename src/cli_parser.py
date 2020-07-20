"""Command Line Interface generator and dependency injection"""
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    HelpFormatter,
    Namespace,
)
from asyncio import get_event_loop
from inspect import Parameter, signature
from typing import Any, Callable, Dict, List, Optional

import yaml
from typing_inspect import get_origin


# Fixes https://bugs.python.org/issue9571
class ArgumentParserShim(ArgumentParser):
    def _get_values(self, action, arg_strings):
        if arg_strings and arg_strings[0] == "--":
            arg_strings = arg_strings[1:]
        # noinspection PyProtectedMember
        return super(ArgumentParserShim, self)._get_values(action, arg_strings)


class Program(ArgumentParserShim):
    """
    Constructs an argument parser and command runner

    :param prog: Name of the program, as referred to on the command line
    :param description: Short description of the program displayed at the top of help
    :param version: String representation without the leading "v" e.g. "1.0.0"
    :param author: String of program author
    :param bootstrap: function to be called after args are parsed
    :param bootstrap_resv: list of reserved argurements that will be in globals
    :ivar globals: Internal globals to be injected in to commands
    :ivar parsed_args: The parsed args, populated after calling parse()
    """

    def __init__(
        self,
        prog: str,
        description: str,
        version: str,
        author: str,
        bootstrap: Callable = None,
        bootstrap_resv: List[str] = [],
        **kwargs,
    ):
        super(Program, self).__init__(
            prog=prog,
            description=description,
            formatter_class=ArgumentDefaultsHelpFormatter,
            epilog=f"Built by {author}",
            **kwargs,
        )
        self.parsed_args: Optional[Namespace] = None

        self.add_argument(
            "--version",
            "-v",
            help="Show the version",
            action="version",
            version="%(prog)s v{}".format(version),
        )

        self.subparser = self.add_subparsers(
            title="command",
            help="Command to run",
            metavar="COMMAND",
            dest="cmd_name",
            parser_class=ArgumentParserShim,
        )
        self.subparser.required = True
        self.bootstrap = bootstrap or (lambda _: {})
        self.reserved_args = bootstrap_resv
        self.globals: Dict[str, Any] = {}
        self._register_args(
            self,
            self.bootstrap,
            yaml.load(self.bootstrap.__doc__, Loader=yaml.SafeLoader),
        )

    def add_command(self, command: Callable) -> "Program":
        """
        Adds a command to the cli. Pass the uninitialised class
        :param command: function to add
        """
        doc = command.__doc__.split("---")
        help_dict = yaml.load(doc[1], Loader=yaml.SafeLoader) if len(doc) >= 2 else {}
        cmd_parser = self.subparser.add_parser(
            command.__name__.replace("_", "-"),
            description=doc[0].strip(),
            help=doc[0].strip(),
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        cmd_parser.set_defaults(cmd=command)
        self._register_args(cmd_parser, command, help_dict)
        return self

    def parse_args(
        self, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None
    ) -> "Program":
        """
        Parse raw command line arguments

        :param args: arguments list. Defaults to sys.argv[1:]
        :param namespace: Namespace to use to store arguments
        """
        self.parsed_args = super().parse_args(args, namespace)
        self.globals = self.bootstrap(
            **self._get_func_args(self.bootstrap, self.parsed_args)
        )
        return self

    def run_command(self, is_async: bool = False) -> int:
        """
        Initialise the command with the parsed args plus any extra kwargs

        :param is_async: If the function being run is async
        :return: Return code from the command's run method
        """

        kwargs = self._get_func_args(self.parsed_args.cmd, self.parsed_args)
        if is_async:
            loop = get_event_loop()
            return loop.run_until_complete(self.parsed_args.cmd(**kwargs))
        return self.parsed_args.cmd(**kwargs)

    def _get_func_args(self, func: Callable, parsed_args: Namespace) -> dict:
        kwargs = {}
        args = vars(parsed_args)
        for arg in list(signature(func).parameters.values()):
            if arg.name in self.reserved_args:
                kwargs.update({arg.name: self.globals[arg.name]})
            else:
                kwargs.update({arg.name: args[arg.name]})
        return kwargs

    def _register_args(self, parser, func: Callable, help_dict: Dict[str, str]):
        for arg in list(signature(func).parameters.values()):
            if arg.name in self.reserved_args:
                continue
            if arg.kind == Parameter.KEYWORD_ONLY:
                if arg.annotation == bool and arg.default is False:
                    parser.add_argument(
                        f"--{arg.name.replace('_', '-')}",
                        help=help_dict.get(arg.name, None),
                        action="store_true",
                    ),
                elif arg.annotation == bool and arg.default is True:
                    parser.add_argument(
                        f"--{arg.name.replace('_', '-')}",
                        help=help_dict.get(arg.name, None),
                        action="store_false",
                    ),
                elif arg.annotation == list or get_origin(arg.annotation) == list:
                    parser.add_argument(
                        f"--{arg.name.replace('_', '-')}",
                        help=help_dict.get(arg.name, None),
                        nargs="+",
                        default=arg.default,
                    )
                else:
                    parser.add_argument(
                        f"--{arg.name.replace('_', '-')}",
                        help=help_dict.get(arg.name, None),
                        type=arg.annotation,
                        default=arg.default,
                    )
            elif arg.kind in [
                Parameter.POSITIONAL_OR_KEYWORD,
                Parameter.POSITIONAL_ONLY,
            ]:
                if arg.annotation == list or get_origin(arg.annotation) == list:
                    parser.add_argument(
                        arg.name.replace("_", "-"),
                        help=help_dict.get(arg.name, None),
                        nargs="+",
                        default=arg.default,
                    )
                else:
                    parser.add_argument(
                        arg.name.replace("_", "-"),
                        help=help_dict.get(arg.name, None),
                        type=arg.annotation,
                        default=arg.default,
                    )
