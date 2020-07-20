"""Command Line Interface generator and dependency injection"""
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
    RawDescriptionHelpFormatter,
)
from asyncio import get_event_loop
from inspect import Parameter, iscoroutinefunction, signature
from typing import Any, Callable, Dict, List, Optional

from docstring_parser import parse
from typing_inspect import get_origin


# Fixes https://bugs.python.org/issue9571
class ArgumentParserShim(ArgumentParser):
    """shim or argparser"""

    def _get_values(self, action, arg_strings):
        if arg_strings and arg_strings[0] == "--":
            arg_strings = arg_strings[1:]
        # noinspection PyProtectedMember
        return super()._get_values(action, arg_strings)


class Program(ArgumentParserShim):
    """
    Constructs an argument parser and command runner

    Args:
        prog: Name of the program, as referred to on the command line
        description: Short description of the program displayed at the top of help
        version: String representation without the leading "v" e.g. "1.0.0"
        author: String of program author
        bootstrap: function to be called after args are parsed
        bootstrap_resv: list of reserved arguments that will be in globals
    """

    def __init__(
        self,
        version: str,
        author: str,
        bootstrap: Callable = None,
        bootstrap_resv: List[str] = [],
        **kwargs,
    ):
        super().__init__(
            formatter_class=RawDescriptionHelpFormatter,
            epilog=f"Version {version}\nBuilt by {author}",
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
            {
                param.arg_name: param.description
                for param in parse(self.bootstrap.__doc__).params
            },
        )

    def add_commands(self, *commands: Callable) -> "Program":
        """
        Add a list of commands to program

        Args:
            commands: List of functions to add
        """
        for command in commands:
            self.add_command(command)
        return self

    def add_command(self, command: Callable) -> "Program":
        """
        Adds a command to the cli. Pass the uninitialised class

        Args:
            command: function to add
        """
        doc = parse(command.__doc__)
        help_dict = {param.arg_name: param.description for param in doc.params}
        cmd_parser = self.subparser.add_parser(
            command.__name__.replace("_", "-"),
            description=(doc.long_description or doc.short_description).strip(),
            help=doc.short_description.strip(),
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

        Args:
            args: arguments list. Defaults to sys.argv[1:]
            namespace: Namespace to use to store arguments
        """
        self.parsed_args = super().parse_args(args, namespace)
        self.globals = self.bootstrap(
            **self._get_func_args(self.bootstrap, self.parsed_args)
        )
        return self

    def run_command(self) -> int:
        """
        Initialise the command with the parsed args plus any extra kwargs

        Returns:
            Return code from the command's run method
        """

        kwargs = self._get_func_args(self.parsed_args.cmd, self.parsed_args)
        if iscoroutinefunction(self.parsed_args.cmd):
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
