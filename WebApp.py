from spyre import server
import main

dataFrameVoltron = main.DataFrameCreate("D:\Documents\.Projects\DataScience\Laba-2")

class DataVisualisation(server.App):
    title = "Laba 2"

    inputs = [{"type": 'dropdown',
               "label": 'Тип даних',
               "options": [{"label": "VHI", "value": "VHI"},
                           {"label": "VCI", "value": "VCI"},
                           {"label": "TCI", "value": "TCI"}],
               "key": 'type',
               "action_id": "update_data"},

              {"type": 'dropdown',
               "label": 'Область',
               "options": [{"label": "Вінницька", "value": "1"},
                           {"label": "Волиньська", "value": "2"},
                           {"label": "Дніпро", "value": "3"},
                           {"label": "Донецька", "value": "4"},
                           {"label": "Житомирська", "value": "5"},
                           {"label": "Закарпатська", "value": "6"},
                           {"label": "Запорізька", "value": "7"},
                           {"label": "Івано-Франківська", "value": "8"},
                           {"label": "Київська", "value": "9"},
                           {"label": "Кіровоградська", "value": "10"},
                           {"label": "Луганська", "value": "11"},
                           {"label": "Львівська", "value": "12"},
                           {"label": "Миколаївська", "value": "13"},
                           {"label": "Одеська", "value": "14"},
                           {"label": "Полтавська", "value": "15"},
                           {"label": "Рівненська", "value": "16"},
                           {"label": "Сумська", "value": "17"},
                           {"label": "Тернопільска", "value": "18"},
                           {"label": "Харківська", "value": "19"},
                           {"label": "Херсонська", "value": "20"},
                           {"label": "Хмельницька", "value": "21"},
                           {"label": "Черкаська", "value": "22"},
                           {"label": "Чернівецька", "value": "23"},
                           {"label": "Чернігівська", "value": "24"},
                           {"label": "АР Крим", "value": "25"},
                           {"label": "м. Київ", "value": "26"},
                           {"label": "м. Севастополь", "value": "27"}
                           ],
               "key": 'region',
               "action_id": "update_data"},

              {"type": "text",
               "key": "weekInterval",
               "label": "Напиши тижневий інтервал, через дефіс",
               "value": "1-52",
               "action_id": "simple_html_output"},

              {"type": "text",
               "key": "yearInterval",
               "label": "Напиши річний інтервал, через дефіс",
               "value": "1982-2020",
               "action_id": "simple_html_output"}]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True},

               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}]

    def getData(self, params):
        type = params["type"]
        region = int(params["region"])
        weekLimits = params["weekInterval"].split("-")
        yearLimits = params["yearInterval"].split("-")

        firstWeekLim = int(weekLimits[0])
        secondWeekLim = int(weekLimits[1])

        firstYearLim = int(yearLimits[0])
        secondYearLim = int(yearLimits[1])

        return dataFrameVoltron.loc[
            (dataFrameVoltron["Region"] == region) & (dataFrameVoltron["Week"] >= firstWeekLim) & (
                    dataFrameVoltron["Week"] <= secondWeekLim) & (dataFrameVoltron["Year"] >= firstYearLim) & (
                        dataFrameVoltron["Year"] <= secondYearLim), ["Year", "Week", type]]

    def getPlot(self, params):
        dataFrame = self.getData(params).reset_index().drop(["Year", "Week", "index"], axis=1)
        plot = dataFrame.plot()

        if(params["type"] == "VCI"):
            plot.set_ylabel("VCI")
        if (params["type"] == "TCI"):
            plot.set_ylabel("TCI")
        if(params["type"] == "VHI"):
            plot.set_ylabel("VHI")

        plot.set_xlabel("index")
        plot.set_title(params["type"])

        return plot.get_figure()

Application = DataVisualisation()
Application.launch(port=8080)
