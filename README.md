# Medicatie PDF naar Excel Converter

Deze applicatie is een Streamlit webapp waarmee gebruikers medicatie-overzichten uit PDF-bestanden kunnen uploaden en automatisch laten omzetten naar Excel-bestanden. De app is ontwikkeld voor gebruik door zorgprofessionals, zoals verpleegkundigen, om handmatig overtypen te voorkomen en tijd te besparen.

---

## Hoe werkt de code?

- **Upload**: De gebruiker uploadt één of meerdere PDF-bestanden via de webinterface.
- **Parsing**: Voor elk PDF-bestand wordt de tekst uitgelezen met PyMuPDF (`fitz`).
- **Extractie**: De code zoekt per regel naar patronen voor patiëntnaam, kamer, medicatie, tijdstip, dosis, etc. (zie `parse_medication_pdf` in `app.py`).
- **Resultaat**: Voor elk PDF-bestand wordt een tabel getoond en kan een Excel-bestand worden gedownload met de gevonden medicatiegegevens.
- **Debug**: In een uitklapbaar menu wordt debug-informatie getoond over de parsing.

---

## Hoe wordt data behandeld?

- **Geüploade bestanden**: PDF-bestanden worden alleen tijdelijk in het geheugen verwerkt. Ze worden niet opgeslagen op de server of in een database.
- **Resultaten**: De geconverteerde data wordt direct als Excel-bestand aangeboden aan de gebruiker via een downloadknop. Er wordt niets permanent opgeslagen.
- **Privacy**: Na het verwerken van een bestand wordt het direct uit het geheugen verwijderd. Er blijft geen data achter op de server.
- **Geen logging van inhoud**: De app logt geen patiëntgegevens of medicatie-informatie. Alleen foutmeldingen of debug-informatie (voor de gebruiker zichtbaar) worden getoond.

---

## Hoe werkt Streamlit Cloud met data?

- **Tijdelijke verwerking**: Streamlit Cloud draait de app in een tijdelijke container. Geüploade bestanden en resultaten bestaan alleen zolang de gebruiker de app gebruikt.
- **Geen opslag**: Streamlit Cloud slaat geen geüploade bestanden of resultaten op. Alles wordt in het RAM van de server verwerkt en verdwijnt zodra de sessie eindigt.
- **Beveiliging**: De app is alleen toegankelijk via de unieke link. Iedereen met de link kan de app gebruiken, tenzij je zelf authenticatie toevoegt.
- **AVG/GDPR**: Omdat er geen data wordt opgeslagen, is het risico op datalekken minimaal. Toch is het verstandig geen zeer privacygevoelige data te verwerken zonder extra beveiliging.

---

## Belangrijkste gebruikte technologieën
- [Streamlit](https://streamlit.io/) (webinterface)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) (PDF parsing)
- [pandas](https://pandas.pydata.org/) (dataverwerking)
- [openpyxl](https://openpyxl.readthedocs.io/) (Excel export)

---

## Veelgestelde vragen

**Worden mijn geüploade PDF’s opgeslagen?**  
Nee, alle bestanden worden alleen tijdelijk in het geheugen verwerkt en niet opgeslagen.

**Kan iemand anders mijn data zien?**  
Nee, alleen jij ziet je eigen upload/resultaat. Zodra je de pagina sluit, is alles weg.

**Is de app veilig voor patiëntgegevens?**  
De app slaat geen data op, maar voor zeer gevoelige data is het verstandig een extra beveiligde (interne) versie te gebruiken.

**Kan ik meerdere PDF’s tegelijk uploaden?**  
Ja, elke PDF levert een eigen Excel-bestand op.

---

## Gebruik
1. Ga naar de Streamlit Cloud link van de app.
2. Upload één of meerdere PDF-bestanden.
3. Download per PDF het bijbehorende Excel-bestand.

---

Voor vragen of feedback: neem contact op met de ontwikkelaar.
