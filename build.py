#!/usr/bin/env python3
"""Erzeugt alle statischen Seiten des DICOM Viewers. Aufruf: python3 build.py"""
import json, os, html
BASE = "https://freimoser.github.io/dicom-viewer/"
P = "/dicom-viewer/"
LASTMOD = "2026-10-17"
GA_ID = ""  # GA4 Mess-ID, z. B. "G-XXXXXXX". Leer = kein Analytics, kein Banner.
LINKEDIN = "https://www.linkedin.com/in/freimoser"
MDR = "Nur zur Ansicht, nicht zur Diagnose. Kein Medizinprodukt."
NAV = [("", "Viewer"), ("radiologie-cd-oeffnen/", "Radiologie-CD öffnen"), ("dicom-in-jpg/", "DICOM in JPG"),
       ("dicom-viewer-mac/", "Mac"), ("dicom-iphone/", "iPhone"), ("mrt-bilder-verstehen/", "MRT verstehen"), ("medizinische-datenformate/", "Datenformate")]

def ga_snippet():
    if not GA_ID:
        return ""
    return f'''<div id="cc" class="cc" hidden><p>Darf ich mit Google Analytics anonym messen, welche Seiten genutzt werden? Ihre DICOM-Bilder werden dabei nie erfasst. <a href="{P}datenschutz/">Datenschutz</a></p><div class="btns"><button class="btn pri" type="button" id="ccYes">Zustimmen</button><button class="btn" type="button" id="ccNo">Ablehnen</button></div></div>
<script>(function(){{var K="dv-consent",v=localStorage.getItem(K),b=document.getElementById("cc");
function load(){{window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}window.gtag=gtag;
gtag("consent","default",{{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"granted"}});
gtag("js",new Date());gtag("config","{GA_ID}",{{anonymize_ip:true}});var s=document.createElement("script");s.async=1;s.src="https://www.googletagmanager.com/gtag/js?id={GA_ID}";document.head.appendChild(s);}}
if(v==="yes")load();else if(v!=="no")b.hidden=false;
document.getElementById("ccYes").onclick=function(){{localStorage.setItem(K,"yes");b.hidden=true;load();}};
document.getElementById("ccNo").onclick=function(){{localStorage.setItem(K,"no");b.hidden=true;}};
window.dvConsentReset=function(){{localStorage.removeItem(K);b.hidden=false;}};}})();</script>'''

CROSS = '''<aside class="xlink"><h2>Auch für Praxis-Dateien: LDT, BDT und GDT</h2><p>Laborbefunde, Praxisdaten-Exporte und Gerätedaten liegen nicht als DICOM vor, sondern in den xDT-Formaten der KBV. Dafür gibt es zwei passende kostenlose Viewer – ebenfalls ohne Upload:</p><div class="btns"><a class="btn pri" href="https://freimoser.github.io/ldt-bdt-viewer/">LDT &amp; BDT Viewer öffnen →</a><a class="btn pri" href="https://freimoser.github.io/gdt-viewer/">GDT Viewer öffnen →</a><a class="btn" href="https://freimoser.github.io/pdf-schwaerzen/">PDF schwärzen (Befund, Arztbrief) →</a></div><p class="small">Hintergrund: <a href="/dicom-viewer/ldt-bdt-gdt-dateien-oeffnen/">LDT, BDT und GDT öffnen</a> · <a href="/dicom-viewer/laborbefund-ldt-verstehen/">Laborbefunde (LDT) verstehen</a> · <a href="/dicom-viewer/medizinische-datenformate/">DICOM, LDT, BDT, GDT im Vergleich</a></p></aside>'''

