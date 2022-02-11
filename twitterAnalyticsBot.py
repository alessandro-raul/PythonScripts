import tweepy as tw
import pandas as pd

API_KEY = "m25i78PT1MBt6Dqk9SjhupAOa"
API_SECRET = "w3jBh9HL49I90ugZOTR9fWk4bU2mfp8jn9A9sLX7v5qLF7Kyao"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABZlZAEAAAAADRqDSCZJbBpCuv00MGB06OhtI4k%3Dru3CorH7KCjYPa8wbx9AHzDJVkPeWrXprT3kfVGTqWnLAy19Sy"
ACCESS_TOKEN = "4605286767-NqB1F3bLGXIzNzAf8SdtbBvqLEq9gs2MVNK4E4u"
ACCESS_SECRET = "UuXaWglFFRnrdhvaTKGIgtbm5S7xD4SWLYNItVH68dgGg"

max_results = 100
start_time = "2022-02-10T19:00:01Z"

cliente = tw.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)
resposta = cliente.search_recent_tweets('#bbb22', max_results=max_results, start_time=start_time)
dados = resposta.data

base = []

for i in dados:

    linha = [0 for j in range(7)]
    texto = i.text

    if('RT' in texto):
        posicao = texto.find(':')
        texto = texto[posicao+2:]
        linha[6] = 1

    linha[0] = texto
    linha[1] = 1 if ('jade' in texto.lower()) else 0
    linha[2] = 1 if ('arthur' in texto.lower()) else 0
    linha[3] = 1 if ('paulo andré' in texto.lower()) else 0
    linha[4] = 1 if ('naiara' in texto.lower()) else 0
    linha[5] = 1 if ('thiago abravanel' in texto.lower()) else 0

    base.append(linha)

baseBBB = pd.DataFrame(base)
baseBBB.columns = ['tweet', 'Jade', 'Arthur', 'Paulo André', 'Naiara', 'Thiago', 'RT']

baseView = baseBBB.drop(['tweet', 'RT'], axis=1)

comentarios = baseView.sum().sort_values(ascending=False).to_list()
participantes = baseView.sum().sort_values(ascending=False).index.to_list() 

base2 = pd.DataFrame(zip(participantes, comentarios))
base2.columns = ['participante', 'comentarios']

total_comentarios = base2['comentarios'].sum()

base2['perc'] = base2['comentarios']/total_comentarios
base2['perc_acum'] = base2['perc'].cumsum()

base2['perc_format'] = base2['perc'].map("{:.1%}".format)
base2['perc_acum_format'] = base2['perc_acum'].map("{:.1%}".format)

base2View = base2.drop(['perc', 'perc_acum'], axis=1)
print(base2View)