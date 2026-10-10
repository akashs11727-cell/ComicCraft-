from pathlib import Path
from datetime import datetime
from fpdf import FPDF
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'static'/'exports'; OUT.mkdir(parents=True,exist_ok=True)
def save_pdf(layout):
    path=OUT/f'comic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'; pdf=FPDF(); pdf.set_auto_page_break(True,15)
    for p in layout:
        pdf.add_page(); pdf.set_font('Helvetica','B',18); pdf.multi_cell(0,10,f"Panel {p['panel_number']}: {p['title']}"); img=ROOT/p['image_path'].lstrip('/').replace('static/','static/'); pdf.image(str(img),w=175); pdf.set_font('Helvetica','I',11); pdf.multi_cell(0,7,p['scene_description']); pdf.set_font('Helvetica','',11); pdf.multi_cell(0,7,'Caption: '+p.get('caption','')); pdf.multi_cell(0,7,'Narration: '+p.get('narration','')); pdf.multi_cell(0,7,'Dialogue: '+p.get('dialogue',''))
    pdf.output(str(path)); return f'/static/exports/{path.name}'