ABOUT = f'''<section class="about"><div class="wrap"><img src="/dicom-viewer/favicon.svg" alt="" width="44" height="44"><div><h2>Über den Entwickler</h2><p><strong>Thomas Freimoser</strong> entwickelt kostenlose, datensparsame Web-Tools für Praxen, Labore und Patientinnen und Patienten – alles läuft im Browser, nichts wird hochgeladen. München / Remote.</p><div class="btns"><a class="btn" href="https://freimoser.de/">🌐 freimoser.de</a><a class="btn" href="{LINKEDIN}" rel="noopener" target="_blank">in LinkedIn</a><a class="btn" href="https://freimoser.de/projekte/">Alle Projekte</a></div></div></div></section>'''

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs):
    return "<h2>Häufige Fragen</h2>" + "".join(f'<details class="faq"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faqs)

def page(path, title, desc, h1, lead, body, faqs, extra_ld=None, tool=False):
    url = BASE + path
    lds = [faq_ld(faqs)] + ([extra_ld] if extra_ld else [])
    lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "DICOM Viewer", "item": BASE}] + ([{"@type": "ListItem", "position": 2, "name": h1, "item": url}] if path else [])})
    nav = "".join(f'<a href="{P}{p}"{" aria-current=\"page\"" if p == path else ""}>{n}</a>' for p, n in NAV)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    tool_html = TOOL if tool else f'<p><a class="btn pri" href="{P}">DICOM Viewer öffnen →</a></p>'
    scripts = f'<script src="{P}vendor/dicomParser.min.js"></script><script src="{P}app.js"></script>' if tool else ""
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="google-site-verification" content="6pYvtFCnU7UFcQFajtMSkQ7tYMy3Z_Bt7teKiT5yKNg" />
<meta name="msvalidate.01" content="E1F30DEB311AAF5458907DB431B481AC" />
<meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:site_name" content="DICOM Viewer">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}icon-512.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0b1117">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml"><link rel="icon" href="{P}favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{P}apple-touch-icon.png">
<link rel="stylesheet" href="{P}styles.css">
{ld}
<meta name="author" content="Thomas Freimoser">
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="{P}"><img src="{P}favicon.svg" alt="" width="28" height="28">DICOM Viewer</a><nav class="main">{nav}</nav></div></header>
<main class="wrap">
<div class="mdr" role="note">⚠️ {MDR} Ihre Dateien bleiben auf Ihrem Gerät – es gibt keinen Upload.</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{tool_html}
<div class="content">{body}{CROSS if not path.startswith(("ldt-","laborbefund","medizinische","datenschutz","404")) else ""}{faq_html(faqs) if faqs else ""}</div>
</main>
{ABOUT}
<footer><div class="wrap">
<p><strong>Weitere kostenlose Praxis-Tools:</strong></p>
<div class="cols"><a href="https://freimoser.github.io/gdt-viewer/">GDT Viewer</a><a href="https://freimoser.github.io/ldt-bdt-viewer/">LDT &amp; BDT Viewer</a><a href="https://freimoser.github.io/e-rechnung-klartext/">E-Rechnung Klartext</a><a href="https://freimoser.de/">Portfolio Thomas Freimoser</a></div>
<p class="cols" style="margin-top:12px"><a href="https://freimoser.github.io/freimoser.de/impressum/">Impressum</a><a href="{P}datenschutz/">Datenschutz</a><span>{MDR}</span></p>
<p>Open-Source-Bausteine: <a href="https://github.com/cornerstonejs/dicomParser">dicomParser</a> (MIT, © Chris Hafey), <a href="https://github.com/cornerstonejs/codecs">codec-openjpeg und codec-charls</a> (MIT, © Chris Hafey) mit OpenJPEG (BSD-2) und CharLS (BSD-3), <a href="https://github.com/rii-mango/JPEGLosslessDecoderJS">jpeg-lossless-decoder-js</a> (MIT, © RII-UTHSCSA), JPEG-Decoder aus cornerstone3D (MIT) auf Basis von pdf.js (Apache-2.0, © Mozilla). <a href="https://github.com/freimoser/dicom-viewer/blob/main/THIRD-PARTY-LICENSES">Alle Lizenztexte</a>. Gebaut in München / Remote.</p>
</div></footer>
{scripts}
{ga_snippet()}
</body></html>
'''

TOOL = '''
<section class="drop" id="drop" aria-label="Dateien laden">
<p><strong>DICOM-Dateien oder den ganzen Ordner der CD hierher ziehen</strong></p>
<div class="btns">
<label class="btn pri">📁 Ordner / CD wählen<input type="file" id="dirIn" webkitdirectory directory multiple></label>
<label class="btn">📄 Dateien wählen<input type="file" id="fileIn" multiple></label>
</div>
<p style="color:var(--mu);font-size:.88rem;margin:10px 0 0">Erkennt DICOMDIR und Dateien ohne Endung. Unterstützt unkomprimierte Bilder, JPEG, JPEG Lossless, JPEG-LS, JPEG 2000 und RLE.</p>
</section>
<div class="msg" id="msg" hidden></div>
<section class="app" id="app" hidden>
<aside class="side" id="tree" aria-label="Patienten, Studien und Serien"></aside>
<div class="main">
<div class="tools">
<button class="btn on" data-mode="wl" type="button" title="Linke Maustaste ziehen: Helligkeit/Kontrast">◐ Fenster</button>
<button class="btn" data-mode="pan" type="button">✋ Verschieben</button>
<button class="btn" data-mode="zoom" type="button">🔍 Zoom</button>
<button class="btn" data-mode="scroll" type="button">↕ Blättern</button>
<select id="presets" aria-label="Fenster-Vorgaben"><option value="">Fenster-Vorgabe …</option><option value="40,400">Weichteil</option><option value="-600,1500">Lunge</option><option value="400,1800">Knochen</option><option value="40,80">Gehirn</option></select>
<button class="btn" data-mode="redact" type="button" title="Rechteck aufziehen, um eingebrannte Namen zu übermalen">⬛ Schwärzen</button>
<button class="btn" id="unredact" type="button">Schwärzung löschen</button>
<button class="btn" id="invert" type="button">Invertieren</button>
<button class="btn" id="reset" type="button">Zurücksetzen</button>
<button class="btn pri" id="png" type="button">PNG ⬇</button>
<button class="btn" id="jpg" type="button">JPG ⬇</button>
</div>
<div class="stage"><canvas id="view" aria-label="DICOM-Bild"></canvas><div class="ov" id="ovTL"></div><div class="ov" id="ovTR"></div><div class="ov" id="ovBL"></div><div class="ov" id="ovBR"><span id="wlLbl"></span>  <span id="zoomLbl"></span></div><div class="err" id="err" hidden></div></div>
<div class="slicebar"><input type="range" id="slice" min="0" max="0" value="0" aria-label="Schicht"><span id="sliceLbl">–</span></div>
<div class="checks"><label><input type="checkbox" id="phiToggle"> Patientendaten anzeigen</label><label><input type="checkbox" id="phiExport" disabled> Name im Export einbrennen</label></div>
<div class="mdr" style="margin:8px 0">⚠️ Vor dem Export: <strong>Bild auf eingebrannte Namen prüfen!</strong> Bei Ultraschall- und Röntgenaufnahmen steht der Name oft direkt im Pixelbild. Mit „⬛ Schwärzen“ ein Rechteck darüber ziehen – die Schwärzung wird mit exportiert.</div>
<p style="color:var(--mu);font-size:.88rem;margin:0">🔒 <strong>Anonymer Export:</strong> PNG und JPG enthalten standardmäßig nur das Bild – ohne Name, Geburtsdatum, ID oder DICOM-Metadaten. Achtung: Manche Geräte brennen Text direkt ins Bild; den prüfen Sie bitte vor dem Weitergeben selbst. Mausrad = Schichten, <kbd>Strg</kbd>+Mausrad = Zoom, mittlere Taste = Verschieben.</p>
<div class="tagbox"><h3>DICOM-Tags</h3><input id="tagFilter" placeholder="Tags filtern, z. B. 0008 oder Modalität"><div class="tablewrap"><table><thead><tr><th>Tag</th><th>VR</th><th>Name</th><th>Wert</th></tr></thead><tbody id="tagBody"></tbody></table></div></div>
</div>
</section>
'''

APP_LD = {"@context": "https://schema.org", "@type": "WebApplication", "name": "DICOM Viewer", "url": BASE,
  "description": "Kostenloser DICOM Viewer im Browser: Röntgen-, CT- und MRT-Bilder und Radiologie-CDs ohne Installation und ohne Upload ansehen, anonym als PNG oder JPG exportieren.",
  "applicationCategory": "MultimediaApplication", "operatingSystem": "Windows, macOS, Linux, iOS, Android", "browserRequirements": "Requires JavaScript",
  "inLanguage": "de-DE", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
  "featureList": ["Ordner und Radiologie-CDs laden, DICOMDIR erkennen", "Gruppierung nach Patient, Studie und Serie", "Fenster/Level, Zoom, Verschieben, Schichten blättern",
                  "DICOM-Tag-Ansicht", "Anonymer Export als PNG und JPG", "Keine Datenübertragung, alles lokal"],
  "disambiguatingDescription": MDR}

PAGES = []
PAGES.append(("", page("", "DICOM Viewer kostenlos online – ohne Installation, ohne Upload",
  "DICOM Viewer kostenlos im Browser: Röntgen-, CT- und MRT-Bilder und ganze Radiologie-CDs ansehen. Keine Installation, kein Upload, anonymer PNG/JPG-Export.",
  "DICOM Viewer kostenlos online",
  "Röntgen-, CT- und MRT-Bilder direkt im Browser öffnen – auch den kompletten Ordner einer Radiologie-CD. Keine Installation, keine Anmeldung und kein Upload: Die Dateien werden ausschließlich auf Ihrem Gerät gelesen.",
  '''<h2>So funktioniert der Viewer</h2>
