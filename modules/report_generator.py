from jinja2 import Environment, FileSystemLoader
import os, datetime

class ReportGenerator:
    def generate(self, data):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("report.html")

        html = template.render(data=data)

        os.makedirs("reports", exist_ok=True)
        filename = f"reports/report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        return filename  # <-- return the file path
