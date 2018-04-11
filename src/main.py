import os.path
import pandas
import matplotlib.pyplot as plt

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

parse_file('C:\Users\cfilip09\Downloads\dblp.xml\dblp.xml', 'C:\Master\TimeSeries\data\\result.txt')


year_df = pandas.read_csv('C:\Master\TimeSeries\data\\result.txt', names=["year"])
select2016 = year_df['year'] <= 2016 
data = year_df[select2016].groupby('year')['year'].count().reset_index(name="count").as_matrix()

plt.plot(data[:,0], data[:,1])
plt.ylabel('number of articles')
plt.xlabel('year')
plt.show()