<ol><li><strong>Laden:</strong> Ziehen Sie einzelne .dcm-Dateien oder den ganzen CD-Ordner in das Feld oben oder klicken Sie auf „Ordner / CD wählen“.</li>
<li><strong>Auswählen:</strong> Links erscheinen alle Patienten, Studien und Serien mit Vorschaubild. Ein Klick öffnet die Serie.</li>
<li><strong>Ansehen:</strong> Mit dem Mausrad oder dem Schieberegler blättern Sie durch die Schichten. Linke Maustaste ziehen ändert Helligkeit und Kontrast (Fenster/Level), <kbd>Strg</kbd>+Mausrad zoomt.</li>
<li><strong>Exportieren:</strong> Das aktuelle Bild lässt sich als PNG oder JPG speichern – standardmäßig ohne Patientendaten.</li></ol>
<div class="grid3">
<div class="card"><h3>🔒 Bleibt auf Ihrem Gerät</h3><p>Die Seite ist rein statisch. Ihre Bilder werden per JavaScript lokal gelesen und nie an einen Server geschickt. Sie können die Seite nach dem Laden sogar offline nutzen.</p></div>
<div class="card"><h3>🕶️ Anonymer Export</h3><p>Exportierte Bilder enthalten nur Pixel – keinen Namen, kein Geburtsdatum, keine Metadaten. Ideal, um ein Bild an Familie, Trainer oder ein Forum weiterzugeben.</p></div>
<div class="card"><h3>💿 CD-tauglich</h3><p>DICOMDIR wird erkannt, Dateien ohne Endung (z. B. <code>IM000001</code>) werden über die DICOM-Kennung „DICM“ gefunden.</p></div></div>
<h2>Welche Dateien werden unterstützt?</h2>
<p>Unkomprimierte DICOM-Bilder (Implicit/Explicit VR Little Endian, Explicit VR Big Endian) in 8, 16 und 32 Bit, Graustufen und Farbe, auch Mehrbild-Dateien (Multiframe) wie Ultraschall-Clips. Dazu alle auf Radiologie-CDs üblichen Kompressionen: JPEG Baseline und Extended (8/12 Bit), JPEG Lossless, JPEG-LS (verlustfrei und nahezu verlustfrei), JPEG 2000 (verlustfrei und verlustbehaftet) sowie RLE. Die nötigen Decoder werden erst nachgeladen, wenn ein solches Bild auftaucht – ebenfalls lokal, ohne dass Bilddaten Ihr Gerät verlassen. Nur seltene Exoten (z. B. Deflate, HTJ2K, Video-Formate) zeigen einen klaren Hinweis statt eines leeren Bildes.</p>
<h2>Was der Viewer bewusst nicht kann</h2>
<p>Es gibt keine Mess-, Markierungs- oder Befundwerkzeuge. Der Viewer ist zum Anschauen gedacht, etwa um vor dem Arzttermin die eigenen Bilder zu sehen. {MDR} Die Beurteilung Ihrer Bilder gehört in ärztliche Hände.</p>
<p>Mehr dazu: <a href="radiologie-cd-oeffnen/">Radiologie-CD öffnen</a> · <a href="dicom-in-jpg/">DICOM in JPG umwandeln</a> · <a href="dicom-viewer-mac/">DICOM am Mac</a> · <a href="dicom-iphone/">DICOM am iPhone</a> · <a href="mrt-bilder-verstehen/">MRT-Bilder verstehen</a> · <a href="medizinische-datenformate/">DICOM, LDT, BDT, GDT</a></p>
<h2>Was ist DICOM?</h2>
<p>DICOM (Digital Imaging and Communications in Medicine) ist der weltweite Standard für medizinische Bilder. Eine DICOM-Datei enthält das Bild selbst und zusätzlich Angaben wie Patientenname, Untersuchungsdatum, Gerät, Schichtdicke und Kontrastvorgaben. Deshalb öffnen normale Bildbetrachter diese Dateien nicht: Sie kennen weder das Format noch die 12- oder 16-Bit-Graustufen, die ein CT liefert.</p>'''.replace("{MDR}", MDR),
  [("Ist der DICOM Viewer wirklich kostenlos?", "Ja. Keine Anmeldung, keine Werbung im Viewer, keine Testphase."),
   ("Werden meine Bilder hochgeladen?", "Nein. Die Dateien werden ausschließlich in Ihrem Browser gelesen. Es gibt keinen Server, der sie empfängt."),
   ("Kann ich damit eine Diagnose stellen?", "Nein. Der Viewer ist kein Medizinprodukt und hat bewusst keine Mess- oder Befundfunktionen. Er dient nur zur Ansicht."),
   ("Warum sehe ich nur eine Fehlermeldung?", "Dann ist das Bild in einem seltenen Format gespeichert, etwa Deflate, HTJ2K oder als Video (MPEG/H.264). Die Meldung nennt das genaue Format. JPEG, JPEG Lossless, JPEG-LS, JPEG 2000 und RLE werden unterstützt."),
   ("Funktioniert es auf dem Handy?", "Ja, in aktuellen Browsern auf Android und iPhone. Für große CT-Serien ist ein Computer angenehmer.")],
  APP_LD, tool=True)))

PAGES.append(("radiologie-cd-oeffnen/", page("radiologie-cd-oeffnen/", "Radiologie-CD öffnen am PC und Mac – ohne Installation",
  "Radiologie-CD oder MRT-CD öffnen, auch wenn der mitgelieferte Viewer nicht startet: DICOMDIR erklärt, Schritt-für-Schritt für Windows und Mac, kostenlos im Browser.",
  "Radiologie-CD öffnen – am PC und am Mac",
  "Sie haben nach dem MRT oder CT eine CD bekommen, aber der Viewer darauf startet nicht? So sehen Sie Ihre Bilder trotzdem an – kostenlos und ohne etwas zu installieren.",
  '''<h2>Was ist auf einer Radiologie-CD?</h2>
