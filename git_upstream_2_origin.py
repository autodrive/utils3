import git_util


def main():
    remotes_list = git_util.git('remote')
    print(remotes_list)


if __name__ == '__main__':
    main()
