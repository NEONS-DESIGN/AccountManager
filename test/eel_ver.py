import eel
from jinja2 import Environment, FileSystemLoader


eel.init('web', allowed_extensions=['.js', '.html'])

env = Environment(loader=FileSystemLoader('web'))

@eel.expose
def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(context)

eel.start('templates/index.j2', jinja_templates='templates', mode='chrome', size=(640, 480))