<p>Typisch sind drei Dinge: eine Datei namens <code>DICOMDIR</code> (das Inhaltsverzeichnis), ein Ordner wie <code>DICOM</code> oder <code>IMAGES</code> mit hunderten Einzelbildern ohne Dateiendung, und oft ein mitgelieferter Windows-Viewer samt <code>autorun.inf</code>. Die Bilder selbst sind immer DICOM-Dateien – nur der Viewer ist austauschbar.</p>
<h2>Warum startet der CD-Viewer nicht?</h2>
<ul><li><strong>Mac:</strong> Der mitgelieferte Viewer ist fast immer ein Windows-Programm (.exe). macOS kann ihn nicht ausführen.</li>
<li><strong>Windows 10/11:</strong> Autostart von CDs ist meist deaktiviert, oder der alte Viewer wird von Virenschutz bzw. SmartScreen blockiert.</li>
<li><strong>Kein Laufwerk:</strong> Viele Laptops haben kein CD-Laufwerk mehr. Ein externes USB-Laufwerk für rund 20 € hilft, alternativ kopiert jemand den CD-Inhalt auf einen USB-Stick.</li>
<li><strong>Firmen-PC:</strong> Ohne Administratorrechte darf man nichts installieren.</li></ul>
<h2>Schritt für Schritt</h2>
<ol><li>CD einlegen (oder den kopierten Ordner bereithalten).</li>
<li>Den <a href="../">DICOM Viewer</a> öffnen und auf <strong>„Ordner / CD wählen“</strong> klicken.</li>
<li>Das CD-Laufwerk bzw. den obersten Ordner der CD auswählen und bestätigen. Der Browser fragt eventuell, ob Sie die Dateien „hochladen“ möchten – das ist nur die Standardformulierung; die Daten verlassen Ihren Rechner nicht.</li>
<li>Links erscheinen alle Untersuchungen und Serien. Serie anklicken, mit dem Mausrad blättern.</li></ol>
<p>Alternativ den ganzen CD-Ordner per Drag &amp; Drop auf die Seite ziehen.</p>
<h2>Die Rolle der DICOMDIR-Datei</h2>
<p>Das DICOMDIR listet auf, welche Datei zu welchem Patienten, welcher Studie und welcher Serie gehört. Der Viewer erkennt es, liest aber die Bilder direkt und sortiert sie selbst anhand ihrer eingebetteten Angaben. Wählen Sie deshalb immer den <em>ganzen</em> Ordner, nicht nur die DICOMDIR-Datei – sie enthält keine Bilder.</p>
<h2>Bilder sichern</h2>
<p>CDs altern. Kopieren Sie den kompletten Inhalt in einen Ordner auf Ihrem Rechner oder einen USB-Stick, dann können Sie die Bilder auch ohne Laufwerk jederzeit wieder öffnen. Einzelne Aufnahmen für Angehörige exportieren Sie anonym als <a href="../dicom-in-jpg/">JPG oder PNG</a>.</p>''',
  [("Brauche ich das Programm von der CD?", "Nein. Die Bilder sind im Standardformat DICOM gespeichert und lassen sich mit jedem DICOM-Viewer öffnen, auch im Browser."),
   ("Die Dateien haben keine Endung – ist das normal?", "Ja. Auf Radiologie-CDs heißen Bilder oft IM000001 oder ähnlich. Der Viewer erkennt sie an der internen Kennung DICM."),
   ("Mein Laptop hat kein CD-Laufwerk. Was tun?", "Ein externes USB-Laufwerk nutzen oder den Inhalt an einem anderen Rechner auf einen USB-Stick kopieren und diesen Ordner laden."),
   ("Warum wird nichts angezeigt, wenn ich DICOMDIR öffne?", "Das DICOMDIR ist nur ein Inhaltsverzeichnis ohne Bilder. Wählen Sie den ganzen Ordner der CD.")])))

PAGES.append(("dicom-in-jpg/", page("dicom-in-jpg/", "DICOM in JPG oder PNG umwandeln – anonym und kostenlos",
  "DICOM-Bild in JPG oder PNG umwandeln, ohne Patientendaten: kostenlos im Browser, ohne Upload. So anonymisieren Sie Röntgen- und MRT-Bilder vor dem Weitergeben.",
  "DICOM in JPG umwandeln – und dabei anonymisieren",
  "Sie möchten ein Röntgen- oder MRT-Bild per Messenger teilen, in eine Präsentation einbauen oder im Forum zeigen? So wird aus der DICOM-Datei ein normales Bild – ohne Ihren Namen darin.",
  '''<h2>In drei Schritten</h2>
