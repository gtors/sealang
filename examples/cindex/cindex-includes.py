#!/usr/bin/env python

"""
A simple command line tool for dumping a Graphviz description (dot) that
describes include dependencies.
"""


def main():
    import sys
    from clang.cindex import Index

    from optparse import OptionParser

    parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")
    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args()
    if len(args) == 0:
        parser.error('invalid number arguments')

    # FIXME: Add an output file option
    out = sys.stdout

    index = Index.create()
    tu = index.parse(None, args)
    if not tu:
        parser.error("unable to load input")

    # A helper function for generating the node name.
    def name(f):
        if f:
            return "\"" + f.name + "\""

    # Generate the include graph
    out.write("digraph G {\n")
    for i in tu.get_includes():
        line = "  "
        if i.is_input_file:
            # Always write the input file as a node just in case it doesn't
            # actually include anything. This would generate a 1 node graph.
            line += name(i.include)
        else:
            line += f'{name(i.source)}->{name(i.include)}'
        line += "\n"
        out.write(line)
    out.write("}\n")


if __name__ == '__main__':
    main()

