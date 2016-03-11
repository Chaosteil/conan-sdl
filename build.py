import os
import platform
import sys

if __name__ == "__main__":
    os.system('conan export chaosteil/develop')

    def test(settings):
        argv = " ".join(sys.argv[1:])
        command = "conan test %s %s" % (settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t %s" % command)

    test('-s arch=x86_64 -s build_type=Debug')
    test('-s arch=x86_64')
