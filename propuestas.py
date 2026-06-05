import os
import base64
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from playwright.sync_api import sync_playwright


def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"


def images_dict(base_dir: Path):

    return {
        "historigrama_sti": get_image_as_base64(base_dir / "sti" / "histograma_sti.png"),
        "spl1": get_image_as_base64(base_dir / "spl" / "spl1.png"),
        "npx": get_image_as_base64(base_dir / "products" / "npx.jpg"),
        "alc_1604d": get_image_as_base64(base_dir / "products" / "alc-1604d.png"),
        "ease0003": get_image_as_base64(base_dir / "sti" / "Ease0003.png"),
        "spl2": get_image_as_base64(base_dir / "spl" / "spl2.png"),
        "spl3": get_image_as_base64(base_dir / "spl" / "spl3.png"),
        "cca_80d": get_image_as_base64(base_dir / "products" / "CCA-80D.png"),
        "r15_3696": get_image_as_base64(base_dir / "products" / "R15-3696.png")
    }


def render_html():
    base_dir = Path(__file__).parent.absolute()
    env = Environment(loader=FileSystemLoader(base_dir / "templates"))
    template = env.get_template("proposal.html")
    
    base_dir = Path(__file__).parent.absolute()
    assets_dir = base_dir / "assets"

    return template.render(
            images=images_dict(base_dir / "assets")
        )


def main():
    base_dir = Path(__file__).parent.absolute()
    html_content = render_html()
    
        
    print("Generating PDF via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use A4 screen resolution ratio for rendering
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        
        page.set_content(html_content, wait_until="networkidle")

        css_path = base_dir / "static" / "styles.css"
        page.add_style_tag(path=str(css_path))

        pdf_path = base_dir / "output" / "proposal.pdf"
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "0mm",
                "bottom": "0mm",
                "left": "0mm",
                "right": "0mm"
            }
        )
        browser.close()
        
    print(f"PDF successfully generated: {pdf_path}")

if __name__ == "__main__":
    main()
