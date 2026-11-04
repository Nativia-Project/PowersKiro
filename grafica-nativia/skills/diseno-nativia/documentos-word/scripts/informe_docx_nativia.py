"""Formato de marca Nativia para documentos Word (.docx).

SOLO documentos Word. No aplica a las presentaciones HTML (ver assets/plantillas y
references/presentaciones-slides.md), que no se modifican con este script.

Uso:
  python informe_docx_nativia.py --src entrada.docx --out salida.docx \
    --kicker "INFORME EJECUTIVO | FASE 2" --titulo "..." --subtitulo "..." --detalle "..." \
    --dato "Fecha=2026-11-03" --dato "Respaldo=..."

Requisitos: python-docx, lxml. Opcional: LibreOffice (soffice) y pdftotext para calcular los
numeros de pagina reales del indice. Reglas completas en ../README.md.
"""
import docx, copy, re, os, argparse, json, subprocess, tempfile, shutil, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AZUL=RGBColor(0x0A,0x2A,0x43); GRIS=RGBColor(0x58,0x59,0x5B); NAR='F39221'
NEGRO=RGBColor(0x1A,0x1A,0x1A); NARANJA=RGBColor(0xF3,0x92,0x21)  # cuerpo de texto en negro; titulos en azul; acentos en naranja
TITULO='Montserrat'; CUERPO='Inter'
ap=argparse.ArgumentParser(description='Reformatea un .docx (Title, Heading 1, List Bullet, tablas) con la identidad Nativia')
ap.add_argument('--src',required=True); ap.add_argument('--out',required=True)
ap.add_argument('--kicker',default='INFORME'); ap.add_argument('--titulo',required=True)
ap.add_argument('--subtitulo',default=''); ap.add_argument('--detalle',default='')
ap.add_argument('--dato',action='append',default=[],help='CLAVE=valor (repetible)')
ap.add_argument('--paginas',default='',help='json interno con paginas del indice')
A=ap.parse_args()
LOGOS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets')
src=Document(A.src)
R=A.out
d=Document()
from docx.enum.section import WD_SECTION
sec=d.sections[0]
PH=27.94
sec.page_width=Cm(21.59); sec.page_height=Cm(PH)
sec.left_margin=sec.right_margin=sec.top_margin=sec.bottom_margin=Cm(0)
sec.header_distance=Cm(0); sec.footer_distance=Cm(0)
def setfont(run,name,size,bold=False,color=None,italic=False):
    run.font.name=name; run.font.size=Pt(size); run.font.bold=bold; run.font.italic=italic
    rpr=run._element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=OxmlElement('w:rFonts'); rpr.insert(0,rf)
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),name)
    if color is not None: run.font.color.rgb=color
# NEGRITA_MARCADOR delimita los tramos a resaltar en negrita dentro del cuerpo de texto.
# El texto fuente trae pares de este marcador (uno abre, el siguiente cierra); se usa un caracter
# privado poco comun para no chocar con el contenido. emit_runs parte el texto en esos limites y
# pone en negrita los tramos impares, dejando el resto en peso normal.
NEGRITA_MARCADOR='\ue000'
def emit_runs(par,texto,size,color,font=None):
    font=font or CUERPO
    for i,trozo in enumerate(texto.split(NEGRITA_MARCADOR)):
        if not trozo: continue
        r=par.add_run(trozo); setfont(r,font,size,i%2==1,color)
def shade(cell,hexc):
    tcPr=cell._element.get_or_add_tcPr(); s=OxmlElement('w:shd')
    s.set(qn('w:val'),'clear'); s.set(qn('w:color'),'auto'); s.set(qn('w:fill'),hexc); tcPr.append(s)
def borders(cell,**kw):
    tcPr=cell._element.get_or_add_tcPr(); b=OxmlElement('w:tcBorders')
    for edge in ('top','left','bottom','right'):
        e=OxmlElement('w:'+edge); v=kw.get(edge)
        if v: e.set(qn('w:val'),'single'); e.set(qn('w:sz'),str(v[0])); e.set(qn('w:color'),v[1])
        else: e.set(qn('w:val'),'nil')
        b.append(e)
    tcPr.append(b)
