import pandas as pd
from matplotlib import pyplot as plt

# df = pd.io.json.json_normalize(pd.json.load(open('data.json')))
# df.to_csv('data.csv')
df = pd.DataFrame.from_csv('data.csv')
df.columns
df.describe()
df.text[0]
geo = pd.DataFrame(pd.np.array([pd.np.array(ll) for ll in df['geo.coordinates'].dropna()]), columns=['lat', 'lon'])
plt.plot(geo.lon, geo.lat, '.')
plt.show()
