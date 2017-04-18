import sys


def main(argv):
    input_file_name = argv[1]

    # read file
    with open(input_file_name, 'rt') as input_file:
        hosts_txt_lines = input_file.readlines()

    n_lines = len(hosts_txt_lines)
    print(n_lines)

    # init dict
    d = {}

    # text line loop
    for i, host_line in enumerate(hosts_txt_lines):
        # remove '\n' at the end
        host_line_strip = host_line.strip()
        # if anything remaining
        if host_line_strip:
            if not host_line_strip.startswith('#'):
                # if not comment
                host_line_strip_split = host_line_strip.split()
                # probably [address, domain name]
                key = host_line_strip_split[-1]
                # append line number, address, and a tab character
                value = (i, host_line)
                # find entry in d
                d[key] = d.get(key, value)
            # end if comment block

    # end text line loop

    values_list = list(d.values())
    values_list.sort()

    print(len(values_list))


if __name__ == '__main__':
    main(sys.argv)
