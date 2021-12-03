import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_excel('PS7 predictive policing sample data (1).xlsx')
print(df)

# Generate a report
profile = ProfileReport(df)
profile.to_file(output_file="PS7.html")