import pandas as pd

dfs = []
for i in range(24):
    try: 
        df1 = pd.read_csv('result{}.csv'.format(i), sep = ';', encoding = 'utf-8', usecols= ['name', 'position', 'profession', 'profexp', 'anotherexp', 'strongs', 'contacts'])
        dfs.append(df1)
    except Exception:
        print(i)
        continue
df = pd.concat(dfs)
print(df)
df.drop_duplicates(keep='first', inplace=True)
df.to_csv('result_final.csv', encoding='utf-8-sig', index=False, sep = ';')
