import os
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    base_dir = Path(__file__).parent.absolute()
    template_file = base_dir / "template.html"
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    
    if not template_file.exists():
        print(f"Error: {template_file} not found.")
        return
        
    print("Generating PDF via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use A4 screen resolution ratio for rendering
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(f"file://{template_file}", wait_until="networkidle")
        
        pdf_path = output_dir / "proposal.pdf"
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
