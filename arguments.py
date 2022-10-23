import os


def parse_file_io(parser, output_ext):
    parser.add_argument(
        "file", help='The file to operate on')
    parser.add_argument(
        "-o", "--output", help="Directs the output to a name of your choice")
    args = parser.parse_args()
    if not args.output:
        args.output = "out."+output_ext
    
    return args
