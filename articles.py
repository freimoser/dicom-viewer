# Zusatzartikel (wird von build.py per exec eingebunden)
LDT_V = "https://freimoser.github.io/ldt-bdt-viewer/"
GDT_V = "https://freimoser.github.io/gdt-viewer/"
CTA = f'<div class="xlink"><p><strong>Direkt ausprobieren:</strong> Dateien lokal im Browser öffnen, ohne Upload und ohne Installation.</p><div class="btns"><a class="btn pri" href="{LDT_V}">LDT &amp; BDT Viewer öffnen →</a><a class="btn pri" href="{GDT_V}">GDT Viewer öffnen →</a></div></div>'
def art_ld(h1, desc, url):
    return {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "inLanguage": "de-DE",
            "dateModified": LASTMOD, "mainEntityOfPage": url, "author": {"@type": "Person", "name": "Thomas Freimoser", "url": "https://freimoser.de/", "sameAs": [LINKEDIN]}}

# 1 ----------------------------------------------------------------
t1 = "LDT, BDT und GDT Dateien öffnen"
d1 = "LDT-, BDT- und GDT-Dateien öffnen und lesen: Was die xDT-Formate sind, wie sie aufgebaut sind, typische Fehler und wie Sie sie kostenlos im Browser ansehen."
PAGES.append(("ldt-bdt-gdt-dateien-oeffnen/", page("ldt-bdt-gdt-dateien-oeffnen/", "LDT, BDT und GDT Dateien öffnen – kostenlos im Browser",
  d1, t1,
  "Eine Datei mit der Endung .ldt, .bdt oder .gdt lässt sich per Doppelklick nicht sinnvoll öffnen? Hier steht, was in diesen Praxis-Dateien steckt, wie man sie liest und welche Werkzeuge helfen.",
  CTA + f'''<h2>Die xDT-Familie in einem Satz</h2>
<p>LDT, BDT und GDT gehören zur sogenannten <strong>xDT-Familie</strong>: Datenaustauschformate, die von der Kassenärztlichen Bundesvereinigung (KBV) bzw. – im Fall von GDT – vom Qualitätsring Medizinische Software (QMS) beschrieben werden. Sie stammen aus einer Zeit, in der Daten zwischen Programmen per Diskette oder Dateiordner ausgetauscht wurden, und sind bis heute in vielen Arztpraxen im Einsatz. Das „x“ steht dabei als Platzhalter: <strong>L</strong>DT für Labor, <strong>B</strong>DT für Behandlungsdaten, <strong>G</strong>DT für Geräte.</p>
<h2>Welche Datei ist wofür?</h2>
<table><thead><tr><th>Format</th><th>Langname</th><th>Typischer Einsatz</th></tr></thead><tbody>
<tr><td>LDT</td><td>Labordatenträger</td><td>Laboraufträge und Laborbefunde zwischen Praxis und Labor</td></tr>
<tr><td>BDT</td><td>Behandlungsdatenträger</td><td>Export von Patienten- und Behandlungsdaten, etwa beim Wechsel der Praxissoftware</td></tr>
<tr><td>GDT</td><td>Gerätedatenträger</td><td>Kopplung von Medizingeräten (EKG, Spirometrie, Ultraschall, Augenmessgeräte …) an die Praxissoftware</td></tr>
</tbody></table>
<h2>So ist eine xDT-Datei aufgebaut</h2>
<p>Alle drei Formate teilen dasselbe Grundprinzip: Es sind reine Textdateien, die Zeile für Zeile gelesen werden. Jede Zeile hat einen festen Aufbau:</p>
<ul><li><strong>3 Ziffern Zeilenlänge</strong> – die Länge der gesamten Zeile in Bytes, einschließlich der Zeilenendezeichen,</li>
<li><strong>4 Ziffern Feldkennung</strong> – eine Nummer, die festlegt, was in der Zeile steht,</li>
<li><strong>der Inhalt</strong> – etwa ein Name, ein Datum oder ein Messwert,</li>
<li>und am Ende <strong>Wagenrücklauf und Zeilenvorschub</strong> (CR LF).</li></ul>
<p>Eine Zeile wie <code>0193101Mustermann</code> bedeutet also: 19 Bytes lang, Feld 3101 (Nachname), Inhalt „Mustermann“. Die Rechnung: 3 + 4 + 10 Zeichen + 2 Zeilenendezeichen = 19. Stimmt die Längenangabe nicht, ist die Zeile streng genommen fehlerhaft. Genau solche Abweichungen sind eine häufige Ursache, wenn ein Import in der Praxissoftware scheitert.</p>
<p>Mehrere Zeilen bilden einen <strong>Satz</strong>. Welche Art Satz vorliegt, steht im Feld <code>8000</code> (Satzart). Bei GDT zeigt zum Beispiel die Satzart 6302 an, dass die Praxissoftware eine neue Untersuchung anfordert, und 6310, dass ein Gerät Untersuchungsdaten zurückschickt.</p>
<h2>Warum normale Programme scheitern</h2>
<p>Technisch könnte man eine xDT-Datei im Editor öffnen. Praktisch hilft das wenig:</p>
<ul><li><strong>Kryptische Nummern:</strong> Statt „Geburtsdatum“ steht dort <code>3103</code>. Ohne Feldkatalog versteht man den Inhalt nicht.</li>
<li><strong>Zeichensatz:</strong> Ältere Dateien sind oft im DOS-Zeichensatz (Codepage 437) oder in ISO 8859-1 gespeichert. Umlaute erscheinen im Windows-Editor dann als Sonderzeichen. Welcher Zeichensatz gilt, steht meist im Feld <code>9206</code>.</li>
<li><strong>Endungen variieren:</strong> Viele Systeme verwenden statt .ldt oder .gdt eigene Endungen oder nummerierte Dateien. Der Inhalt ist trotzdem xDT.</li>
<li><strong>Große Dateien:</strong> Ein BDT-Export einer ganzen Praxis kann sehr umfangreich sein. Ein Editor zeigt dann tausende Zeilen ohne Struktur.</li></ul>
<h2>Schritt für Schritt: Datei im Browser ansehen</h2>
<ol><li>Für <strong>LDT oder BDT</strong> den <a href="{LDT_V}">LDT &amp; BDT Viewer</a> öffnen, für <strong>GDT</strong> den <a href="{GDT_V}">GDT Viewer</a>.</li>
<li>Die Datei per Drag &amp; Drop auf die Seite ziehen oder über den Dateidialog wählen.</li>
<li>Der Viewer übersetzt die Feldkennungen in Klartext, gruppiert die Sätze und zeigt Auffälligkeiten wie falsche Zeilenlängen an.</li>
<li>Bei Bedarf Patientendaten ausblenden, bevor Sie einen Screenshot an den Software-Support schicken.</li></ol>
<p>Die Dateien werden dabei ausschließlich in Ihrem Browser gelesen. Das ist bei Gesundheitsdaten kein Nebendetail: Laborbefunde und Behandlungsdaten gehören zu den besonders geschützten Kategorien personenbezogener Daten nach Art. 9 DSGVO. Ein Online-Konverter, der die Datei auf einen fremden Server lädt, ist für den Praxisalltag deshalb meist keine gute Idee.</p>
<h2>Typische Situationen aus der Praxis</h2>
<h3>Der Laborimport bricht ab</h3>
<p>Die Praxissoftware meldet beim Einlesen eines Laborbefunds einen Fehler. Im Viewer sieht man oft sofort, woran es liegt: eine Zeile mit falscher Längenangabe, ein unerwarteter Zeichensatz oder ein fehlendes Pflichtfeld. Mit dieser Information kann der Support des Labors oder des Softwareherstellers deutlich schneller helfen.</p>
<h3>Praxisübernahme oder Softwarewechsel</h3>
<p>Beim Wechsel der Praxissoftware wird häufig ein BDT-Export erzeugt. Vor dem Import lohnt ein Blick hinein: Sind alle Patienten enthalten? Sind die Umlaute korrekt? Fehlen Diagnosen oder Leistungsziffern? Eine Stichprobe im Viewer erspart böse Überraschungen nach der Umstellung.</p>
<h3>Ein Gerät überträgt nichts</h3>
<p>Wenn EKG oder Lungenfunktion keine Ergebnisse an die Praxissoftware zurückliefern, liegt das häufig an der GDT-Konfiguration: falsches Austauschverzeichnis, abweichende Dateinamen oder Kürzel für Sender und Empfänger. Im <a href="{GDT_V}">GDT Viewer</a> erkennt man, ob die Anforderung (6302) überhaupt beim Gerät ankommt und was das Gerät zurückschreibt.</p>
<h2>Und DICOM?</h2>
<p>Bilder aus Röntgen, CT, MRT oder Ultraschall werden nicht als xDT, sondern als <strong>DICOM</strong> gespeichert. Dafür ist der <a href="{P}">DICOM Viewer</a> auf dieser Seite gedacht. Wie die Formate zusammenspielen, erklärt der Artikel <a href="{P}medizinische-datenformate/">Medizinische Datenformate in der Praxis</a>.</p>
<div class="mdr" role="note">⚠️ Die verlinkten Viewer dienen der Ansicht und Fehlersuche. {MDR}</div>''',
  [("Kann ich eine LDT-Datei in Excel öffnen?", "Nicht sinnvoll. Excel erkennt den Zeilenaufbau aus Länge, Feldkennung und Inhalt nicht. Ein spezieller Viewer übersetzt die Feldnummern in Klartext."),
   ("Werden meine Dateien hochgeladen?", "Nein. LDT & BDT Viewer und GDT Viewer lesen die Dateien lokal im Browser."),
   ("Warum sind die Umlaute kaputt?", "Die Datei ist vermutlich im DOS-Zeichensatz (Codepage 437) oder in ISO 8859-1 gespeichert. Ein xDT-Viewer berücksichtigt das automatisch bzw. anhand von Feld 9206."),
   ("Was ist der Unterschied zwischen BDT und GDT?", "BDT dient dem Austausch kompletter Behandlungsdaten zwischen Praxisprogrammen, GDT der Kommunikation zwischen Praxisprogramm und einzelnen Medizingeräten.")],
  art_ld(t1, d1, BASE + "ldt-bdt-gdt-dateien-oeffnen/"))))

