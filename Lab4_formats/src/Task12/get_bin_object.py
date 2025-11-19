# print(501178 % 132) = 106
# 106: INI -> JSON


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
