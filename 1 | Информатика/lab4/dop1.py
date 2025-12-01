from json2xml import json2xml
from json2xml.utils import readfromjson

input_file = "input_schedule.json"
output_file = "output_dop1.xml"

data = readfromjson(input_file)

xml_data = json2xml.Json2xml(data).to_xml()

with open(output_file, "w", encoding="utf-8") as file:
    file.write(xml_data)

print(f"Конвертация завершена! Результат сохранён в {output_file}")