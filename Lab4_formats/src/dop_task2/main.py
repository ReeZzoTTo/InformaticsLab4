from configparser import ConfigParser
import json


def main():
    config = ConfigParser()
    config.read("objects/schedule.ini", encoding="utf-8")
    
    ini_dict: dict = {}
    
    for section in config.sections():
        ini_dict[section] = dict(config[section].items())

    for section in config.sections():
        for key, value in config[section].items():
            ini_dict[section][key] = value.strip('"').strip("'")

            if "," in value and '", "' not in value:
                continue
            elif "," in value:
                list_items = [val.strip().strip('"') for val in value.split(",")]
                for x in range(len(list_items)):
                    try:
                        list_items[x] = int(list_items[x])
                    except ValueError: pass

                ini_dict[section][key] = list_items
    
    with open("./schedule.json", "w", encoding="utf-8") as file:
        json.dump(ini_dict, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()