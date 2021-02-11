from jinja2 import Template
import os


def render(template, folder='templates', **kwargs):
    file = os.path.join(folder, template)
    with open(file, encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs)
