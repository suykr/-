import csv
from reportlab.platypus import BaseDocTemplate, PageTemplate, FrameBreak, PageBreak
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4, mm, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import cidfonts
from reportlab.platypus.frames import Frame
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("HCR Batang", "HANBatang.ttf"))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Hangul", fontName="HCR Batang"))
PS = ParagraphStyle

file_path = "./last.pdf"
doc = BaseDocTemplate(file_path, 
    title="오답노트",
    pagesize=portrait(A4),
    )
width, height = A4  


show = 1
frames = [
    Frame(15*mm, 15*mm, width / 2 - 15*mm, height - 30*mm, showBoundary=show),
    Frame(width / 2, 15*mm, width / 2 - 15*mm, height - 30*mm, showBoundary=show),
]

page_template = PageTemplate("test", frames=frames)
doc.addPageTemplates(page_template)

from reportlab import platypus
import PIL
from io import BytesIO


PS = ParagraphStyle
style_body = PS(name = 'body',
       fontSize = 12,
       leading = 13)


f = open("test.csv", "r", encoding='utf-8')
reader = csv.reader(f)
next(reader)

flowables = []

for row in reader:
    time, name, s, e, m = row
    s = s.split(';')
    for i in s:
        if not i: continue
        flowables.append(Paragraph(name+'-실수', style=styles["Hangul"]))
        x = PIL.Image.open(f"./img/{i}.jpg") 
        imgdata = BytesIO()
        x.save(imgdata,'PNG')
        imgdata.seek(0)
        flowables.append(platypus.Image(imgdata,250, 150))
        flowables.append(FrameBreak())
    e = e.split(';')
    for i in e:
        if not i: continue
        flowables.append(Paragraph(name+'-애매', style=styles["Hangul"]))
        x = PIL.Image.open(f"./img/{i}.jpg") 
        imgdata = BytesIO()
        x.save(imgdata,'PNG')
        imgdata.seek(0)
        flowables.append(platypus.Image(imgdata,250, 150))
        flowables.append(FrameBreak())
    m = m.split(';')
    for i in m:
        if not i: continue
        flowables.append(Paragraph(name+'-모름', style=styles["Hangul"]))
        x = PIL.Image.open(f"./img/{i}.jpg") 
        imgdata = BytesIO()
        x.save(imgdata,'PNG')
        imgdata.seek(0)
        flowables.append(platypus.Image(imgdata,250, 150))
        flowables.append(FrameBreak())
    flowables.append(PageBreak())
    print(name, s, e, m)
    
doc.multiBuild(flowables)
