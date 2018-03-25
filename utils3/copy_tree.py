import os
import shutil
import sys

def main():
    try:
        src_path = sys.argv[1]
        dest_path = sys.argv[2]
    except BaseException as e:
        raise e

    could_not_copy_list = []

    for dir_path, dir_names, file_names in os.walk(src_path):
        rel_dir = os.path.relpath(dir_path, src_path)

        dest_dir_path = os.path.join(dest_path, rel_dir)

        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)

        for file_name in file_names:
            if '.DS_Store' != file_name:
                src_full_path = os.path.join(dir_path, file_name)
                dest_full_path = os.path.join(dest_dir_path, file_name)

                if os.path.exists(dest_full_path):
                    src_stat = os.stat(src_full_path)
                    dest_stat = os.stat(dest_full_path)

                    if src_stat.st_size > dest_stat.st_size:
                        # print({'name': src_full_path, 'size': src_stat.st_size})
                        could_not_copy_list.append(copy_carefully(src_full_path, dest_full_path))

                    if src_stat.st_size == dest_stat.st_size:
                        shutil.copystat(src_full_path, dest_full_path)

                        # copy_carefully(source, destination)
                else:
                    try:
                        shutil.copyfile(src_full_path, dest_full_path)
                    except IOError as e:
                        could_not_copy_list.append(copy_carefully(src_full_path, dest_full_path))
                    else:
                        shutil.copystat(src_full_path, dest_full_path)

    print(len(could_not_copy_list))
    f_log = open('log.txt', 'wt')
    for item in could_not_copy_list:
        f_log.write(str(item) + '\n')
    f_log.close()


def copy_carefully(source, destination):
    print('copy_carefully()')
    src_stat = os.stat(source)
    dest_stat = os.stat(destination)
    print('%s(%s)' % (source, src_stat.st_size))
    print('-> %s(%s)' % (destination, dest_stat.st_size))

    b_error = False

    f = open(source, 'rb')

    fo = open(destination, 'wb')
    while True:
        try:
            txt = f.read(1024)

            if not txt:
                break

            fo.write(txt)
        except IOError as e:
            b_error = True
            f.close()
            fo.close()
            src_stat = os.stat(source)
            dest_stat = os.stat(destination)
            print("%s(%s) -> %s(%s) partially" % (source, src_stat.st_size, destination, dest_stat.st_size))
            break
    f.close()
    fo.close()

    b_success = not b_error

    if b_success:
        shutil.copystat(source, destination)

    src_stat = os.stat(source)
    dest_stat = os.stat(destination)
    return {'source': {'name': source, 'size': src_stat.st_size},
            'destination': {'name': destination, 'size': dest_stat.st_size}}


if __name__ == '__main__':
    main()
