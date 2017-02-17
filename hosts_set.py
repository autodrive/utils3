import sys

import file_util


def main(filename, output_filename):
    host_info_dict = read_host_info(filename)

    write_host_info(host_info_dict, output_filename)


def write_host_info(host_info_dict, output_filename):
    """
    dictonary -> host info
    :param host_info_dict: dict
    :param output_filename: str
    :return: None
    """
    with open(output_filename, 'wt') as f:
        # write result
        for host_info_key, address in host_info_dict['host_info'].iteritems():
            write_this = '%s\t%s' % (address, host_info_key)
            print(write_this)
            f.write('%s\n' % write_this)

        for comment_line in host_info_dict['comment']:
            write_this = comment_line.strip()
            print(write_this)
            f.write('%s\n' % write_this)


def read_host_info(filename):
    """
    host info -> dictionary
    :param filename: str
    :return: dict
    """
    txt_lines = file_util.read_txt_lines(filename)
    result = {'host_info': {}, 'comment': set()}
    for txt in txt_lines:
        if '#' == txt[0]:
            result['comment'].add(txt.strip())
        # if not comment
        else:
            address, hostname = txt.split()
            result['host_info'][hostname.strip()] = address.strip()
    return result


if __name__ == '__main__':
    if 3 <= len(sys.argv):
        # if arg given
        main(sys.argv[1], sys.argv[2])