<ol><li>Datei oder CD-Ordner im <a href="../">DICOM Viewer</a> laden.</li>
<li>Die gewünschte Schicht suchen und mit Fenster/Level Helligkeit und Kontrast einstellen. Exportiert wird genau das, was Sie sehen – in der Originalauflösung des Bildes.</li>
<li>Auf <strong>PNG</strong> oder <strong>JPG</strong> klicken. Fertig.</li></ol>
<h2>PNG oder JPG?</h2>
<p><strong>PNG</strong> ist verlustfrei und die bessere Wahl für feine Strukturen oder wenn das Bild weiterbearbeitet wird. <strong>JPG</strong> ist kleiner und lässt sich problemlos per Messenger oder E-Mail verschicken. Für Fotos von Ultraschall oder Röntgen reicht JPG meist völlig.</p>
<h2>Warum anonymisieren?</h2>
<p>Eine DICOM-Datei trägt Name, Geburtsdatum, Patienten-ID, Einrichtung und überweisende Ärztin in sich. Wer die Originaldatei weitergibt, gibt diese Daten mit. Viele Viewer blenden sie außerdem ins Bild ein, sodass sie auf jedem Screenshot landen.</p>
<p>Unser Export enthält <strong>standardmäßig nur die Pixel</strong>: keine Metadaten, keine eingeblendeten Namen. Nur wenn Sie „Patientendaten anzeigen“ und zusätzlich „Name im Export einbrennen“ aktivieren, wird der Name bewusst ins Bild geschrieben.</p>
<h2>Checkliste vor dem Weitergeben</h2>
<ul><li>Ist Text direkt ins Bild gebrannt? Manche Ultraschall- und ältere Röntgengeräte schreiben Namen oder Datum in die Pixel. Das kann kein Export entfernen – prüfen Sie das Bild und schneiden Sie die Stelle notfalls zu.</li>
<li>Keine Screenshots des Bildschirms mit offener Seitenleiste teilen, dort stehen ggf. Namen.</li>
<li>Für eine ärztliche Zweitmeinung immer die Original-DICOM-Dateien weitergeben, nicht JPGs – nur so bleiben alle Grauwerte und Abstände erhalten.</li></ul>''',
  [("Gehen beim Umwandeln Details verloren?", "Ja, teilweise: DICOM speichert bis zu 65.536 Graustufen, JPG und PNG nur 256. Deshalb wird das aktuelle Fenster/Level angewendet. Für Ärzte immer die Originaldatei weitergeben."),
   ("Sind die Patientendaten wirklich weg?", "Im exportierten Bild stehen keine Metadaten und standardmäßig kein eingeblendeter Text. Text, den das Gerät selbst in die Pixel gebrannt hat, bleibt sichtbar – übermalen Sie ihn vor dem Export mit dem Werkzeug „Schwärzen“."),
   ("Kann ich alle Schichten auf einmal umwandeln?", "Derzeit wird das jeweils angezeigte Bild exportiert. So entscheiden Sie bewusst, welches Bild Sie teilen."),
   ("Wird mein Bild dafür hochgeladen?", "Nein, die Umwandlung passiert vollständig in Ihrem Browser.")])))

PAGES.append(("dicom-viewer-mac/", page("dicom-viewer-mac/", "DICOM Viewer für Mac – kostenlos, ohne Installation",
  "DICOM-Dateien und Radiologie-CDs am Mac öffnen: kostenloser DICOM Viewer im Browser für Safari, Chrome und Firefox. Funktioniert auf Intel und Apple Silicon.",
  "DICOM Viewer für den Mac",
  "Der Viewer auf der Radiologie-CD ist ein Windows-Programm, und Vorschau kann mit .dcm nichts anfangen? Im Browser öffnen Sie DICOM-Bilder am Mac ohne Installation.",
  '''<h2>Warum der Mac DICOM nicht von Haus aus öffnet</h2>
