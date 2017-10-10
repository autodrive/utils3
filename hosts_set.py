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
        for host_info_key, address in host_info_dict['host_info'].items():
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

    print('# lines = %d' % len(txt_lines))

    result = {'host_info': {}, 'comment': set()}
    for k, txt in enumerate(txt_lines):

        serial_number_str = '%04d/%04d' % (k, len(txt_lines))

        if '#' == txt[0]:
            result['comment'].add(txt.strip())
        # if not comment
        else:
            address, hostname = txt.split()
            hostname_strip = hostname.strip()
            b_already = hostname_strip in result['host_info']
            if b_already:
                print("%s %s already known" % (serial_number_str, hostname_strip))
            else:
                result['host_info'][hostname_strip] = address.strip()
                b_success = hostname_strip in result['host_info']
                if b_success:
                    print(
                    "%s %s read successfully (%d)" % (serial_number_str, hostname_strip, len(result['host_info'])))
                else:
                    print("%s %s not read (%d)" % (serial_number_str, hostname_strip, len(result['host_info'])))

    return result


if __name__ == '__main__':
    if 3 <= len(sys.argv):
        # if arg given
        main(sys.argv[1], sys.argv[2])