def margins(cell,t=100,b=100,l=140,r=140):
    tcPr=cell._element.get_or_add_tcPr(); m=OxmlElement('w:tcMar')
    for k,v in (('top',t),('left',l),('bottom',b),('right',r)):
        e=OxmlElement('w:'+k); e.set(qn('w:w'),str(v)); e.set(qn('w:type'),'dxa'); m.append(e)
    tcPr.append(m)
def spacing(p,before=0,after=6,line=1.3):
    pf=p.paragraph_format; pf.space_before=Pt(before); pf.space_after=Pt(after); pf.line_spacing=line
def pborder(p,edge='bottom',color=NAR,sz=12,space=4):
    pPr=p._p.get_or_add_pPr(); pb=OxmlElement('w:pBdr'); e=OxmlElement('w:'+edge)
    e.set(qn('w:val'),'single'); e.set(qn('w:sz'),str(sz)); e.set(qn('w:space'),str(space)); e.set(qn('w:color'),color)
    pb.append(e); pPr.append(pb)
def field(run,code):
    for t,txt in (('begin',None),(None,code),('end',None)):
        if t:
            f=OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'),t); run._r.append(f)
        else:
            i=OxmlElement('w:instrText'); i.set(qn('xml:space'),'preserve'); i.text=txt; run._r.append(i)

