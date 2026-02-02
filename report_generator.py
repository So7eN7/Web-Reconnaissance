import json
import os
from jinja2 import Environment, FileSystemLoader

FILE_DIR="reports/"
FILE_NAME="report.json"

file_path = os.path.join(FILE_DIR, FILE_NAME)

def generate_json_report(data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def generate_html_report(data, template_dir="reports", output="reports/report.html"):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html.jinja")

    html = template.render(data=data)

    with open(output, "w") as f:
        f.write(html)