<p>macOS bringt mit Vorschau einen guten Bildbetrachter mit, der aber nur gängige Formate wie JPG, PNG, HEIC oder PDF kennt. DICOM-Dateien enthalten 12- bis 16-Bit-Graustufen und medizinische Zusatzdaten – dafür braucht es einen DICOM-Viewer. Die auf CDs mitgelieferten Programme laufen meist nur unter Windows.</p>
<h2>So geht es am Mac</h2>
<ol><li>CD einlegen (bei Macs ohne Laufwerk: USB-Laufwerk anschließen) – sie erscheint im Finder in der Seitenleiste.</li>
<li><a href="../">DICOM Viewer</a> in Safari, Chrome oder Firefox öffnen.</li>
<li>Das CD-Symbol aus dem Finder direkt auf die Seite ziehen – oder „Ordner / CD wählen“ klicken und die CD auswählen.</li>
<li>Serie links anklicken und mit Trackpad (zwei Finger) oder Mausrad durch die Schichten blättern.</li></ol>
<h2>Bedienung mit Trackpad</h2>
<ul><li><strong>Blättern:</strong> zwei Finger auf- und abwärts</li>
<li><strong>Zoomen:</strong> Modus „Zoom“ wählen und ziehen, oder <kbd>Ctrl</kbd> halten und mit zwei Fingern scrollen</li>
<li><strong>Helligkeit/Kontrast:</strong> mit einem Finger klicken und ziehen (Modus „Fenster“)</li>
<li><strong>Verschieben:</strong> Modus „Verschieben“ wählen</li></ul>
<h2>Datenschutz am Mac</h2>
<p>Safari meldet beim Ordner-Auswählen eventuell „Hochladen“. Das ist die übliche Formulierung des Browsers – der Viewer schickt nichts ins Internet, sondern liest die Dateien nur lokal. Sie können das prüfen, indem Sie nach dem Laden der Seite das WLAN ausschalten: Der Viewer funktioniert weiter.</p>''',
  [("Läuft der Viewer auf Apple-Silicon-Macs (M1–M4)?", "Ja. Er läuft im Browser und ist damit unabhängig vom Prozessor."),
   ("Welcher Browser ist am besten?", "Alle aktuellen Versionen von Safari, Chrome, Edge und Firefox funktionieren. Für sehr große Serien ist Chrome oft etwas schneller."),
   ("Muss ich etwas installieren oder Gatekeeper umgehen?", "Nein. Es wird keine App installiert und keine Sicherheitseinstellung geändert."),
   ("Kann ich Bilder für Keynote oder Pages verwenden?", "Ja, über den Export als PNG oder JPG – standardmäßig ohne Patientendaten.")])))

PAGES.append(("dicom-iphone/", page("dicom-iphone/", "DICOM-Datei am iPhone öffnen – ohne App",
  "DICOM-Datei auf dem iPhone oder iPad öffnen, z. B. aus einer E-Mail oder einem Download-Link der Radiologie: kostenlos im Browser, ohne App und ohne Upload.",
  "DICOM-Datei am iPhone öffnen",
  "Die Radiologie hat Ihnen einen Download-Link oder eine .dcm-Datei per E-Mail geschickt, und das iPhone zeigt nur ein leeres Dokument? So öffnen Sie die Bilder direkt in Safari.",
  '''<h2>Schritt für Schritt am iPhone und iPad</h2>
