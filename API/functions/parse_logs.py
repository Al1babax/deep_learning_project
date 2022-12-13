"""
Parsing log files to get car count per hour/day/week/month, And current car count that has been seen by the system
"""
import pandas as pd
import numpy as np
import json


def read_log_file():
    """
    Read log file and return a dataframe
    :param log_file_path: path to log file
    :return: dataframe
    """
    log_file_path = "C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/count_cars/data/log.txt"
    df = pd.read_csv(log_file_path, sep="|", header=None)
    df.columns = ["datetime", "user", "log_level", "message"]
    df["datetime"] = pd.to_datetime(df["datetime"], format="%d-%b-%y %H:%M:%S")
    return df


def whole_data():
    data = read_log_file()
    final_data = {}
    for i in range(data.shape[0]):
        final_data[i] = {
            "datetime": data["datetime"][i],
            "user": data["user"][i],
            "log_level": data["log_level"][i],
            "message": data["message"][i]
        }
    return final_data


def past_hour_data():
    data = read_log_file()
    data = data[data["datetime"] > pd.to_datetime("now") - pd.Timedelta(hours=1)]
    final_data = {}
    for i in range(data.shape[0]):
        final_data[i] = {
            "datetime": data["datetime"][i],
            "user": data["user"][i],
            "log_level": data["log_level"][i],
            "message": data["message"][i]
        }
    return final_data


def main():
    data = read_log_file()


if __name__ == "__main__":
    main()
