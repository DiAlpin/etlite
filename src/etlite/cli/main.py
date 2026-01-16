
import sys
import argparse

from etlite.cli.create_project import Project


__version__ = "0.1.0"

def display_version():
    """Display the version information."""
    print(f"etl version {__version__}")



def create_project(name: str, path: str = "."):
    try:
        proj = Project(name, path)
        proj.init()
        
    except Exception as e:
        print(f"Error creating project: {e}", file=sys.stderr)
        sys.exit(1)



def main():
    parser = argparse.ArgumentParser(
        prog='etl',
        description='ETLite - A lightweight ETL framework',
        epilog='For more information, visit the documentation at https://github.com/DiAlpin/etlite',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(
        dest='command', 
        help='Available commands',
        required=False
    )
    
    init_parser = subparsers.add_parser(
        'init', 
        help='Initialize a new ETL project'
    )
    init_parser.add_argument(
        '-n', '--name',
        type=str,
        help='Name of the project to create'
    )
    init_parser.add_argument(
        '-p', '--path',
        type=str,
        default='.',
        help='Base path where project will be created (default: current directory)'
    )
    args = parser.parse_args()
    
    if args.command == 'init':
        create_project(args.name, args.path)
    elif args.command is None:
        parser.print_help()
        sys.exit(0)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