# 2 ----------------------------------------------------------------
t2 = "Medizinische Datenformate in der Praxis: DICOM, LDT, BDT, GDT"
d2 = "DICOM, LDT, BDT und GDT verständlich erklärt: Wofür jedes Format da ist, wie die Daten durch die Praxis fließen, wo Fehler entstehen und welche Viewer helfen."
PAGES.append(("medizinische-datenformate/", page("medizinische-datenformate/", "Medizinische Datenformate: DICOM, LDT, BDT, GDT erklärt",
  d2, t2,
  "In einer Arztpraxis laufen täglich Daten zwischen Praxissoftware, Labor, Geräten und Radiologie hin und her. Vier Formate tauchen dabei immer wieder auf. Ein Überblick für Praxisteams, IT-Betreuer und Neugierige.",
  CTA + f'''<h2>Der Überblick</h2>
<table><thead><tr><th>Format</th><th>Wofür</th><th>Art der Datei</th><th>Passender Viewer</th></tr></thead><tbody>
<tr><td><strong>DICOM</strong></td><td>Medizinische Bilder: Röntgen, CT, MRT, Ultraschall</td><td>Binärdatei mit Bild und Metadaten</td><td><a href="{P}">DICOM Viewer</a></td></tr>
<tr><td><strong>LDT</strong></td><td>Laboraufträge und -befunde</td><td>Textdatei im xDT-Zeilenformat</td><td><a href="{LDT_V}">LDT &amp; BDT Viewer</a></td></tr>
<tr><td><strong>BDT</strong></td><td>Behandlungsdaten, Praxisdaten-Export</td><td>Textdatei im xDT-Zeilenformat</td><td><a href="{LDT_V}">LDT &amp; BDT Viewer</a></td></tr>
<tr><td><strong>GDT</strong></td><td>Anbindung von Medizingeräten</td><td>Textdatei im xDT-Zeilenformat</td><td><a href="{GDT_V}">GDT Viewer</a></td></tr>
</tbody></table>
<h2>DICOM – der internationale Bildstandard</h2>
<p>DICOM (Digital Imaging and Communications in Medicine) ist ein weltweiter Standard, der nicht nur ein Dateiformat, sondern auch ein Netzwerkprotokoll beschreibt. Modalitäten wie CT oder MRT schicken ihre Bilder per DICOM an ein Bildarchiv (PACS); Patientinnen und Patienten erhalten sie häufig auf CD oder per Download-Link. Eine DICOM-Datei enthält neben den Pixeldaten eine lange Liste von Angaben, die über Tag-Nummern wie <code>(0010,0010)</code> für den Patientennamen adressiert werden. Mehr dazu: <a href="{P}radiologie-cd-oeffnen/">Radiologie-CD öffnen</a> und <a href="{P}mrt-bilder-verstehen/">MRT-Bilder verstehen</a>.</p>
<h2>xDT – die deutschen Praxisformate</h2>
<p>LDT, BDT und GDT sind deutsche Formate aus der xDT-Familie. Sie sind deutlich einfacher als DICOM: reine Textdateien, in denen jede Zeile aus Längenangabe, vierstelliger Feldkennung und Inhalt besteht. Diese Einfachheit ist ihr großer Vorteil – fast jede Praxissoftware kann sie schreiben und lesen, und man kann sie notfalls mit einem Texteditor untersuchen. Der Nachteil: Ohne Feldkatalog sind sie für Menschen kaum lesbar, und kleine Abweichungen von der Spezifikation führen schnell zu Importfehlern.</p>
<h3>LDT: Labor ↔ Praxis</h3>
<p>Die Praxis schickt einen Auftrag ans Labor, das Labor liefert den Befund als LDT-Datei zurück – meist automatisiert über eine Laborsoftware oder einen sicheren Übertragungsweg. In der Praxissoftware landen die Werte dann in der Patientenakte, inklusive Einheit, Referenzbereich und Kennzeichnung auffälliger Werte. Wie man einen solchen Befund liest, erklärt der Artikel <a href="{P}laborbefund-ldt-verstehen/">Laborbefunde (LDT) verstehen</a>.</p>
<h3>BDT: Praxis ↔ Praxis</h3>
<p>BDT wurde für den Austausch von Behandlungsdaten zwischen Praxisprogrammen entworfen. Heute begegnet man ihm vor allem beim Softwarewechsel, bei Praxisübernahmen oder wenn Daten für Auswertungen exportiert werden. Ein BDT-Export kann Stammdaten, Diagnosen, Leistungen, Befundtexte und vieles mehr enthalten – entsprechend groß und sensibel ist er.</p>
<h3>GDT: Praxis ↔ Gerät</h3>
<p>Über GDT ruft die Praxissoftware ein Gerät oder dessen Software auf und übergibt die Patientendaten, damit am EKG nicht noch einmal Name und Geburtsdatum eingetippt werden müssen. Nach der Untersuchung schreibt das Gerät das Ergebnis – Messwerte, Befundtext oder einen Verweis auf eine PDF – zurück. Der Austausch läuft klassisch über Dateien in einem gemeinsamen Verzeichnis.</p>
<h2>Wie die Daten durch die Praxis fließen</h2>
<ol><li>Eine Patientin kommt zur Vorsorge. Die Praxissoftware legt den Termin an.</li>
<li>Für das Ruhe-EKG wird per <strong>GDT</strong> die Gerätesoftware gestartet, die Patientendaten werden übergeben, das Ergebnis kommt zurück.</li>
<li>Blut wird abgenommen und ans Labor geschickt. Der Befund kommt als <strong>LDT</strong> zurück und wird in die Akte übernommen.</li>
<li>Eine Überweisung zur Radiologie ergibt ein MRT. Die Bilder kommen als <strong>DICOM</strong> – auf CD, per Portal oder direkt ins Bildarchiv.</li>
<li>Jahre später wechselt die Praxis die Software. Die Altdaten werden per <strong>BDT</strong> (oder einem herstellereigenen Weg) übertragen.</li></ol>
<h2>Wo es in der Praxis hakt</h2>
<ul><li><strong>Zeichensätze:</strong> Umlautfehler sind bei xDT der Klassiker, weil ältere Systeme den DOS-Zeichensatz verwenden.</li>
<li><strong>Versionen:</strong> Von LDT gibt es mehrere Versionen (verbreitet sind LDT 2 und LDT 3), die sich im Aufbau unterscheiden. Sender und Empfänger müssen zueinander passen.</li>
<li><strong>Herstellerdialekte:</strong> Manche Programme nutzen eigene Felder oder interpretieren Pflichtfelder großzügig.</li>
<li><strong>Bilder ohne Viewer:</strong> Bei DICOM liegt das Problem oft nicht in der Datei, sondern darin, dass der CD-Viewer auf dem eigenen Rechner nicht startet.</li>
<li><strong>Datenschutz bei der Fehlersuche:</strong> Wer eine fehlerhafte Datei an den Support schickt, verschickt Gesundheitsdaten. Besser: lokal ansehen, Fehler eingrenzen, nur das Nötige weitergeben.</li></ul>
<h2>Und was ist mit HL7 und FHIR?</h2>
<p>Im Krankenhaus ist HL7 seit Langem verbreitet, und mit FHIR gibt es einen modernen, webbasierten Standard, auf dem auch viele Anwendungen der Telematikinfrastruktur aufbauen, etwa die elektronische Patientenakte. Für die niedergelassene Praxis bleiben die xDT-Formate aber vorerst im Alltag präsent – gerade bei Labor- und Geräteanbindungen.</p>
<h2>Die passenden Werkzeuge</h2>
<p>Alle vier Formate lassen sich mit kostenlosen Browser-Tools ansehen, ohne dass Daten Ihr Gerät verlassen: der <a href="{P}">DICOM Viewer</a> für Bilder, der <a href="{LDT_V}">LDT &amp; BDT Viewer</a> für Labor- und Behandlungsdaten und der <a href="{GDT_V}">GDT Viewer</a> für Gerätedaten. Eine Anleitung zum Öffnen finden Sie unter <a href="{P}ldt-bdt-gdt-dateien-oeffnen/">LDT, BDT und GDT Dateien öffnen</a>.</p>
<div class="mdr" role="note">⚠️ {MDR} Die Tools ersetzen weder die Praxissoftware noch die ärztliche Beurteilung.</div>''',
  [("Ist DICOM auch ein xDT-Format?", "Nein. DICOM ist ein internationaler Bildstandard mit binärem Dateiformat und eigenem Netzwerkprotokoll. xDT sind deutsche, textbasierte Austauschformate."),
   ("Welches Format nutzt das Labor?", "In deutschen Arztpraxen kommen Laborbefunde typischerweise als LDT-Datei."),
   ("Kann ich alle Formate mit einem Programm öffnen?", "Dafür gibt es spezialisierte Viewer: den DICOM Viewer für Bilder, den LDT & BDT Viewer und den GDT Viewer. Alle laufen kostenlos im Browser."),
   ("Sind LDT, BDT und GDT veraltet?", "Sie sind alt, aber weiterhin weit verbreitet. Moderne Standards wie FHIR kommen hinzu, ersetzen die xDT-Formate im Praxisalltag aber nicht von heute auf morgen.")],
  art_ld(t2, d2, BASE + "medizinische-datenformate/"))))

