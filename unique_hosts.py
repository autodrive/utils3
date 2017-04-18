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
        # remove '\n' at the end
        host_line_strip = host_line.strip()
        # if anything remaining
        if host_line_strip:
            if host_line_strip.startswith('#'):
                # if comment
                key = host_line_strip
                # append line number
                value = i
            else:
                # if not comment
                host_line_strip_split = host_line_strip.split()
                # probably [address, domain name]
                key = host_line_strip_split[-1]
                # append line number and address
                value = (i, host_line_strip_split[:-1])
            # end if comment block
            # find entry in d
            d[key] = d.get(key, [])
            # append to the entry
            d[key].append(value)
    # end text line loop
    print(len(d.keys()))


if __name__ == '__main__':
    main(sys.argv)
