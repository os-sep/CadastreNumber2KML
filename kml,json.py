import json,os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def Placemark_etree(name_geozone, descript, coords, color_line="55307b19", width="50", poly_color="55307b19"):
    """Функция которая составляет тег Placemark формата  ElementTree.
    Берёт в себя: название геозоны, описание, координаты, *цвет линии, *ширину линии, *цвет полигона"""
    root = ET.Element("Placemark")

    name = ET.Element('name')
    name.text = name_geozone
    root.append(name)

    descr = ET.Element('description')
    descr.text = descript
    root.append(descr)

    style = ET.Element('Style')

    line_style = ET.Element('LineStyle')
    color = ET.SubElement(line_style,'color')
    color.text = color_line
    width_text = ET.SubElement(line_style,'width')
    width_text.text =  width
    style.append(line_style)

    poly_style = ET.Element('PolyStyle')
    poly_style_color = ET.SubElement(poly_style,'color')
    poly_style_color.text = poly_color
    style.append(poly_style)

    root.append(style)

    polygon = ET.Element('Polygon')
    outer=ET.SubElement(polygon,'outerBoundaryIs')
    line_ring = ET.SubElement(outer,'LinearRing')
    coordinates = ET.SubElement(line_ring,'coordinates')
    coordinates.text = coords
    root.append(polygon)

    Placemark = root
    return Placemark

#Найдём список файлов с расширением geo.json в папке ./input/output от текущей
os.chdir('./input/output')
files_dir=os.listdir()
list_jsons = []
for i in files_dir:
    if i[-8:] == "geo.json":
        list_jsons.append(i)

#Создаём словарь название = координаты
dict_name_coords=dict()
multipoly_names=[]
for name_file in list_jsons:
    file = open(name_file,'r')
    txt = file.read()
    string = ']]]]}, "crs": {"type": "name", "properties": {"use_local_coord": true}}}'
    count_of_poly=txt.count(string)
    if count_of_poly>1:
        k=0
        n=1
        for i in range(len(txt)):
            if string == txt[i:(i+len(string))] and n == 1:
                with open(name_file[:-9]+' '+str(n)+'.geo.json','w') as file:
                    if n == 1:
                        file.write(txt[0:(i+len(string))])
                    if n >1:
                        file.write(txt[k:(i+len(string))])
                k=i+len(string)
                n+=1


files_dir=os.listdir()
list_jsons = []
for i in files_dir:
    if i[-8:] == "geo.json":
        list_jsons.append(i)


for name_file in list_jsons:
    try:
        with open(name_file,'r') as file:
            json_data = json.load(file)
    except json.JSONDecodeError:
        pass
    s=json_data['geometry']['coordinates'][0][0]
    try:
        for i in s:
            i.append(0)
            for k in range(3):
                i[k] = str(i[k])
    except AttributeError:
        multipoly_names.append(name_file)
        continue
    for i in range(len(s)):
        s[i] = ','.join(s[i])
    dict_name_coords.update({name_file:' '.join(s)})

# Создаём KML

root = ET.Element('kml')
doc = ET.SubElement(root,'Document')
name = ET.SubElement(doc,'name')
name.text = "Geofences"
names_of_dicts = dict_name_coords.keys()
for name in names_of_dicts:
    descript = ':'.join(name[0:-9].split('_'))
    doc.append(Placemark_etree(descript, "Kad number of geozone: "+descript, dict_name_coords[name]))

#Записываем KML
os.chdir('../..')
def save_xml(filename, xml_code):
    xml_string = ET.tostring(xml_code).decode()

    xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
    with open(filename, 'w') as xml_file:
        xml_file.write(xml_prettyxml)
save_xml('result.kml',root)


with open('Multy_poly.txt','w') as file:
    for name in multipoly_names:
        file.writelines(name+'\n')









    #asd