# 3 ----------------------------------------------------------------
t3 = "Laborbefunde (LDT) verstehen"
d3 = "Laborbefund als LDT-Datei verstehen: Aufbau, wichtige Felder für Test, Ergebnis, Einheit und Referenzbereich, Kennzeichen auffälliger Werte und typische Stolperfallen."
PAGES.append(("laborbefund-ldt-verstehen/", page("laborbefund-ldt-verstehen/", "Laborbefunde (LDT) verstehen – Felder, Werte, Kennzeichen",
  d3, t3,
  "Was steht eigentlich in einer LDT-Datei aus dem Labor, und wie wird daraus der Befund in der Praxissoftware? Eine Lesehilfe für Praxisteams, IT-Betreuer und alle, die bei einem Importfehler genauer hinschauen müssen.",
  CTA + f'''<div class="card"><strong>Wichtig:</strong> Diese Seite erklärt das Dateiformat, nicht die medizinische Bedeutung einzelner Werte. Ob ein Laborwert behandlungsbedürftig ist, beurteilt die behandelnde Ärztin oder der behandelnde Arzt.</div>
<h2>Vom Röhrchen zur Datei</h2>
<p>Wenn eine Praxis Blut ins Labor schickt, geht in der Regel ein Auftrag mit – elektronisch oder auf einem Anforderungsschein. Das Labor misst, prüft die Ergebnisse und erzeugt einen Befund. Damit die Werte nicht abgetippt werden müssen, wird der Befund als <strong>LDT-Datei</strong> (Labordatenträger) an die Praxis übermittelt. Die Praxissoftware liest die Datei ein und ordnet die Werte dem richtigen Patienten zu.</p>
<h2>Der Grundaufbau</h2>
<p>Eine LDT-Datei ist eine Textdatei im xDT-Format: Jede Zeile beginnt mit drei Ziffern für die Zeilenlänge und vier Ziffern für die Feldkennung, danach folgt der Inhalt. Die Datei ist in Sätze gegliedert. Grob gibt es</p>
<ul><li>einen <strong>Kopfsatz</strong> mit Angaben zum Labor, zum Empfänger und zur Datei (zum Beispiel Erstellungsdatum und Version),</li>
<li>einen oder mehrere <strong>Befundsätze</strong>, je einen pro Auftrag bzw. Patient,</li>
<li>einen <strong>Abschlusssatz</strong>, der die Datei beendet.</li></ul>
<p>In LDT 3 sind die Inhalte zusätzlich in Objekte gegliedert, das Grundprinzip der Zeilen bleibt aber gleich. Welche Version vorliegt, steht im Kopf der Datei – das ist bei Importproblemen die erste Frage, die der Support stellt.</p>
<h2>Die wichtigsten Felder eines Ergebnisses</h2>
<p>Für jeden Test enthält der Befund eine Gruppe von Zeilen. In LDT 2 sind das zum Beispiel:</p>
<table><thead><tr><th>Feld</th><th>Bedeutung</th><th>Beispielinhalt</th></tr></thead><tbody>
<tr><td>8410</td><td>Test-Ident (Kurzbezeichnung)</td><td>HB</td></tr>
<tr><td>8411</td><td>Testbezeichnung</td><td>Hämoglobin</td></tr>
<tr><td>8420</td><td>Ergebniswert</td><td>13,9</td></tr>
<tr><td>8421</td><td>Einheit</td><td>g/dl</td></tr>
<tr><td>8460</td><td>Normalwert als Text</td><td>12,0 – 16,0</td></tr>
<tr><td>8422</td><td>Grenzwertindikator</td><td>z. B. H für erhöht, L für erniedrigt</td></tr>
<tr><td>8480</td><td>Ergebnistext (Freitext)</td><td>Kommentar des Labors</td></tr>
</tbody></table>
<p>Die genauen Feldnummern und Pflichtfelder hängen von der LDT-Version ab und sind im Feldkatalog der KBV beschrieben. Die Beispielwerte oben sind frei gewählt und dienen nur der Veranschaulichung.</p>
<h2>Referenzbereiche richtig lesen</h2>
<p>Ein Laborwert ist für sich allein wenig aussagekräftig. Erst der Referenzbereich zeigt, wo er einzuordnen ist – und dieser Bereich ist nicht universell: Er hängt von der Messmethode des Labors, oft auch von Alter und Geschlecht ab. Deshalb liefert das Labor ihn im Befund mit. Zwei Labore können für denselben Test unterschiedliche Referenzbereiche und sogar unterschiedliche Einheiten angeben (zum Beispiel mg/dl gegenüber mmol/l). Werte aus verschiedenen Laboren sollte man daher nur mit Vorsicht direkt vergleichen.</p>
<h2>Kennzeichen für auffällige Werte</h2>
<p>Damit auffällige Werte in der Praxissoftware hervorgehoben werden, setzt das Labor einen Grenzwertindikator. Üblich sind Buchstaben wie <strong>H</strong> (hoch) und <strong>L</strong> (niedrig), oft auch abgestufte Kennzeichen für stark abweichende Werte. Wichtig: Ein Kennzeichen bedeutet nur, dass der Wert außerhalb des angegebenen Bereichs liegt. Es sagt nichts darüber, ob das medizinisch relevant ist.</p>
<h2>Freitexte, Anhänge und Folgebefunde</h2>
<p>Nicht jedes Ergebnis ist eine Zahl. Mikrobiologische Befunde, Antibiogramme oder Kommentare des Labors stehen häufig als Freitext in der Datei. Außerdem kennt LDT den Unterschied zwischen <strong>Teil- und Endbefunden</strong>: Manche Werte liegen nach Stunden vor, andere erst nach Tagen. Das Labor schickt dann mehrere Dateien zum selben Auftrag. Wer sich wundert, warum ein Befund „doppelt“ auftaucht, findet die Erklärung meist im Befundstatus.</p>
<h2>Typische Stolperfallen beim Import</h2>
<ul><li><strong>Falsche Zeilenlänge:</strong> Wird eine Datei nachträglich bearbeitet oder mit falscher Kodierung gespeichert, stimmen die Längenangaben nicht mehr.</li>
<li><strong>Zeichensatz:</strong> Umlaute in Patientennamen oder Testbezeichnungen werden falsch dargestellt, wenn Sender und Empfänger unterschiedliche Zeichensätze annehmen.</li>
<li><strong>Zuordnung zum Patienten:</strong> Wenn Patientennummer, Name oder Geburtsdatum nicht zu den Daten in der Praxissoftware passen, landet der Befund in einer Warteschlange zur manuellen Zuordnung.</li>
<li><strong>Versionskonflikt:</strong> Eine LDT-3-Datei kann nicht von jeder Software gelesen werden, die nur LDT 2 erwartet – und umgekehrt.</li>
<li><strong>Dezimaltrennzeichen:</strong> Komma oder Punkt – bei der Auswertung außerhalb der Praxissoftware führt das schnell zu falschen Zahlen.</li></ul>
<h2>Selbst nachsehen – ohne Upload</h2>
<p>Im <a href="{LDT_V}">LDT &amp; BDT Viewer</a> laden Sie eine LDT-Datei per Drag &amp; Drop. Der Viewer übersetzt Feldkennungen in Klartext, stellt die Ergebnisse tabellarisch mit Einheit und Referenzbereich dar und weist auf formale Fehler hin. Da die Datei nur lokal gelesen wird, eignet sich das auch für echte Befunde – etwa um vor einem Anruf beim Labor-Support zu sehen, welche Zeile das Problem verursacht. Hintergründe zu den anderen Formaten finden Sie unter <a href="{P}medizinische-datenformate/">DICOM, LDT, BDT und GDT im Vergleich</a>.</p>
<div class="mdr" role="note">⚠️ {MDR} Laborwerte immer ärztlich beurteilen lassen.</div>''',
  [("Was bedeutet das H hinter einem Laborwert?", "H steht üblicherweise für einen Wert oberhalb des vom Labor angegebenen Referenzbereichs, L für einen Wert darunter. Über die medizinische Bedeutung sagt das allein nichts aus."),
   ("Warum unterscheiden sich Referenzbereiche zwischen Laboren?", "Sie hängen von Messmethode, Geräten und Referenzpopulation ab und werden deshalb vom jeweiligen Labor mitgeliefert."),
   ("Kann ich eine LDT-Datei selbst lesen?", "Ja, mit einem LDT-Viewer, der die Feldnummern in Klartext übersetzt. Der LDT & BDT Viewer läuft kostenlos und ohne Upload im Browser."),
   ("Welche LDT-Version habe ich?", "Die Version steht im Kopfsatz der Datei. Der Viewer zeigt sie direkt an.")],
  art_ld(t3, d3, BASE + "laborbefund-ldt-verstehen/"))))

