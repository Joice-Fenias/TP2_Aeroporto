# Funções para ler/escrever em ficheiro (JSON ou CSV)

#Create template for saving the data
data = {
    "passengers":[],
    "flights":[],
    "tickets":[]
}

#Function to read json files
def load_data(data):
    #Try to open the file, if not create it
    try:
        pass
    except FileNotFoundError:
        pass