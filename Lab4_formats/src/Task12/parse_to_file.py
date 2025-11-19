def get_file_name(filename: str) -> str:
    package_way: str = filename.split("/")
    json_file_name = package_way[-1].split(".")
    json_file_name = "".join([pack + "/" for pack in package_way[:-1]]) + json_file_name[0] + ".json"

    return json_file_name

def list_parser(array: list, inner_lvl: int) -> list[str]:
    inner_lvl += 1
    result_list: list[str] = []
    
    for array_element_ind in range(len(array)):
        cur_el = array[array_element_ind]

        if str(type(cur_el))[8:-2] == "str":
            cur_el = f'"{cur_el}"'

        if array_element_ind == len(array) - 1:
            result_list.append("\t" * inner_lvl + f'{cur_el}')
        else:
            result_list.append("\t" * inner_lvl + f"{cur_el},")

    return result_list
    

def object_parser(obj: dict, inner_lvl: int) -> list[str]:
    inner_lvl += 1
    result_list: list[str] = []

    iterations_count: int = len(obj.keys())
    current_iteration: int = 0

    for element in obj:
        current_iteration += 1
        
        
        element_type: str = str(type(obj[element]))   

        if element_type == "<class 'dict'>":
            current_dict_list: list[str] = ["\t" * inner_lvl + f'"{element}": ' + "{"]
            current_dict_list += object_parser(obj[element], inner_lvl)

            for i in current_dict_list:
                result_list.append(i)

            if current_iteration == iterations_count:
                result_list.append("\t" * inner_lvl + "}")
            else:
                result_list.append("\t" * inner_lvl + "},")

        elif element_type == "<class 'list'>":
            current_dict_list: list[str] = ["\t" * inner_lvl + f'"{element}": [']
            current_dict_list += list_parser(obj[element], inner_lvl)

            for i in current_dict_list:
                result_list.append(i)

            if current_iteration == iterations_count:
                result_list.append("\t" * inner_lvl + "]")
            else:
                result_list.append("\t" * inner_lvl + "],")


        elif element_type == "<class 'int'>" or element_type == "<class 'float'>":
            if current_iteration == iterations_count:
                result_list.append("\t" * inner_lvl + f'"{element}": {obj[element]}')
            else:
                result_list.append("\t" * inner_lvl + f'"{element}": {obj[element]},')

        else:
            if current_iteration == iterations_count:
                result_list.append("\t" * inner_lvl + f'"{element}": "{obj[element]}"')
            else:
                result_list.append("\t" * inner_lvl + f'"{element}": "{obj[element]}",')

    return result_list

def parse_to_file(obj: dict, filename: str) -> None:
    json_file = open(get_file_name(filename), "w", encoding="utf-8")
    json_file.write("{\n")

    inner_lvl = 0

    for element in object_parser(obj, inner_lvl):
        json_file.write(element + "\n")


    json_file.write("}")
    json_file.close()
