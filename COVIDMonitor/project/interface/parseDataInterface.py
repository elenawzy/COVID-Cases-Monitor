from abc import ABC, abstractmethod
import pandas as pd


class DataInterface(ABC):

    """
    Attributes:
        original_data: unfiltered dataframe that is created by reading all reuqired csv files
        parsed_data: dataframe that is filtered for export
    """

    def __init__(self):
        self.original_data = pd.DataFrame()
        self.parsed_data = pd.DataFrame()

    # Read all files in the path where the csv datafiles are saved, filter out unecessary columns.
    @abstractmethod
    def readData(self):
        pass

    # Take string and list of strings as parameter, and filter parsed_data.
    @abstractmethod
    def queryData(self):
        pass

    # Refresh parsed_data and undo all filtering.
    def refreshParsedData(self):
        self.parsed_data = self.original_data

    # Transfer parsed_data into json format, display it on the webpage and save the json file in resultfiles folder
    @abstractmethod
    def exportJson(self):
        pass

    # Transfer parsed_data into csv format, display it on the webpage and save the json file in resultfiles folder
    @abstractmethod
    def exportCsv(self):
        pass

    # Transfer parsed_data into html format, display it on the webpage and save the txt(html) file in resultfiles folder
    @abstractmethod
    def exportTxt(self):
        pass
