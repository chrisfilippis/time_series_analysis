import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_file(input_file_path, output_file_path):
    
    if(os.path.isfile(output_file_path)):
        return

    input_file = open(input_file_path)
    output_file = open(output_file_path, 'w')
    line = input_file.readline()
    cnt = 0

    while line:
        if line.startswith("<year>"):
            cnt = cnt + 1
            newline = line.replace("<year>","").replace("</year>","").replace('\r\n', '').replace('\n', '')
            if(cnt != 1):
                output_file.write("\n")
            output_file.write("%s" % line.replace("<year>","").replace("</year>","").replace('\r\n', '').replace('\n', ''))
        
        line = input_file.readline()

    input_file.close()

def format_data(intermediate_file_path, last_year=2017):
    year_df = pd.read_csv(intermediate_file_path, names=["year"])
    select2017 = year_df['year'] <= last_year

    all_data_df = year_df.groupby('year')['year'].count().reset_index(name="count")
    filterd_data_df = year_df[select2017].groupby('year')['year'].count().reset_index(name="count")
    filterd_data_df['year'] = filterd_data_df['year'].apply(lambda x: int(x))
    filterd_data_df['count'] = filterd_data_df['count'].apply(lambda x: float(x))
    return all_data_df, filterd_data_df

def double_exponential_smoothing_extended(series, alpha, beta, n_pred):
    result = [series[0]]
    level_result = []
    trend_result = []
    forecasts = []

    for n in range(1, len(series) + (n_pred - 1)):
        if n == 1:
            level, trend = series[0], series[1] - series[0]

        if n >= len(series): # we are forecasting
          value = result[-1]
        else:
          value = series[n]

        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend

        level_result.append(level)
        trend_result.append(trend)
        result.append(level+trend)

    return np.array(result)

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# enter the path of the original text file
input_file = 'C:\Users\cfilip09\Downloads\dblp.xml\dblp.xml'
# enter the path to save the intermediate file
intermediate_file = 'C:\Users\\filippisc\Projects\Master\\time_series_analysis\data\\result.csv'

last_year = 2017
n_predictions = 2
alpha = 0.7
beta = 0.6

parse_file(input_file, intermediate_file)
all_data_df, filterd_data_df = format_data(intermediate_file, last_year)

years = filterd_data_df['year'].as_matrix()
init_series = filterd_data_df['count'].as_matrix()

actual_series = init_series

pred_years = years
for x in range(1, n_predictions):
    pred_years = np.append(pred_years, last_year + x)

result = double_exponential_smoothing_extended(actual_series, alpha, beta, n_predictions)
plt.plot(years, actual_series, color='navy', lw=2, label='prediction')
plt.plot(pred_years, result, color='red', lw=2)
plt.ylabel('number of articles')
plt.xlabel('year')
plt.title('Time series regression')
plt.show()
print mean_absolute_percentage_error(actual_series[0:len(actual_series)], result[0:len(result)-1])
