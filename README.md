# DICOM Viewer

DICOM-Bilder und Radiologie-CDs im Browser ansehen, lokal, ohne Upload. Anonymer PNG/JPG-Export mit Schwärzen-Werkzeug.
**Nur zur Ansicht, nicht zur Diagnose. Kein Medizinprodukt.**

Live: https://freimoser.github.io/dicom-viewer/

Seiten werden mit `python3 build.py` erzeugt. Verwendet dicomParser, codec-openjpeg, codec-charls, jpeg-lossless-decoder-js und den JPEG-Decoder aus cornerstone3D (vendor/). Lizenztexte: THIRD-PARTY-LICENSES.

## Beispieldateien

Unter `samples/` liegen fünf Beispieldateien (zusammen ca. 5,4 MB), die der Viewer auf der Startseite im Abschnitt „Beispieldateien“ per Klick lädt: Thorax-CT, MRT Kopf-Phantom (T1 und T2) und Röntgen Thorax (alle synthetisch, CC0, von [CharruaSoft](https://www.charruasoft.com/dicom-samples/)) sowie ein CT-Ausschnitt eines Katzen-Oberschenkelknochens (CC BY 4.0, Jana Cavojska, [DOI 10.5281/zenodo.3829502](https://doi.org/10.5281/zenodo.3829502)). Die Dateien sind **nicht für klinische Zwecke**. Quellen und Lizenzen im Detail: [`samples/CREDITS.md`](samples/CREDITS.md) und [`samples/LICENSE-CC0.txt`](samples/LICENSE-CC0.txt). Die Beispielkarten und ihre Erklärungstexte stehen in `build.py` (`SAMPLES`).
