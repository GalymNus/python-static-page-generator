from funcs import generate_pages_recursive, remove_dir, copy_static_files_to_static
import time
import sys


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    remove_dir()
    time.sleep(1)
    copy_static_files_to_static()
    generate_pages_recursive(base_path)


main()
