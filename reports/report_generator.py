import json
import os
from jinja2 import Environment, FileSystemLoader

def generate_json_report(data):
    with open("report.json", "w") as f:
        json.dump(data, f, indent=4)


def generate_html_report(data, template_dir="./", output="report.html"):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html.jinja")

    html = template.render(data=data)

    with open(output, "w") as f:
        f.write(html)
