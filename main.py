import os
import folium
import webview
from flask import Flask, request, render_template_string, session
from geopy.distance import geodesic

app = Flask(__name__)

# Den Pfad zum Vorlagenverzeichnis festlegen
template_dir = os.path.abspath(os.path.dirname(__file__))
app.template_folder = os.path.join(template_dir, "templates")

# Liste der Bundeslandhauptstädte
bundeslaender = {
    "Baden-Württemberg": "Stuttgart",
    "Bayern": "München",
    "Berlin": "Berlin",
    "Brandenburg": "Potsdam",
    "Bremen": "Bremen",
    "Hamburg": "Hamburg",
    "Hessen": "Wiesbaden",
    "Mecklenburg-Vorpommern": "Schwerin",
    "Niedersachsen": "Hannover",
    "Nordrhein-Westfalen": "Düsseldorf",
    "Rheinland-Pfalz": "Mainz",
    "Saarland": "Saarbrücken",
    "Sachsen": "Dresden",
    "Sachsen-Anhalt": "Magdeburg",
    "Schleswig-Holstein": "Kiel",
    "Thüringen": "Erfurt",
}

stadt_koordinaten = {
    "Stuttgart": (48.775846, 9.182932),
    "München": (48.135125, 11.581981),
    "Berlin": (52.520008, 13.404954),
    "Potsdam": (52.390568, 13.064472),
    "Bremen": (53.079296, 8.801694),
    "Hamburg": (53.551086, 9.993682),
    "Wiesbaden": (50.082729, 8.245584),
    "Schwerin": (53.635502, 11.401249),
    "Hannover": (52.375892, 9.732010),
    "Düsseldorf": (51.227741, 6.773456),
    "Mainz": (50.000000, 8.271000),
    "Saarbrücken": (49.240000, 6.990000),
    "Dresden": (51.050409, 13.737262),
    "Magdeburg": (52.120533, 11.627624),
    "Kiel": (54.322708, 10.135555),
    "Erfurt": (50.978700, 11.032830),
}

def berechne_gesamtstrecke(selected_cities):
    gesamtstrecke = 0.0
    for i in range(len(selected_cities) - 1):
        stadt1 = selected_cities[i]
        stadt2 = selected_cities[i + 1]
        koordinaten1 = stadt_koordinaten[stadt1]
        koordinaten2 = stadt_koordinaten[stadt2]
        distanz = geodesic(koordinaten1, koordinaten2).kilometers
        gesamtstrecke += distanz
    return round(gesamtstrecke)

def berechne_kompakte_route(selected_cities):
    unvisited_cities = set(selected_cities)
    current_city = selected_cities[0]
    tour = [current_city]
    unvisited_cities.remove(current_city)

    while unvisited_cities:
        nearest_city = None
        min_distance = float("inf")

        for city in unvisited_cities:
            distanz = geodesic(
                stadt_koordinaten[current_city], stadt_koordinaten[city]
            ).kilometers
            if distanz < min_distance:
                min_distance = distanz
                nearest_city = city

        tour.append(nearest_city)
        current_city = nearest_city
        unvisited_cities.remove(current_city)

    # Füge die erste Stadt am Ende der Route hinzu
    tour.append(selected_cities[0])

    return tour

def berechne_entfernung(stadt1, stadt2):
    koordinaten1 = stadt_koordinaten[stadt1]
    koordinaten2 = stadt_koordinaten[stadt2]
    distanz = geodesic(koordinaten1, koordinaten2).kilometers
    return round(distanz,2)


def berechne_dauer(stadt1, stadt2):
    entfernung = berechne_entfernung(stadt1, stadt2)
    dauer = entfernung / 100 # Annahme: Durchschnittsgeschwindigkeit von 100 km/h
    return round(dauer,2)

def create_dropdown_options(selected_cities):
    options = ""
    for city in selected_cities:
        options += f'<option value="{city}">{city}</option>'
    return options

