import os.path
import pandas
import matplotlib.pyplot as plt
from sklearn.svm import SVR

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

parse_file('C:\Users\cfilip09\Downloads\dblp.xml\dblp.xml', 'C:\Master\TimeSeries\data\\result.csv')


year_df = pandas.read_csv('C:\Master\TimeSeries\data\\result.csv', names=["year"])
select2016 = year_df['year'] <= 2016
all_data = year_df.groupby('year')['year'].count().reset_index(name="count").as_matrix()
data = year_df[select2016].groupby('year')['year'].count().reset_index(name="count").as_matrix()

year_data = list()

for item in data:
    year_data.append([item[0]])

# print data[:, 0]
# print data[:, 1]

svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(year_data, data[:,1]).predict(year_data)
#y_poly = svr_poly.fit(year_data, data[:,1]).predict(year_data)

plt.plot(year_data, data[:,1])
plt.plot(year_data, y_rbf, color='navy', lw=2, label='RBF model')
#plt.plot(year_data, y_poly, color='darkorange', lw=2, label='Polynomial model')
plt.ylabel('number of articles')
plt.xlabel('year')
plt.title('Time series regression')
plt.show()