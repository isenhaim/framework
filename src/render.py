from jinja2 import Environment, FileSystemLoader


def render(template, folder='templates', **kwargs):

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template)

    return template.render(**kwargs)
