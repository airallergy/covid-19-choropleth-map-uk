from retrieve_data import retrieveData
from parse_data import parseData
from plot_uk_latest import plot_uk_latest
from plot_ldn_latest import plot_ldn_latest


for country in ['Eng', 'Wls', 'Sct', 'Nir']:
    retrieveData(country)
    parseData(country)

plot_uk_latest()
plot_ldn_latest()
