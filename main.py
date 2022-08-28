from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_MULTIPLE
import mvg_api
import pandas as pd
import PySimpleGUI as sg
import TextFileHandler as fh

min_depart_time = 2
table_columns_filter = ["product", "label", "destination", "departureTimeMinutes"]
allStations = "allStations.txt"
selectedStations = "selectedStations.txt"
transport_types = ["UBAHN","BUS","TRAM","SBAHN"]

def transportation_types(tTypes:list, df)-> pd.DataFrame:
    return df[df["product"].isin(tTypes)]

def convert_station_name_to_id(station_name):
    return mvg_api.get_id_for_station(station_name)

def get_departures_for_station(station_name):
    return mvg_api.get_departures(convert_station_name_to_id(station_name),timeoffset=min_depart_time)

def create_station_df(station_name)-> pd.DataFrame:
    return pd.DataFrame(get_departures_for_station(station_name))

#create the station data frame with only the including directions list
def create_station_directions_df(station_name, directions: list):
    df = create_station_df(station_name)
    df = df[df["destination"].isin(directions)]
    return df

def only_ubahn(df):
    return transportation_types(["UBAHN"], df)

def only_bus(df):
    return transportation_types("BUS", df)

def convert_transportation_types_indexlist_to_textlist(indexlist):
    textlist = []
    for i in range(len(indexlist)):
        if indexlist[i]:
            textlist.append(transport_types[i])
    return textlist
def sort_df_by_label_destination_minutes(df):
    return df.sort_values(["label","destination", "departureTimeMinutes"], ascending=[False,True, True])

def get_all_stations():
    return fh.read_lines_to_list(allStations)
def get_shown_stations():
    return fh.read_lines_to_list(selectedStations)

def create_radios_list():
    radio_list = []
    all_stations_list = get_all_stations()
    for station in all_stations_list:
        visibility = False
        if fh.containsLine(station, selectedStations
    ):
            visibility = True
        radio_list.append(sg.Radio(station, group_id=0, default=True, key=station, visible=visibility))
    return radio_list
    
tplatz_directions = ["Ostbahnhof U S", "Münchner Freiheit U via Ostbahnhof U S", "Fasangarten Bf. S"]
kpp_directions = ["Hauptbahnhof, Feldmoching"]

layout = [
    create_radios_list(),
    [sg.Checkbox("U-Bahn", default = True), sg.Checkbox("Bus", default = True), sg.Checkbox("Tram"), sg.Checkbox("S-Bahn")],
    [sg.Button("Refresh")],
    [sg.Listbox(values=get_all_stations(), size=(30,6)), sg.Button("Add"), sg.Button("Remove")],
    [sg.Text(key="-OUTPUT-")]]
window = sg.Window("MVG", layout)

while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Refresh":
        num_shown_stations = len(get_shown_stations())
        num_all_stations = len(get_all_stations())
        #checking radio buttons value
        radio_button_range = range(num_all_stations)
        checked_radio_buttons = []
        df_string = ""
        selected_stations = get_shown_stations()
        for station in selected_stations:
            if values[station]:
                df_string = station
                break

        #creating list of indexes of checked boxes
        checkbox_start_index = num_all_stations
        list_checkboxes = list(values)[checkbox_start_index:-1] # from end of stations(radio buttons) up until end (excluding)
        list_index_checked_types = []
        #adding all checked(true) boxes to list
        for n in list_checkboxes:
            list_index_checked_types.append(values[n])

        list_checked_str = convert_transportation_types_indexlist_to_textlist(list_index_checked_types)
        df = create_station_df(df_string)
        #show only checked transportation modes
        df = transportation_types(list_checked_str,df) #shows empty data frame if none checked
        #show only specific columns
        df = df[table_columns_filter]
        #sorting df columns
        df = sort_df_by_label_destination_minutes(df)
        #renaming df columns
        df = df.rename(columns={"product":"Type", "departureTimeMinutes":"Minutes", "label":"Number", "destination":"Destination"})
        #changing text alignment property in data frame
        df.style.set_properties(align="right")

        layout.append(df)
        #updating the window's data frame
        window["-OUTPUT-"].update(df)

    elif event == "Add":
        lastPosition = list(values)[-1]
        listBoxValues = values[lastPosition]
        for station in listBoxValues:
            if not fh.containsLine(station,selectedStations
        ):
                fh.add_text(station,selectedStations
            )
            radioElement = window.find_element(station)
            radioElement.Update(visible=True)
    elif event == "Remove":
        lastPosition = list(values)[-1]
        listBoxValues = values[lastPosition]
        for station in listBoxValues:
            fh.remove_text(station,selectedStations
        )
            radioElement = window.find_element(station)
            radioElement.Update(visible=False)
    elif event == sg.WIN_CLOSED:
        break
window.close()