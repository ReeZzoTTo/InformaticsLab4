def get_bin_file_object(filename: str) -> dict:
    with open(filename, encoding="utf-8") as file:
        result_json_file_text: dict = {}
        ini_block: dict = {}

        for line in file:
            if line[0] == "[":
                if ini_block:
                    result_json_file_text[ini_block_name] = ini_block
                ini_block_name: str = line[1:-2]
                ini_block = {}
            
            line_value = line[0:-1].split(" = ")
            if len(line_value) == 2:
                if line_value and "," in line_value[1] and line_value[1].count('"') != 2:
                    list_values: list[str] | list[int] = line_value[1].split(", ")

                    for val_ind in range(len(list_values)):
                        try: list_values[val_ind] = int(list_values[val_ind])
                        except ValueError: 
                            list_values[val_ind] = list_values[val_ind][1:-1]
                    
                    ini_block[line_value[0]] = list_values

                elif line_value and '"' in line_value[1]:
                    ini_block[line_value[0]] = line_value[1][1:-1]
                elif line_value:
                    ini_block[line_value[0]] = line_value[1]
        
        result_json_file_text[ini_block_name] = ini_block

        return result_json_file_text

def parse_xml_list(lst: list, key: str, inner_lvl: int) -> list[str]:
    xml_line_list: list[str] = []
    
    for element in lst:
        element_type: str = str(type(element))[8:-2]

        if element_type == "dict":
            xml_line_list.append("\t" * inner_lvl + f"<{key}>")
            xml_line_list += parse_xml_element(obj=element, inner_lvl=inner_lvl + 1)
            xml_line_list.append("\t" * inner_lvl + f"</{key}>")
        elif element_type == "list":
            xml_line_list.append("\t" * inner_lvl + f"<{key}>")
            xml_line_list += parse_xml_list(obj=element, key=key+"_element", inner_lvl=inner_lvl + 1)
            xml_line_list.append("\t" * inner_lvl + f"</{key}>")
        else:
            xml_line_list.append("\t" * inner_lvl + f"<{key}>{element}</{key}>")
    
    return xml_line_list


def parse_xml_element(obj: dict | list, inner_lvl: int) -> list[str]:
    xml_line_list: list[str] = []
    
    for key in obj:
        element: any = obj[key]
        element_type: str = str(type(element))[8:-2]

        if element_type == "dict":
            xml_line_list.append("\t" * inner_lvl + f"<{key}>")
            xml_line_list += parse_xml_element(obj=element, inner_lvl=inner_lvl + 1)
            xml_line_list.append("\t" * inner_lvl + f"</{key}>")
        elif element_type == "list":
            xml_line_list.append("\t" * inner_lvl + f"<{key}>")
            xml_line_list += parse_xml_list(lst=element, key=key+"_element", inner_lvl=inner_lvl + 1)
            xml_line_list.append("\t" * inner_lvl + f"</{key}>")
        else:
            xml_line_list.append("\t" * inner_lvl + f"<{key}>{element}</{key}>")
    
    return xml_line_list



def parse_main_xml(obj: dict, main_argument: str = "schedule") -> None:
    xml_line_list: list[str] = ['<?xml version=1.0 encoding="UTF-8">']
    inner_lvl: int = 0
    xml_line_list.append(f"<{main_argument}>")

    xml_line_list += parse_xml_element(obj=obj, inner_lvl=inner_lvl + 1)

    xml_line_list.append(f"</{main_argument}>")

    xml_file = open(f"./{main_argument}.xml", "w", encoding="utf-8")

    for el in xml_line_list: xml_file.write(el + "\n")

    xml_file.close()

    

def main():
    obj: dict = get_bin_file_object("objects/schedule.ini")
    parse_main_xml(obj=obj, main_argument="schedule")

if __name__ == "__main__":
    main()
