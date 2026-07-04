import os
import base64
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    if image_path.endswith(".svg"):
        return f"data:image/svg+xml;base64,{encoded_string}"
    elif image_path.endswith(".png"):
        return f"data:image/png;base64,{encoded_string}"
    else:
        return f"data:image/jpeg;base64,{encoded_string}"

def generate_filiere_pdfs(template_name, static_data, students_data, logo_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(current_dir)
    backend_dir = os.path.dirname(app_dir)
    
    template_dir = os.path.join(app_dir, "templates", "html")
    css_file_path = os.path.join(app_dir, "templates", "css", f"{template_name}.css")
    output_base_dir = os.path.join(backend_dir, "output_diplomas")

    os.makedirs(output_base_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(f"{template_name}.html")
    logo_base64 = get_image_base64(logo_path)

    grouped_students = {}
    for student in students_data:
        filiere = student["filiere"]
        if filiere not in grouped_students:
            grouped_students[filiere] = []
        grouped_students[filiere].append(student)

    # Using the standard Sync API
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for filiere, students_list in grouped_students.items():
            context_data = static_data.copy()
            context_data["logo_url"] = logo_base64
            context_data["students"] = students_list

            output_filename = os.path.join(output_base_dir, f"Diplomas_{filiere}.pdf")
            rendered_html = template.render(context_data)
            
            page.set_content(rendered_html)
            page.add_style_tag(path=css_file_path)
            page.wait_for_load_state("networkidle")

            page.pdf(
                path=output_filename,
                format="A4",
                landscape=True,
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            print(f"Generated: {output_filename} ({len(students_list)} diplomas)")

        browser.close()
        print("\nAll batch files generated successfully!")