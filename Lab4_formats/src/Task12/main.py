from get_bin_object import get_bin_file_object
from parse_to_file import parse_to_file


def main():
    filename: str = "objects/schedule.ini"
    bin_object: dict = get_bin_file_object(filename) 
    parse_to_file(bin_object, filename)
    

if __name__ == "__main__":
    main()