# estilos base
st=d.styles['Normal']; st.font.name=CUERPO; st.font.size=Pt(10.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'),CUERPO)
lg=OxmlElement('w:lang'); lg.set(qn('w:val'),'es-CL'); lg.set(qn('w:eastAsia'),'es-CL'); st.element.rPr.append(lg)
for nm,sz,bf,af in (('Heading 1',16,22,8),('Heading 2',13,14,6)):
    h=d.styles[nm]; h.font.name=TITULO; h.font.size=Pt(sz); h.font.bold=True; h.font.color.rgb=AZUL
    h.element.rPr.rFonts.set(qn('w:ascii'),TITULO); h.element.rPr.rFonts.set(qn('w:hAnsi'),TITULO)
    h.paragraph_format.space_before=Pt(bf); h.paragraph_format.space_after=Pt(af); h.paragraph_format.keep_with_next=True

# ---- portada a pagina completa
# Fondo: un rectangulo Azul Profundo (forma de Word, no imagen) anclado a la esquina de la
# hoja, del tamano exacto de la pagina y detras del texto. Encima va texto real y editable.
from lxml import etree
BL=RGBColor(0xFF,0xFF,0xFF)
sec.left_margin=sec.right_margin=Cm(2.6); sec.top_margin=Cm(2.6); sec.bottom_margin=Cm(1.5)
EMU_W=int(21.59*360000); EMU_H=int(PH*360000)
FONDO=(
 '<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
 'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"><w:drawing>'
 '<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="0" behindDoc="1" '
 'locked="1" layoutInCell="1" allowOverlap="1"><wp:simplePos x="0" y="0"/>'
 '<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
 '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
 '<wp:extent cx="%(w)d" cy="%(h)d"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
 '<wp:docPr id="900" name="Fondo portada"/><wp:cNvGraphicFramePr/>'
 '<a:graphic><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
 '<wps:wsp><wps:cNvSpPr/><wps:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%(w)d" cy="%(h)d"/></a:xfrm>'
 '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="0A2A43"/></a:solidFill>'
 '<a:ln><a:noFill/></a:ln></wps:spPr><wps:bodyPr/></wps:wsp></a:graphicData></a:graphic>'
 '</wp:anchor></w:drawing></w:r>')%{'w':EMU_W,'h':EMU_H}
p=d.paragraphs[0] if d.paragraphs else d.add_paragraph()
spacing(p,0,0,1.0); p._p.append(etree.fromstring(FONDO))
p.add_run().add_picture(os.path.join(LOGOS,'logo-portada-sobre-azul.png'),width=Cm(7.2))
p=d.add_paragraph(); r=p.add_run(A.kicker); setfont(r,TITULO,10.5,True,NARANJA); spacing(p,150,10)
p=d.add_paragraph(); r=p.add_run(A.titulo); setfont(r,TITULO,30,True,BL); spacing(p,0,14,1.05)
p=d.add_paragraph(); pborder(p,'top',NAR,24,1); spacing(p,0,0,1.0)
if A.subtitulo:
    p=d.add_paragraph(); r=p.add_run(A.subtitulo); setfont(r,CUERPO,15,False,BL); spacing(p,8,3)
if A.detalle:
    p=d.add_paragraph(); r=p.add_run(A.detalle); setfont(r,CUERPO,11,False,BL); spacing(p,0,0)
for i_,(k,v) in enumerate(x.split('=',1) for x in A.dato):
    p=d.add_paragraph(); spacing(p,60 if i_==0 else 0,3)
    r=p.add_run(k.strip().upper()+'   '); setfont(r,TITULO,8.5,True,NARANJA)
    r=p.add_run(v.strip()); setfont(r,CUERPO,10,False,BL)
pcov=p
# la seccion de portada no lleva encabezado ni pie: asi toda la altura de la hoja queda para la imagen
sec2=d.add_section(WD_SECTION.NEW_PAGE)
sec2.left_margin=sec2.right_margin=Cm(2.3); sec2.top_margin=Cm(2.4); sec2.bottom_margin=Cm(2.2)
sec2.header_distance=Cm(1.0); sec2.footer_distance=Cm(1.0)
sec2.header.is_linked_to_previous=False; sec2.footer.is_linked_to_previous=False
sec=sec2
_body=d.element.body
for _p in list(_body.iterchildren(qn('w:p'))):
    _sp=_p.find(qn('w:pPr')+'/'+qn('w:sectPr'))
    if _sp is not None:
        if _p is not pcov._p:
            pcov._p.get_or_add_pPr().append(_sp); _body.remove(_p)
        break

# ---- encabezado / pie
hp=sec.header.paragraphs[0]; hp.add_run().add_picture(os.path.join(LOGOS,'glifo-encabezado.png'),width=Cm(1.3))
r=hp.add_run('   '+A.kicker.split('|')[0].strip().capitalize()+'  |  '+A.titulo[:70]); setfont(r,CUERPO,8.5,False,GRIS)
pborder(hp,'bottom','0A2A43',6,6)
fp=sec.footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=fp.add_run('Nativia - Cloud & IA   |   Página '); setfont(r,CUERPO,8.5,False,GRIS)
r=fp.add_run(); setfont(r,CUERPO,8.5,True,AZUL); field(r,'PAGE')

# ---- cuerpo
def add_table(t):
    rows=len(t.rows); cols=len(t.columns)
    nt=d.add_table(rows=rows,cols=cols); nt.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,row in enumerate(t.rows):
        for j,cell in enumerate(row.cells):
            c=nt.cell(i,j); txt=cell.text.strip(); p=c.paragraphs[0]; spacing(p,3,3,1.2); margins(c); p.paragraph_format.left_indent=Cm(0.15); p.paragraph_format.right_indent=Cm(0.15)
            if i==0:
                shade(c,'0A2A43'); borders(c); r=p.add_run(txt); setfont(r,TITULO,9,True,RGBColor(255,255,255))
            else:
                shade(c,'EEF2F6' if i%2==0 else 'FFFFFF'); borders(c,bottom=(4,'C9D3DC'))
                if j==0 or NEGRITA_MARCADOR not in txt:
                    # primera columna (encabezado de fila) siempre en negrita; o celda sin marcador
                    r=p.add_run(txt.replace(NEGRITA_MARCADOR,'')); setfont(r,CUERPO,9.5,j==0,NEGRO)
                else:
                    emit_runs(p,txt,9.5,NEGRO)
        if i==0:
            trPr=nt.rows[0]._tr.get_or_add_trPr(); th=OxmlElement('w:tblHeader'); trPr.append(th)
        
        for c_ in nt.rows[i].cells:
            c_.paragraphs[0].paragraph_format.keep_with_next=(i<rows-1)
        cs=nt.rows[i]._tr.get_or_add_trPr(); cant=OxmlElement('w:cantSplit'); cs.append(cant)
    # anchos
    from docx.shared import Cm as C
    w=16.9
    if cols==3: ws=[w*.34,w*.33,w*.33]
    else: ws=[w*.4,w*.6]
    for row in nt.rows:
        for j,c in enumerate(row.cells): c.width=C(ws[j])
    sp=d.add_paragraph(); spacing(sp,0,4)

# ---- numeracion de encabezados e indice
NUM=re.compile(r'^\d+(\.\d+)*\.?\s')
heads=[]; c1=c2=0
for p_ in src.paragraphs:
    sn=p_.style.name; t_=p_.text.strip()
    if sn not in ('Heading 1','Heading 2') or not t_: continue
    if sn=='Heading 1':
        c1+=1; c2=0; lvl=1; t_=t_ if NUM.match(t_) else '%d. %s'%(c1,t_)
    else:
        c2+=1; lvl=2; t_=t_ if NUM.match(t_) else '%d.%d %s'%(c1,c2,t_)
    heads.append((lvl,t_,p_._p))
HTXT={h[2]:h[1] for h in heads}
PAG=json.load(open(A.paginas)) if A.paginas and os.path.exists(A.paginas) else {}
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
p=d.add_paragraph(); r=p.add_run('Índice'); setfont(r,TITULO,22,True,AZUL); spacing(p,0,4); pborder(p,'bottom',NAR,12,6)
p=d.add_paragraph(); spacing(p,0,6)
for i,(lvl,t_,_) in enumerate(heads):
    p=d.add_paragraph(); spacing(p,6 if lvl==1 else 0,3,1.2)
    p.paragraph_format.left_indent=Cm(0 if lvl==1 else 0.8)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16.9),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
    if i==0:
        r0=p.add_run(); fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),'begin'); r0._r.append(fc)
        it=OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text=' TOC \\o "1-2" \\h \\z \\u '; r0._r.append(it)
        fs=OxmlElement('w:fldChar'); fs.set(qn('w:fldCharType'),'separate'); r0._r.append(fs)
    r=p.add_run(t_+'\t'+str(PAG.get(t_,'')) ); setfont(r,TITULO if lvl==1 else CUERPO,10.5 if lvl==1 else 10,lvl==1,AZUL if lvl==1 else GRIS)
    if i==len(heads)-1:
        r1=p.add_run(); fe=OxmlElement('w:fldChar'); fe.set(qn('w:fldCharType'),'end'); r1._r.append(fe)