# Datenschutz --------------------------------------------------------
PAGES.append(("datenschutz/", page("datenschutz/", "Datenschutz – DICOM Viewer", "Datenschutzhinweise zum kostenlosen DICOM Viewer: keine Uploads, Hosting über GitHub Pages, optionale Reichweitenmessung nur nach Einwilligung.",
  "Datenschutz", "Kurz gesagt: Ihre medizinischen Dateien verlassen Ihr Gerät nicht. Hier stehen die Details.",
  f'''<h2>Verantwortlicher</h2>
<p>Thomas Freimoser, München / Remote. Kontakt: <a href="mailto:kontakt@freimoser.de">kontakt@freimoser.de</a>. Vollständige Angaben im <a href="https://freimoser.github.io/freimoser.de/impressum/">Impressum</a>.</p>
<h2>Ihre Dateien</h2>
<p>DICOM-Dateien, die Sie in den Viewer laden, werden ausschließlich lokal in Ihrem Browser verarbeitet. Es findet keine Übertragung an einen Server statt; es gibt keinen Server, der solche Daten empfangen könnte.</p>
<h2>Hosting</h2>
<p>Die Seite wird über GitHub Pages (GitHub Inc.) ausgeliefert. Beim Aufruf verarbeitet GitHub technisch notwendige Verbindungsdaten wie IP-Adresse, Zeitpunkt und angeforderte Datei, um die Seite bereitzustellen und abzusichern (Art. 6 Abs. 1 lit. f DSGVO). Details: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement">Datenschutzerklärung von GitHub</a>.</p>
<h2>Analytics (Reichweitenmessung)</h2>
<p>Zur Verbesserung des Angebots kann Google Analytics 4 (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland) eingesetzt werden – <strong>ausschließlich nach Ihrer ausdrücklichen Einwilligung</strong> über das Banner (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG). Vor der Einwilligung wird kein Google-Skript geladen und kein Cookie gesetzt. Nach Einwilligung werden pseudonyme Nutzungsdaten (aufgerufene Seiten, Gerät, Browser, ungefährer Standort auf Basis der gekürzten IP-Adresse) erfasst; Werbefunktionen bleiben deaktiviert. Inhalte Ihrer DICOM-Dateien werden nie erfasst. Eine Übermittlung in die USA ist möglich; Google ist nach dem EU-US Data Privacy Framework zertifiziert.</p>
<p>Ihre Entscheidung wird nur lokal in Ihrem Browser (localStorage) gespeichert. Sie können sie jederzeit widerrufen: <button class="btn" type="button" onclick="if(window.dvConsentReset)dvConsentReset();else alert('Derzeit ist keine Reichweitenmessung aktiv.')">Einwilligung ändern</button></p>
<h2>Google Search Console und Bing Webmaster Tools</h2>
<p>Die Seite enthält Bestätigungs-Meta-Tags für diese Dienste. Dabei werden keine Daten von Besucherinnen und Besuchern übertragen.</p>
<h2>Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren.</p>''',
  [])))
