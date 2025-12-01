def json_to_xml(json_obj, indent=0):

    xml_str = ""
    spacing = "  " * indent

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            xml_str += f"{spacing}<{key}>\n"
            xml_str += json_to_xml(value, indent + 1)
            xml_str += f"{spacing}</{key}>\n"
    elif isinstance(json_obj, list):
        for item in json_obj:
            xml_str += f"{spacing}<item>\n"
            xml_str += json_to_xml(item, indent + 1)
            xml_str += f"{spacing}</item>\n"
    else:
        xml_str += f"{spacing}{json_obj}\n"

    return xml_str


def convert_json_to_xml(input_file, output_file):

    try:
        with open("/Users/kirol.nadol/Desktop/input_schedule.json") as json_file:
            content = json_file.read()
            data = eval(content)

        xml_data = f"<root>\n{json_to_xml(data, 1)}</root>"

        with open(output_file, "w", encoding="utf-8") as xml_file:
            xml_file.write(xml_data)

        print(f"Конвертация завершена. XML сохранён в {output_file}")
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")


input_json_file = "input.json"
output_xml_file = "output.xml"

convert_json_to_xml(input_json_file, output_xml_file)