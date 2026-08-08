from typing import Any
from weasyprint import HTML, CSS
from io import BytesIO

def generate_pdf_from_html(html_content: str, paper_size: str = "A4") -> bytes:
    """
    Convert HTML content to a PDF file bytes using WeasyPrint.
    Applies the appropriate page size and margins.
    """
    
    # CSS for the page layout
    if paper_size == "A5":
        page_css = "@page { size: A5 portrait; margin: 15mm; }"
        font_css = "body { font-size: 12pt; font-family: sans-serif; }"
    else:
        page_css = "@page { size: A4 portrait; margin: 20mm; }"
        font_css = "body { font-size: 11pt; font-family: sans-serif; }"
        
    base_css = """
        table { width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 20px; }
        th, td { border: 1px solid #ced4da; padding: 8px; text-align: left; }
        th { background-color: #f1f3f5; font-weight: bold; }
        h1, h2, h3 { margin-top: 10px; margin-bottom: 10px; }
        p { margin-bottom: 8px; line-height: 1.5; }
    """
    
    full_css = CSS(string=f"{page_css} {font_css} {base_css}")
    
    # WeasyPrint requires a full HTML document structure for best results
    full_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Ordonnance</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    pdf_io = BytesIO()
    HTML(string=full_html).write_pdf(pdf_io, stylesheets=[full_css])
    
    return pdf_io.getvalue()
