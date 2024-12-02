import csv
from reportlab.platypus import BaseDocTemplate, PageTemplate, FrameBreak, PageBreak
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4, mm, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import cidfonts
from reportlab.platypus.frames import Frame
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import platypus
import PIL
from io import BytesIO

pdfmetrics.registerFont(TTFont("HCR Batang", "HANBatang.ttf"))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Hangul", fontName="HCR Batang"))
PS = ParagraphStyle


def makePDF(file_path):
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
    doc.multiBuild(flowables)

PS = ParagraphStyle
style_body = PS(name = 'body',
       fontSize = 12,
       leading = 13)

f = open("test.csv", "r", encoding='utf-8')
reader = csv.reader(f)
next(reader)

flowables = []

def insertImg(name, label, i):
    flowables.append(Paragraph(name+label, style=styles["Hangul"]))
    x = PIL.Image.open(f"./img/{i}.jpg") 
    imgdata = BytesIO()
    x.save(imgdata,'PNG')
    imgdata.seek(0)
    flowables.append(platypus.Image(imgdata,250, 250*(x.height/x.width)))
    flowables.append(FrameBreak())

for row in reader:
    time, name, s, e, m = row
    s = s.split(';')
    for i in s:
        if not i: continue
        insertImg(name, '-실수', i)
    e = e.split(';')
    for i in e:
        if not i: continue
        insertImg(name, '-애매', i)
    m = m.split(';')
    for i in m:
        if not i: continue
        insertImg(name, '-모름', i)
    makePDF(f'./{name}.pdf')
    del flowables
    flowables = []
    print(name, s, e, m)