@app.route("/", methods=["GET", "POST"])
def index():
    selected_cities = []
    gesamtstrecke = 0.0
    kompakteste_route = []
    gesamtdauer = 0.0

    # Erstelle die Benutzeroberfläche direkt in Python-Code
    form = ""

    if request.method == "POST":
        for stadt in bundeslaender.values():
            if request.form.get(stadt):
                selected_cities.append(stadt)
        #Eingefügt, weil sonst nach dem Drucken die Werte weg sind
        #Das konnte ich auf andere Weise auch mit ChatGPT nicht beheben
        if len(selected_cities) > 1:
            kompakteste_route = berechne_kompakte_route(selected_cities)
            gesamtstrecke = berechne_gesamtstrecke(kompakteste_route)
            gesamtdauer = sum([berechne_dauer(kompakteste_route[i], kompakteste_route[i+1]) for i in range(len(kompakteste_route)-1)])

        if "berechnen" in request.form:
            if len(selected_cities) > 1:
                kompakteste_route = berechne_kompakte_route(selected_cities)
                gesamtstrecke = berechne_gesamtstrecke(kompakteste_route)
                gesamtdauer = sum([berechne_dauer(kompakteste_route[i], kompakteste_route[i+1]) for i in range(len(kompakteste_route)-1)])

        if "reset" in request.form:
            selected_cities = []
            gesamtstrecke = 0.0
            kompakteste_route = []
            gesamtdauer = 0.0

        #Zum Debuggen
        #print("POST request")
        #print("Selected cities:", selected_cities)
        #print("Compact route:", kompakteste_route)

    form = "<h1>Berechnen Sie Ihre Rundreise</h1>"
    form += '<div class="checkbox-container">'

    for stadt in bundeslaender.values():
        checked = "checked" if stadt in selected_cities else ""
        form += f'<label><input type="checkbox" class="checkbox" name="{stadt}" value="{stadt}" {checked} onClick="updateDropdown()">{stadt}</label>'

    form += "</div>"
    form += "<br>"
    form += '<button class="btn" type="submit" name="berechnen">Berechnen</button>'
    form += '<button class="btn" type="submit" name="reset">Zurücksetzen</button>'
    form += '<button class="btn" onclick="window.print()">Drucken</button>'

    # Dropdown-Feld mit den ausgewählten Städten immer anzeigen
    dropdown_options = create_dropdown_options(selected_cities)
    form += f'<select name="selected_city" id="selected_city">{dropdown_options}</select>'
    form += '<button class="btn" type="submit" name="show_on_map">Auf Karte anzeigen</button>'

    # Erstelle das Dropdown-Feld, wenn Städte ausgewählt sind
    if selected_cities:
        dropdown_options = create_dropdown_options(selected_cities)
        form += f'<select name="selected_city">{dropdown_options}</select>'
        form += '<button class="btn" type="submit" name="show_on_map">Auf Karte anzeigen</button>'

     # Erstelle den Inhalt der E-Mail
    subject = "Ausgewählte Städte und kompakte Route"
    body = "Ausgewählte Städte: " + ', '.join(selected_cities) + " - "
    body += "Kompakte Route: " + ' -> '.join(kompakteste_route)

    # Erstelle den mailto-Link
    mailto_link = f'mailto:?subject={subject}&body={body}'
    # Füge den Link zum Formular hinzu
    form += '<a class="btn" href="{}">Per E-Mail senden</a>'.format(mailto_link)

    result = ""
    if selected_cities:
        result += '<div class="result-container">'
        result += '<div class="selected-cities">'
        result += "<h2>Ausgewählte Städte:</h2>"
        result += "<ol>"
        for city in selected_cities:
            result += f"<li>{city}</li>"
        result += "</ol>"
        result += "</div>"

        if len(selected_cities) > 1:
            if kompakteste_route:
                result += '<div class="compact-route">'
                result += "<h2>Kompakte Route:</h2>"
                result += "<ol>"
                for i in range(len(kompakteste_route)):
                    city = kompakteste_route[i]
                    result += f"<li>{city}"
                    if i > 0:
                        dauer = berechne_dauer(kompakteste_route[i - 1], city)
                        stunden = int(dauer)
                        minuten = int((dauer - stunden) * 60)
                        result += f" - Dauer: {stunden:02d}:{minuten:02d} (Std:Min)"
                    result += "</li>"
                result += "</ol>"
                result += "</div>"

        result += "</div>"

        if len(selected_cities) > 1 and kompakteste_route:
            # Erstelle eine Karte mit den ausgewählten Städten und der kompaktesten Route
            karte = folium.Map()

            for city in selected_cities:
                folium.Marker(
                    location=stadt_koordinaten[city],
                    popup=city,
                    icon=folium.Icon(color="blue"),
                ).add_to(karte)

            folium.PolyLine(
                locations=[stadt_koordinaten[city] for city in kompakteste_route],
                color="red",
                weight=2.5,
                opacity=1,
            ).add_to(karte)

            # Passe die Karte an die Grenzen der Route an
            karte.fit_bounds([stadt_koordinaten[city] for city in kompakteste_route])

            # Füge die HTML-Representation der Karte zur Ergebnis-Ausgabe hinzu
            result += '<div class="map-container">'
            result += '<div class="total-distance">'
            result += f'<div class="distance"><h2>Gesamtstrecke: {gesamtstrecke} km</h2></div>'
            stunden = int(gesamtdauer)
            minuten = int((gesamtdauer - stunden) * 60)
            result += f"<h2>Gesamtdauer: {stunden:02d}:{minuten:02d} (Std:Min)</h2>"
            result += "</div>"
            result += '<div class="map">'
            result += karte._repr_html_()
            result += "</div>"
            result += "</div>"

        else:
            result += '<div class="error">'
            result += f"<p>Bitte mindestens 2 Städte auswählen, um eine Strecke zu berechnen.</p>"
            result += "</div>"

    return render_template_string(
        f"""
<html>
<head>
<title>Routenplaner für Außendienstmitarbeiter</title>
<style>
                @media print {{
                    @page {{
                            size: landscape;
                    }}
                    /* Hier können Sie weitere CSS-Regeln hinzufügen, um das Layout der Seite für den Druck im Querformat anzupassen */
                }}
                
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}

                .checkbox-container {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    grid-gap: 5px;
                }}

                .checkbox {{
                    width: 16px;
                    height: 16px;
                    margin: 0;
                    padding: 0;
                }}

                label {{
                    display: flex;
                    align-items: center;
                }}

                h1 {{
                    color: #555555;
                }}

                .btn {{
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }}

                .result-container {{
                    display: flex;
                    grid-template-columns: 1fr 1fr;
                    grid-gap: 10px; 
                }}

                .selected-cities, .compact-route {{
                    padding: 10px;
                }}

                .total-distance, .map-container {{
                    grid-column: span 2;
                    padding: 10px;
                }}

                ol {{
                    padding-left: 20px;
                }}

                li {{
                    flex-basis: 25%;
                    margin-bottom: 10px;
                }}

                .map-container {{
                    grid-row: 2;
                    height: 500px;
                }}

                .error {{
                    flex-basis: 100%;
                    color: red;
                    padding: 10px;
                }}
                
                .total-distance {{
                    display: flex;
                }}

                .distance, .duration {{
                    margin-right: 20px;
                }}
</style>
<script>
    function updateDropdown() {{
        var checkboxes = document.getElementsByClassName('checkbox');
        var selected_cities = [];
        for (var i = 0; i < checkboxes.length; i++) {{
            if (checkboxes[i].checked) {{
                selected_cities.push(checkboxes[i].value);
            }}
        }}

        var dropdown = document.getElementById('selected_city');
        dropdown.innerHTML = '';
        for (var i = 0; i < selected_cities.length; i++) {{
            var option = document.createElement('option');
            option.value = selected_cities[i];
            option.text = selected_cities[i];
            dropdown.add(option);
        }}
    }}
</script>
</head>
<body>
<form method="POST" action="/">
                {form}
</form>
            {result}
</body>
</html>
    """
    )

if __name__ == "__main__":
    window = webview.create_window(
        "Routenplaner für Außendienstmitarbeiter", app, width=1000, height=1000
    )
    webview.start()