<ol><li>Datei zuerst sichern: In der Mail lange auf den Anhang tippen → <strong>„In Dateien sichern“</strong>. Bei einem ZIP-Download tippen Sie in der Dateien-App einmal auf das ZIP, dann wird es entpackt.</li>
<li>Den <a href="../">DICOM Viewer</a> in Safari öffnen.</li>
<li>Auf <strong>„Dateien wählen“</strong> tippen → „Durchsuchen“ → die .dcm-Dateien markieren (oben rechts „Auswählen“, dann mehrere antippen).</li>
<li>Die Serie erscheint mit Vorschaubild. Mit dem Schieberegler blättern Sie durch die Schichten.</li></ol>
<h2>Gesten</h2>
<ul><li><strong>Helligkeit/Kontrast:</strong> Modus „Fenster“ und mit einem Finger wischen</li>
<li><strong>Zoom:</strong> Modus „Zoom“ und nach oben/unten wischen</li>
<li><strong>Verschieben:</strong> Modus „Verschieben“</li>
<li><strong>Blättern:</strong> Schieberegler unter dem Bild oder Modus „Blättern“</li></ul>
<h2>Grenzen auf dem Handy</h2>
<p>Ein CT kann aus über tausend Einzelbildern bestehen. iPhones haben im Browser begrenzten Arbeitsspeicher; laden Sie bei sehr großen Untersuchungen lieber nur die interessierende Serie oder nutzen Sie einen Computer. Ganze Ordner kann iOS im Browser nicht auswählen – markieren Sie die Dateien stattdessen einzeln oder gesammelt.</p>
<h2>Bild teilen</h2>
<p>Mit <strong>JPG</strong> speichern Sie das aktuelle Bild in die Dateien-App und können es danach per Messenger verschicken – ohne Namen oder Geburtsdatum. Mehr dazu unter <a href="../dicom-in-jpg/">DICOM in JPG umwandeln</a>.</p>''',
  [("Brauche ich eine App aus dem App Store?", "Nein. Safari genügt. Es wird nichts installiert."),
   ("Funktioniert das auch auf Android?", "Ja, in Chrome auf Android genauso. Dort lassen sich Dateien über den Dateiauswahldialog laden."),
   ("Warum zeigt die Vorschau in Mail nichts an?", "iOS kennt das DICOM-Format nicht und zeigt deshalb nur ein Dateisymbol. Der Inhalt ist trotzdem vollständig vorhanden."),
   ("Werden die Bilder an einen Server geschickt?", "Nein. Safari liest die Dateien lokal auf dem iPhone.")])))

PAGES.append(("mrt-bilder-verstehen/", page("mrt-bilder-verstehen/", "MRT-Bilder verstehen – T1, T2 und welche Serie was zeigt",
  "MRT-Bilder verstehen für Laien: Was bedeuten T1, T2, FLAIR, STIR und DWI? Welche Serie zeigt was, wie liest man Schnittebenen? Verständlich erklärt.",
  "MRT-Bilder verstehen: T1, T2 und Co.",
  "Auf Ihrer CD liegen zehn Serien mit kryptischen Namen wie „t2_tse_sag“ oder „t1_vibe_fs_tra_KM“? Hier steht, was diese Abkürzungen bedeuten – als Orientierung, nicht als Befund.",
  '''<div class="card"><strong>Wichtig:</strong> Diese Seite erklärt Begriffe, sie ersetzt keinen Befund. Ob etwas auffällig ist, kann nur die Radiologin oder der Radiologe beurteilen, der alle Serien gemeinsam und mit Ihrer Vorgeschichte betrachtet.</div>
