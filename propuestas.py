import os
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from playwright.sync_api import sync_playwright

def render_html():
    base_dir = Path(__file__).parent.absolute()
    env = Environment(loader=FileSystemLoader(base_dir / "templates"))
    template = env.get_template("proposal.html")
    
    base_dir = Path(__file__).parent.absolute()
    assets_dir = base_dir / "assets"

    return template.render(
        title="Proposal", 
        content="AV proposal",
        assets_path=assets_dir.as_uri()
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
