from pathlib import Path
import math
import struct
import wave
import zipfile

out=Path(__import__('os').environ.get('TRACE_ACCEPTANCE_FIXTURE_DIR','acceptance-fixtures'))
out.mkdir(parents=True,exist_ok=True)

(out/'interview.txt').write_text(
    'P01: Access to support was difficult at first, but peer help changed the experience.\n'
    'P01: Once I knew who to ask, the process felt more manageable.\n',
    encoding='utf-8'
)

# Minimal but genuine XLSX workbook. Trace's parser supports inline-string cells.
content_types='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="xml" ContentType="application/xml"/>
 <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
 <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''
rels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''
workbook='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <sheets><sheet name="Participants" sheetId="1" r:id="rId1"/></sheets>
</workbook>'''
workbook_rels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>'''
rows=[
    ['Participant ID','Role','Region','Years teaching'],
    ['P01','Teacher','Greater Accra','4'],
    ['P02','Teacher','Eastern','6'],
]
def cell(ref,value):
    return f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>'
letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
row_xml=[]
for ri,row in enumerate(rows,1):
    row_xml.append('<row r="%d">%s</row>'%(ri,''.join(cell(f'{letters[ci]}{ri}',v) for ci,v in enumerate(row))))
sheet='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>%s</sheetData></worksheet>'''%''.join(row_xml)
with zipfile.ZipFile(out/'participants.xlsx','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml',content_types)
    z.writestr('_rels/.rels',rels)
    z.writestr('xl/workbook.xml',workbook)
    z.writestr('xl/_rels/workbook.xml.rels',workbook_rels)
    z.writestr('xl/worksheets/sheet1.xml',sheet)

# Small valid single-page PDF with searchable text.
stream=b'BT /F1 12 Tf 72 720 Td (Support access PDF evidence for Trace acceptance.) Tj ET'
objects=[
    b'<< /Type /Catalog /Pages 2 0 R >>',
    b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>',
    b'<< /Length %d >>\nstream\n'%len(stream)+stream+b'\nendstream',
    b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
]
pdf=bytearray(b'%PDF-1.4\n')
offsets=[0]
for idx,obj in enumerate(objects,1):
    offsets.append(len(pdf))
    pdf.extend(f'{idx} 0 obj\n'.encode())
    pdf.extend(obj)
    pdf.extend(b'\nendobj\n')
xref=len(pdf)
pdf.extend(f'xref\n0 {len(objects)+1}\n'.encode())
pdf.extend(b'0000000000 65535 f \n')
for off in offsets[1:]: pdf.extend(f'{off:010d} 00000 n \n'.encode())
pdf.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
(out/'evidence.pdf').write_bytes(pdf)

# One-second, mono PCM WAV. It is real decodable media without external codecs.
rate=16000
with wave.open(str(out/'interview-audio.wav'),'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate)
    frames=bytearray()
    for i in range(rate):
        sample=int(1200*math.sin(2*math.pi*220*i/rate))
        frames.extend(struct.pack('<h',sample))
    w.writeframes(frames)

for name in ('interview.txt','participants.xlsx','evidence.pdf','interview-audio.wav'):
    p=out/name
    if not p.exists() or p.stat().st_size<10: raise SystemExit(f'Acceptance fixture was not created correctly: {name}')
print('Trace acceptance fixtures created:', ', '.join(p.name for p in out.iterdir()))
