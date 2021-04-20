import xml.etree.ElementTree as ET
import lxml

myTree = ET.parse("XMLtest1.xml")
myRoot = myTree.getroot()
print(myRoot[0].attrib)
for x in myRoot[0]:
    print(x.tag,x.attrib)
for x in myRoot[0]:
    c1 = (x.text)

root = XMLtest1.etree.fromstring(xml)
c1 = root.xpath('//c1/cardList/text()')        
print(c1)



