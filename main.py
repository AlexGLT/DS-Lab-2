import urllib.request
from datetime import datetime
import pandas as pd
import glob

pd.set_option('display.max_rows', 100000)

Indices = {1: 22, 2: 24, 3: 23, 4: 25, 5: "03", 6: "04", 7: "08", 8: 19, 9: 20, 10: 21, 11: "09", 12: 26, 13: 10,
           14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 27, 21: 17, 22: 18, 23: "06", 24: "01", 25: "02",
           26: "07", 27: "05"}
colnames = ["Year", "Week", "VHI"]


def VHIDownload(ID):
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean".format(
        ID)
    vhi_url = urllib.request.urlopen(url)

    out = open(("{}_{}_{}.{}".format("VHI_ID", Indices[ID], datetime.now().strftime("%d-%m-%Y_%H-%M"), "csv")), 'wb')
    out.write(vhi_url.read())
    out.close()


def DataFrameCreate(path):
    Reg = 1
    all_files = glob.glob(path + "\*.csv")
    dataFrames = []

    for filename in all_files:
        dataFrame = pd.read_csv(filename, index_col=False, header=1, delimiter=',', names=colnames, engine='python',
                                usecols=[0, 1, 6], skipfooter=42)
        dataFrame["Region"] = Reg
        Reg += 1
        dataFrames.append(dataFrame)

    dataFrameVoltron = pd.concat(dataFrames, ignore_index=True)

    return dataFrameVoltron


def MinMaxSearch(dataFrame, year, region):
    print(dataFrame.loc[(dataFrame["Year"] == year) & (dataFrame["Region"] == region), ["Year", "Week", "VHI"]])

    min = (dataFrame.loc[(dataFrame["Year"] == year) & (dataFrame["Region"] == region)].VHI).min()
    max = (dataFrame.loc[(dataFrame["Year"] == year) & (dataFrame["Region"] == region)].VHI).max()

    #    min = 100.0
    #    max = 0.0
    #    for week in range(1, 53):
    #        try:
    #            if dataFrame[(dataFrame["Year"] == year) & (dataFrame["Week"] == week) & (dataFrame["Region"] == region)].VHI.item() < min:
    #                min = dataFrame[(dataFrame["Year"] == year) & (dataFrame["Week"] == week) & (dataFrame["Region"] == region)].VHI.item()
    #
    #            if dataFrame[(dataFrame["Year"] == year) & (dataFrame["Week"] == week) & (dataFrame["Region"] == region)].VHI.item() > max:
    #                max = dataFrame[(dataFrame["Year"] == year) & (dataFrame["Week"] == week) & (dataFrame["Region"] == region)].VHI.item()
    #        except ValueError:
    #            continue

    print("The minimum value of VHI for {} = {}".format(region, min))
    print("The maximum value of VHI for {} = {}".format(region, max))


def ExtremeDroughts(dataFrame, year, week):
    values = []



    for year in range(1982, 2021):
        for week in range(1, 53):
            try:
                if dataFrame[(dataFrame["Year"] == year) & (dataFrame["Week"] == week) & (
                        dataFrame["Region"] == region)].VHI.item() > 75:
                    break
            except ValueError:
                continue

    for week in range(6, 10):
        print(dataFrame[dataFrame["Year"] == year & (dataFrame["Week"] == week) & dataFrame["VHI"]])


for i in range(1, 28):
    VHIDownload(i)

DataFrameVoltron = DataFrameCreate("D:\Documents\.Projects\.Python\Laba1")

MinMaxSearch(dataFrameVoltron, 2019, 12)

ExtremeDroughts(dataFrameVoltron, 12)
