try:
    from lxml import etree
except ImportError:
    raise
# from pathlib import Path


class XMLTree:
    def __init__(self, filepath):
        self.filepath = filepath
        
        self.tree = self.read()
        self.configstore = self.tree.find(".//configstore")        

    def list_checkitems(self):
        return self.tree.findall(".//checkitem")
    
    
    def read(self):
        try:
            tree = etree.ElementTree(file=self.filepath)
        except etree.XMLSyntaxError:
            with open(self.filepath, 'rb') as in_file:
                file_content = in_file.read()
            tree = self.recursive_parser(file_content)
        return tree
    
    def recursive_parser(self, file_content):
        try:
            return etree.fromstring(file_content)
        except etree.XMLSyntaxError:
            return self.recursive_parser(file_content[1:])

    def del_checkitem(self, index):
        item = self.list_checkitems()[index]
        item.getparent().remove(item)

    def add_checkitem(self, desc, item_id, compliant_txt='...', noncompliant_txt='...'):
        new_checkitem = etree.Element("checkitem", desc=desc, id=item_id)
        
        compliant = etree.Element("compliant")
        compliant.text = compliant_txt
        
        noncompliant = etree.Element("noncompliant")
        noncompliant.text = noncompliant_txt

        new_checkitem.append(compliant)
        new_checkitem.append(noncompliant)
        
        self.configstore.append(new_checkitem)
        
    def edit_checkitem(self, index, text):
        item = self.list_checkitems()[index]
        newelement = etree.fromstring('<checkitem>' + '\n' + text + '\n' '</checkitem>')

        compliant_text = newelement.find(".//compliant").text
        noncompliant_text = newelement.find(".//noncompliant").text
        
        item.find(".//compliant").text = compliant_text
        item.find(".//noncompliant").text = noncompliant_text

        del newelement
    
    def write(self, filepath, encoding='UTF-8', pretty_print=True):
        #if encoding is None:
            #encoding = self.tree.docinfo.encoding
        with open(filepath, 'wb') as out_file:
            out_file.write(
                        etree.tostring(self.tree, xml_declaration=True, pretty_print=pretty_print, encoding=encoding)
                        )
    def to_string(self, element):
        strings = []
        for sub in element:
            strings.append(etree.tostring(sub, pretty_print=True).decode('UTF-8'))
        string = ''.join(strings)
        return string
        

if __name__ == '__main__':
    filename = r'..\..\..\test.xml'
    xtree = XMLTree(filename)
    xtree.add_checkitem('nue', 'tue')
    print(xtree.list_checkitems()[-1].get('desc'))
    item = xtree.list_checkitems()[-1]
    item.find(".//compliant").text = 'Blablalba'
    print(item.find(".//compliant").text)
    xtree.edit_checkitem(-1, #"<compliant>Testtext</compliant>\n<noncompliant>NotTestText</noncompliant>")
    "<compliant>1FILE_NAME = 'global.ini' and \
                 SECT = 'persistence' and \
                 NAME = 'basepath_databackup' and \
                 ( VALUE like '/hana/backup/%/data' OR VALUE like '/hana_backup/%/data' )\
      </compliant>\
      \
<noncompliant>FILE_NAME = 'global.ini' and \
                 SECT = 'persistence' and \
                 NAME = 'basepath_databackup' and \
                 NOT ( VALUE like '/hana/backup/%/data' OR VALUE like '/hana_backup/%/data'  )\
      </noncompliant>" )
   
    print(item.find(".//compliant").text)
    print(item.find(".//noncompliant").text)
    
    #print(xtree.show())
    #xtree.write('xml_edit_test.xml')
