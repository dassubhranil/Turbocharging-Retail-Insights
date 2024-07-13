import pandas as pd

file_path = 'include/dataset/online_retail.csv'
output_path = 'include/dataset/online_retail.csv'

# Attempt to open the file with a different encoding, like 'ISO-8859-1'
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Save the dataframe in UTF-8 encoding
df.to_csv(output_path, index=False, encoding='utf-8')