from funcs import generate_pages_recursive, remove_dir, copy_static_files_to_static
import time
import sys


def main():
    base_path = sys.argv[0]
    if base_path == None:
        base_path = "/"
    remove_dir()
    time.sleep(1)
    copy_static_files_to_static()
    generate_pages_recursive(base_path)


main()