<h2>Die Seriennamen entschlüsseln</h2>
<p>Ein Serienname setzt sich meist aus Wichtung, Sequenztyp, Zusätzen und Schnittebene zusammen. Beispiel <code>t2_tse_fs_sag</code>: T2-gewichtet, Turbo-Spin-Echo, mit Fettsättigung, sagittale Ebene.</p>
<table><thead><tr><th>Kürzel</th><th>Bedeutung</th><th>Woran man es erkennt</th></tr></thead><tbody>
<tr><td>T1</td><td>T1-Wichtung, gute Darstellung der Anatomie</td><td>Fett hell, Wasser (z. B. Liquor) dunkel</td></tr>
<tr><td>T2</td><td>T2-Wichtung, zeigt Flüssigkeit und Wassereinlagerungen</td><td>Wasser und Liquor hell, Fett mittelhell</td></tr>
<tr><td>PD</td><td>Protonendichte, oft bei Gelenken</td><td>Kontrast zwischen T1 und T2, Knorpel gut sichtbar</td></tr>
<tr><td>FLAIR</td><td>T2 mit unterdrücktem Wassersignal, v. a. Kopf</td><td>Liquor dunkel, Gewebe ähnlich T2</td></tr>
<tr><td>STIR / fs / FatSat / SPAIR</td><td>Fettunterdrückung</td><td>Fett dunkel, Flüssigkeit hebt sich stark ab</td></tr>
<tr><td>DWI / ADC</td><td>Diffusion, misst Wasserbeweglichkeit</td><td>Körniges, kontrastarmes Bild; ADC ist die berechnete Karte dazu</td></tr>
<tr><td>KM / +C / post / Gd</td><td>Nach Kontrastmittel</td><td>Meist T1; Gefäße und gut durchblutetes Gewebe hell</td></tr>
<tr><td>localizer / scout / survey</td><td>Übersichtsbilder zur Planung</td><td>Wenige grobe Bilder in drei Ebenen</td></tr>
</tbody></table>
<h2>Die drei Schnittebenen</h2>
<ul><li><strong>sag (sagittal):</strong> Schnitt von der Seite, wie ein Profil.</li>
<li><strong>cor (coronal/koronar):</strong> Schnitt von vorn, als ob man Ihnen gegenübersteht.</li>
<li><strong>tra / ax (transversal/axial):</strong> Schnitt quer, betrachtet von den Füßen her. Ihre linke Körperseite liegt daher auf dem Bild rechts.</li></ul>
<h2>Hell und dunkel</h2>
<p>Im MRT sagt Helligkeit nichts über „gut“ oder „schlecht“ aus, sondern nur über die Signalstärke in der jeweiligen Wichtung. Dasselbe Gewebe kann in T1 dunkel und in T2 hell sein. Deshalb werden immer mehrere Serien verglichen. Im CT ist das anders: Dort entspricht die Helligkeit der Dichte (Knochen hell, Luft schwarz), gemessen in Hounsfield-Einheiten.</p>
<h2>Selbst ansehen</h2>
<p>Laden Sie Ihre CD in den <a href="../">DICOM Viewer</a>. In der Tag-Ansicht sehen Sie zu jeder Serie die Beschreibung (0008,103E), Echozeit (TE) und Repetitionszeit (TR). Faustregel: kurze TR und TE ≈ T1, lange TR und TE ≈ T2. Wie Sie die CD öffnen, steht unter <a href="../radiologie-cd-oeffnen/">Radiologie-CD öffnen</a>.</p>
<h2>Was ist DICOM überhaupt?</h2>
<p>DICOM ist das Dateiformat, in dem MRT, CT, Röntgen und Ultraschall gespeichert werden. Jede Datei enthält ein Bild (oder einen kurzen Film) plus Angaben zu Patient, Gerät und Aufnahmeparametern. Eine MRT-Untersuchung besteht meist aus mehreren Serien zu je 20 bis 200 Schichten.</p>''',
  [("Was ist der Unterschied zwischen T1 und T2?", "In T1 erscheint Fett hell und Flüssigkeit dunkel, in T2 ist Flüssigkeit hell. T1 zeigt gut die Anatomie, T2 eher Wassereinlagerungen und Entzündungen."),
   ("Warum gibt es so viele Serien?", "Jede Serie betont andere Gewebeeigenschaften oder zeigt eine andere Schnittebene. Erst zusammen ergeben sie ein vollständiges Bild."),
   ("Kann ich anhand der Bilder selbst etwas erkennen?", "Laien können Anatomie erkennen, aber Befunde zuverlässig zu beurteilen erfordert Fachwissen. Der Viewer ist kein Medizinprodukt und nur zur Ansicht gedacht."),
   ("Was bedeutet KM im Seriennamen?", "KM steht für Kontrastmittel. Diese Serie wurde nach der Gabe von Kontrastmittel aufgenommen, meist in T1-Wichtung.")])))

exec(open('articles.py', encoding='utf-8').read())

for path, content in PAGES:
    os.makedirs(path or ".", exist_ok=True)
    open(os.path.join(path, "index.html") if path else "index.html", "w").write(content)

open("404.html", "w").write(page("404/", "Seite nicht gefunden – DICOM Viewer", "Diese Seite gibt es nicht.", "Seite nicht gefunden",
  "Die angeforderte Seite existiert nicht. Zum Viewer geht es hier entlang.", "", []).replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">').replace(f'<link rel="canonical" href="{BASE}404/">', ""))

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, _ in PAGES:
    sm.append(f"  <url><loc>{BASE}{path}</loc><lastmod>{LASTMOD}</lastmod><priority>{'1.0' if not path else '0.8'}</priority></url>")
sm.append("</urlset>")
open("sitemap.xml", "w").write("\n".join(sm) + "\n")

open("llms.txt", "w").write(f"""# DICOM Viewer

> Kostenloser DICOM Viewer im Browser (deutsch). Öffnet Röntgen-, CT-, MRT- und Ultraschallbilder sowie komplette Radiologie-CDs (inkl. DICOMDIR) ohne Installation und ohne Upload. Anonymer Export als PNG/JPG. {MDR} Keine Mess- oder Befundfunktionen.

Unterstützte Transfer-Syntaxen: Implicit/Explicit VR Little Endian, Explicit VR Big Endian, JPEG Baseline (.50), JPEG Extended (.51), JPEG Lossless (.57, .70), JPEG-LS (.80, .81), JPEG 2000 (.90, .91), RLE Lossless (.5). Decoder werden bei Bedarf lokal nachgeladen. Nicht unterstützt (mit Hinweis): Deflate, HTJ2K, Video.

## Seiten
- [DICOM Viewer kostenlos online]({BASE}): das Tool selbst
- [Radiologie-CD öffnen]({BASE}radiologie-cd-oeffnen/): CD am PC/Mac öffnen, DICOMDIR erklärt
- [DICOM in JPG umwandeln]({BASE}dicom-in-jpg/): anonymer Export vor dem Weitergeben
- [DICOM Viewer für Mac]({BASE}dicom-viewer-mac/)
- [DICOM am iPhone öffnen]({BASE}dicom-iphone/)
- [MRT-Bilder verstehen]({BASE}mrt-bilder-verstehen/): T1, T2, FLAIR, Schnittebenen für Laien
- [LDT, BDT und GDT öffnen]({BASE}ldt-bdt-gdt-dateien-oeffnen/)
- [Laborbefunde (LDT) verstehen]({BASE}laborbefund-ldt-verstehen/)
- [Medizinische Datenformate: DICOM, LDT, BDT, GDT]({BASE}medizinische-datenformate/)
- [Datenschutz]({BASE}datenschutz/)

## Verwandte Tools
- [GDT Viewer](https://freimoser.github.io/gdt-viewer/)
- [LDT & BDT Viewer](https://freimoser.github.io/ldt-bdt-viewer/)
- [E-Rechnung Klartext](https://freimoser.github.io/e-rechnung-klartext/)
- [Portfolio Thomas Freimoser](https://freimoser.de/)
- [LinkedIn Thomas Freimoser]({LINKEDIN})
""")
print("ok", len(PAGES), "Seiten")