d.add_page_break()

body=src.element.body
pmap={p._p:p for p in src.paragraphs}; tmap={t._tbl:t for t in src.tables}
first=True
for el in body.iterchildren():
    if el in pmap:
        p=pmap[el]; s=p.style.name; txt=p.text.strip()
        if s=='Title' or (not txt) or (p._p is src.paragraphs[1]._p and p.style.name=='Normal' and ':' in txt[:25]): continue
        if s=='Heading 1':
            np_=d.add_paragraph(style='Heading 1'); r=np_.add_run(HTXT.get(el,txt)); setfont(r,TITULO,16,True,AZUL)
            if first: first=False
        elif s=='Heading 2':
            np_=d.add_paragraph(style='Heading 2'); r=np_.add_run(HTXT.get(el,txt)); setfont(r,TITULO,13,True,AZUL)
        elif s=='List Bullet':
            np_=d.add_paragraph(style='List Bullet'); spacing(np_,0,4)
            emit_runs(np_,txt,10.5,NEGRO)
        else:
            np_=d.add_paragraph(); spacing(np_,0,8); np_.alignment=WD_ALIGN_PARAGRAPH.LEFT
            m=re.match(r'^([^.:]{2,32}\.)\s(.+)$',txt,re.S)
            if m and len(m.group(1).split())>5: m=None
            if m:
                r=np_.add_run(m.group(1)+' '); setfont(r,CUERPO,10.5,True,AZUL)
                emit_runs(np_,m.group(2),10.5,NEGRO)
            else:
                emit_runs(np_,txt,10.5,NEGRO)
    elif el in tmap:
        add_table(tmap[el])
