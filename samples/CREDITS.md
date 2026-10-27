# Beispieldateien: Quellen und Lizenzen

Diese Dateien liegen nur zum Ausprobieren des Viewers im Repository. Sie enthalten keine echten Patientendaten und sind **nicht für klinische Zwecke** gedacht.

| Datei | Inhalt | Quelle | Lizenz |
|---|---|---|---|
| `TS-CT-ELE.dcm` | Thorax-CT, eine Schicht (synthetisch) | [CharruaSoft DICOM Samples](https://www.charruasoft.com/dicom-samples/) | CC0 1.0 |
| `MR-01_T1_s1_10.dcm` | MRT Kopf-Phantom, T1, Schicht 10 (synthetisch) | CharruaSoft | CC0 1.0 |
| `MR-01_T2_s2_10.dcm` | MRT Kopf-Phantom, T2, Schicht 10 (synthetisch) | CharruaSoft | CC0 1.0 |
| `DX-01.dcm` | Röntgen Thorax p.-a. (synthetisch) | CharruaSoft | CC0 1.0 |
| `katze-femur-ct_zenodo-3829502.dcm` | CT-Ausschnitt eines Katzen-Oberschenkelknochens, 75 Schichten | Zenodo, [DOI 10.5281/zenodo.3829502](https://doi.org/10.5281/zenodo.3829502) | CC BY 4.0 |

## CharruaSoft (CC0 1.0)

Die vier synthetischen Dateien stammen unverändert von <https://www.charruasoft.com/dicom-samples/>. CharruaSoft stellt sie unter CC0 1.0 (Public Domain Dedication) bereit, eine Namensnennung ist nicht erforderlich, aber erwünscht. Der Lizenztext des Anbieters liegt als [`LICENSE-CC0.txt`](LICENSE-CC0.txt) bei. Er nennt auch eine Ausnahme für eine EKG-Datei (CC BY 4.0), die hier **nicht** enthalten ist.

## Katzen-Femur-CT (CC BY 4.0)

- Urheberin: **Jana Cavojska**
- Datensatz: „Supplementary data for article ‚Estimating and abstracting the 3D structure of feline bones using neural networks on X-ray (2D) images‘“, Zenodo, Version 1.0, 2020, <https://doi.org/10.5281/zenodo.3829502>
- Lizenz: [Creative Commons Namensnennung 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- Verwendet: eine Datei aus `DICOM_DATA.zip` (`5_sample_bones/AP/4.dcm`), **unverändert übernommen** und nur umbenannt. Die Datei ist laut ihren DICOM-Angaben mit MeVisLab aus einem CT-Volumen abgeleitet.

## Ohne Gewähr

Die Dateien werden ohne Gewährleistung bereitgestellt.
