import pandas as pd
import requests

df = pd.read_excel("~/iNaturalist_dataset.xlsx") #or invasoras.pt_dataset.xlsx
print(df)

i = 0
for url in df["image_url"]:
    img_data = requests.get(url).content
    with open('image' + str(i) + '.jpg', 'wb') as handler:
        handler.write(img_data)
        i += 1
