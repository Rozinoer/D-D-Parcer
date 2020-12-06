import requests
from bs4 import BeautifulSoup
import csv
from itertools import groupby

url = "https://dungeon.su/spells/"
basic_url = "https://dungeon.su"

resp = requests.get(url)
html = resp.text
parser = BeautifulSoup(html, "html.parser")
print("Done")
for elements in parser.find_all("li", {'class': 'first-letter'}):
    elements.decompose()
print("Done")
elements = parser.select_one("ul.list-of-items.col4.double")

spells = elements.find_all("li")

urls = []
for spell in spells:
    url = spell.select_one("a")["href"]
    urls.append(basic_url + url)
print("Done")


def check(mas):
    new_mas = []
    for element in mas:
        if element not in new_mas:
            new_mas.append(element)
    return new_mas


def fill_csv():
    names = ["Id", "info"]
    spell_names = ["ID_spell", "ID_lvl", "ID_component", "ID_source", "Name", "Description", "ID_school"]
    fd_lvl = open("lvl.csv", mode="w", encoding='utf-8')
    fd_class = open("class.csv", mode="w", encoding='utf-8')
    fd_school = open("school.csv", mode="w", encoding='utf-8')
    fd_components = open("components.csv", mode="w", encoding='utf-8')
    fd_distance = open("distance.csv", mode="w", encoding='utf-8')
    fd_duration = open("duration.csv", mode="w", encoding='utf-8')
    fd_source = open("source.csv", mode="w", encoding='utf-8')
    fd_spell = open("spell.csv", mode="w", encoding='utf-8')

    file_writer1 = csv.DictWriter(fd_lvl, delimiter=",", fieldnames=names)
    file_writer2 = csv.DictWriter(fd_class, delimiter=",", fieldnames=names)
    file_writer3 = csv.DictWriter(fd_school, delimiter=",", fieldnames=names)
    file_writer4 = csv.DictWriter(fd_components, delimiter=",", fieldnames=names)
    file_writer5 = csv.DictWriter(fd_distance, delimiter=",", fieldnames=names)
    file_writer6 = csv.DictWriter(fd_duration, delimiter=",", fieldnames=names)
    file_writer7 = csv.DictWriter(fd_source, delimiter=",", fieldnames=names)
    file_writer8 = csv.DictWriter(fd_spell, delimiter=",", fieldnames=spell_names)

    file_writer1.writeheader()
    file_writer2.writeheader()
    file_writer3.writeheader()
    file_writer4.writeheader()
    file_writer5.writeheader()
    file_writer6.writeheader()
    file_writer7.writeheader()
    file_writer8.writeheader()

    num = 1
    classes = []
    level = []
    school = []
    components = []
    distance = []
    duration = []
    source = []

    for url in urls:
        resp = requests.get(url)
        html = resp.text
        parser = BeautifulSoup(html, "html.parser")

        for elements in parser.find_all("li", {'class': 'translate-by'}):
            elements.decompose()

        for elements in parser.find_all("strong"):
            elements.decompose()

        for elements in parser.find_all("h3"):
            elements.decompose()

        elements = parser.select("ul.params li")

        all_param = [element.text for element in elements]
        level.append(all_param[0])
        school.append(all_param[1])
        distance.append(all_param[3])
        components.append(all_param[4])
        duration.append(all_param[5])
        classes.append(all_param[6])
        source.append(all_param[7])
    new_classes = check(classes)
    new_level = check(level)
    new_school = check(school)
    new_components = check(components)
    new_distance = check(distance)
    new_duration = check(duration)
    new_source = check(source)
    for item in new_classes:
        file_writer2.writerow({"Id": num, "info": item})
        num = num + 1
    num = 1
    for item in new_level:
        file_writer1.writerow({"Id": num, "info": item})
        num = num + 1
    num = 1
    for item in new_school:
        file_writer3.writerow({"Id": num, "info": item})
        num = num + 1
    num = 1
    for item in new_components:
        file_writer4.writerow({"Id": num, "info": item})
        num = num + 1
    num = 1
    for item in new_distance:
        file_writer5.writerow({"Id": num, "info": item})
        num = num + 1
    num = 1
    for item in new_duration:
        file_writer6.writerow({"Id": num, "info": item})
        num = num + 1
    num = 1
    for item in new_source:
        file_writer7.writerow({"Id": num, "info": item})
        num = num + 1

    key = 1
    for url in urls:
        resp = requests.get(url)
        html = resp.text
        parser = BeautifulSoup(html, "html.parser")

        for elements in parser.find_all("li", {'class': 'translate-by'}):
            elements.decompose()

        for elements in parser.find_all("strong"):
            elements.decompose()

        for elements in parser.find_all("h3"):
            elements.decompose()

        named = parser.select_one("h2 a.item-link").get_text()

        elements = parser.select("ul.params li")

        all_param = [element.text for element in elements]
        level = new_level.index(all_param[0]) + 1
        components = new_components.index(all_param[4]) + 1
        source = new_source.index(all_param[7]) + 1
        description = all_param[8]
        school = new_school.index(all_param[1]) + 1
        file_writer8.writerow({"ID_spell": key, "ID_lvl": level, "ID_component": components, "ID_source": source,
                               "Name": named, "Description": description, "ID_school": school})
        key = key + 1
    # file_writer.writerow({"Name": named, "Level": level, "School": school, "Application time": app_time,
    #                       "Distance": distance, "Components": components, "Duration": duration,
    #                       "Classes": classes, "Description": description})


fill_csv()
print("Done")