d.core_properties.title=A.titulo
d.core_properties.author='Nativia'
ORD={'tcPr':['cnfStyle','tcW','gridSpan','hMerge','vMerge','tcBorders','shd','noWrap','tcMar','textDirection','tcFitText','vAlign','hideMark'],
 'pPr':['pStyle','keepNext','keepLines','pageBreakBefore','framePr','widowControl','numPr','suppressLineNumbers','pBdr','shd','tabs','suppressAutoHyphens','kinsoku','wordWrap','overflowPunct','topLinePunct','autoSpaceDE','autoSpaceDN','bidi','adjustRightInd','snapToGrid','spacing','ind','contextualSpacing','mirrorIndents','suppressOverlap','jc','textDirection','textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr','sectPr','pPrChange'],
 'tblPr':['tblStyle','tblpPr','tblOverlap','bidiVisual','tblStyleRowBandSize','tblStyleColBandSize','tblW','jc','tblCellSpacing','tblInd','tblBorders','shd','tblLayout','tblCellMar','tblLook'],
 'trPr':['cnfStyle','divId','gridBefore','gridAfter','wBefore','wAfter','cantSplit','trHeight','tblHeader','tblCellSpacing','jc','hidden'],
 'rPr':['rStyle','rFonts','b','bCs','i','iCs','caps','smallCaps','strike','dstrike','outline','shadow','emboss','imprint','noProof','snapToGrid','vanish','webHidden','color','spacing','w','kern','position','sz','szCs','highlight','u','effect','bdr','shd','fitText','vertAlign','rtl','cs','em','lang','eastAsianLayout','specVanish','oMath']}
def reorden(root):
    for tag,orden in ORD.items():
        for pr in root.iter(qn('w:'+tag)):
            hijos=list(pr)
            k=lambda e:(orden.index(e.tag.split('}')[1]) if e.tag.split('}')[1] in orden else 99)
            for h in hijos: pr.remove(h)
            for h in sorted(hijos,key=k): pr.append(h)
reorden(d.element); reorden(d.styles.element)
for sc in d.sections:
    # solo encabezados ya definidos: acceder a uno vinculado lo crearia (y la portada no lleva)
    for hf in (sc.header, sc.footer):
        if not hf.is_linked_to_previous: reorden(hf._element)
d.save(R)

# ---- segunda pasada: calcular paginas reales del indice con LibreOffice
def paginas_reales():
    so=shutil.which('soffice') or shutil.which('libreoffice'); pt=shutil.which('pdftotext')
    if not so or not pt: return None
    tmp=tempfile.mkdtemp()
    subprocess.run([so,'--headless','--convert-to','pdf','--outdir',tmp,R],capture_output=True,timeout=180)
    pdf=os.path.join(tmp,os.path.splitext(os.path.basename(R))[0]+'.pdf')
    if not os.path.exists(pdf): return None
    txt=subprocess.run([pt,'-layout',pdf,'-'],capture_output=True,text=True).stdout.split('\f')
    out={}
    for lvl,t_,_ in heads:
        clave=re.sub(r'\s+',' ',t_)[:32]
        for n,pg in enumerate(txt,1):
            if n<3: continue
            if any(re.sub(r'\s+',' ',l).strip().startswith(clave) for l in pg.splitlines()):
                out[t_]=n; break
    shutil.rmtree(tmp,ignore_errors=True)
    return out
if not A.paginas:
    pr=paginas_reales()
    if pr and pr!=PAG:
        jf=R+'.paginas.json'; json.dump(pr,open(jf,'w'))
        subprocess.run([sys.executable]+sys.argv+['--paginas',jf],check=True)
        os.remove(jf)

