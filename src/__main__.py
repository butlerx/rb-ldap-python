"""rbldap entrypoint"""
from .cli import parse_args

if __name__ == "__main__":
    ARGS = parse_args()
    ARGS.func(ARGS)
