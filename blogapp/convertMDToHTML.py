#!/usr/bin/python
# Python transform MD file to html
import sys
import re  # for regexp search


class MDToHTMLParser:
    config = {
        'paragraph': {
            'type': 'line_default',
            'marker': '',
            'tag': 'p'
        },
        'title': {
            'type': 'line',
            'marker': '#',
            'tag': ['h2', 'h3', 'h4', 'h5']
        },
        'list_unordered': {
            'type': 'line',
            'marker': "(\*|\-|\+)",
            'tag': 'li',
            'main_tag': 'ul'
        },
        'list_ordered': {
            'type': 'line',
            'marker': "(\d+)\.",
            'tag': 'li',
            'main_tag': 'ol'
        },
        'bold': {
            'type': 'style',
            'marker': '((_(.+?)_)|(\*(.+?)\*))',
            'tag': 'b'
        },
        'italic': {
            'type': 'style',
            'marker': '((__(.+?)__)|(\*\*(.+?)\*\*))',
            'tag': 'i'
        }
    }

    def replace_to_tag(self, line, tag=config['paragraph']['tag']):
        line_html = "<%s>%s</%s>" % (tag, line, tag)
        if line_html.find("\n"):
            line_html = "%s\n" % line_html.replace("\n", "")
        return line_html

    def replace_title(self, line_md):
        line = line_md[1:]

        for i in range(len(self.config['title']['tag'])):
            if re.match(self.config['title']['marker'], line) is not None:
                line = line[1:]
            else:
                return self.replace_to_tag(line, self.config['title']['tag'][i])

        return self.replace_to_tag(line_md)

    def replace_list(self, previous_line_md, line_md, next_line_md, t_list):
        line_html = []

        if self.find_type_line(previous_line_md) == t_list:
            line_html.append("<%s>\n" % self.config[t_list]['main_tag'])

        line_tmp = re.sub(self.config[t_list]['marker'], "", line_md)
        line_html.append(self.replace_to_tag(line_tmp, self.config[t_list]['tag']))

        if self.find_type_line(next_line_md) == t_list:
            line_html.append("</%s>\n" % self.config[t_list]['main_tag'])

        return "".join(line_html)

    def find_type_line(self, l_md):
        for key, value in self.config.items():
            if value['type'] == 'line':
                if re.match(value['marker'], l_md) is not None:
                    return key

        return "paragraph"

    def parse_style(self, l_md):
        l_html = l_md
        types_elements = [key for key, value in self.config.items() if value['type'] == 'style']
        types_elements.sort(reverse=True)

        for t_el in types_elements:
            list_regexp = re.split(self.config[t_el]['marker'], l_html)
            list_simple = [el for el in list_regexp
                               if el is not None and
                               re.match(self.config[t_el]['marker'], el) is None]

            for i in range(len(list_simple)):
                if i % 2 == 1:
                    list_simple[i] = self.replace_to_tag(list_simple[i], self.config[t_el]['tag'])

            l_html = "".join(list_simple)

        return l_html

    def parse_link(self, l_md):
        pass

    def parse(self, txt_md):
        txt_html = []

        for idx, l_md in enumerate(txt_md):
            if l_md == '\n':  # empty line
                pass
            else:
                l_html = self.parse_style(l_md)
                l_html = self.parse_link(l_html)

                line_type = self.find_type_line(l_html)
                if line_type == "title":
                    txt_html.append(self.replace_title(l_html))
                elif line_type == "list_unordered" or line_type == "list_ordered":
                    txt_html.append(self.replace_list(
                                    txt_md[idx-1], l_html, txt_md[idx+1], line_type))
                else:
                    txt_html.append(self.replace_to_tag(l_html))

        return "".join(txt_html)


if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename, 'r') as fd_r:
        article_md = fd_r.readlines()

    parser = MDToHTMLParser()
    article_html = parser.parse(article_md)

    with open(filename[:filename.rfind('.')]+".html", 'w') as fd_w:
        fd_w.write(article_html)
