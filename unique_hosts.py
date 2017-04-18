import sys


def main(argv):
    filename = argv[1]

    # read file
    with open(filename, 'rt') as hosts_file:
        hosts_txt_lines = hosts_file.readlines()

    print(len(hosts_txt_lines))

    # init dict
    d = {}

    # text line loop
    for i, host_line in enumerate(hosts_txt_lines):
        host_line_strip = host_line.strip()
        if host_line_strip:
            if host_line_strip.startswith('#'):
                key = host_line_strip
                value = i
            else:
                host_line_strip_split = host_line_strip.split()
                key = host_line_strip_split[-1]
                value = (i, host_line_strip_split[:-1])
            d[key] = d.get(key, [])
            d[key].append(value)
    print(len(d.keys()))


if __name__ == '__main__':
    main(sys.argv)
