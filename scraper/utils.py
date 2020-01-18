from rest_framework_xml.parsers import XMLParser


class CustomXMLParser(XMLParser):
    list_tags = [
        'item'
    ]

    def _xml_convert(self, element):
        children = list(element)

        if len(children) == 0:
            return self._type_convert(element.text)
        else:
            if children[0].tag.split('}')[1] in self.list_tags:
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag] = self._xml_convert(child)

            return data


def remove_rdf_from_parsed_rss(parsed_rss):
    keys_to_remove = []
    new_parsed_rss = {}
    for key, value in parsed_rss.items():
        if '{' in key or '}' in key:
            new_key = key.split('}')[1]
            if type(value) == dict:
                new_parsed_rss[new_key] = remove_rdf_from_parsed_rss(value)
            elif type(value) == list:
                new_parsed_rss[new_key] = [remove_rdf_from_parsed_rss(v) for v in value]
            else:
                new_parsed_rss[new_key] = value
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del parsed_rss[key]
    return new_parsed_rss
