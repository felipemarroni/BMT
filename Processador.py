import nltk
import configparser
import xml.dom.minidom
import csv
import matplotlib.pyplot as plt
from unidecode import unidecode
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

#nltk.download( 'stopwords' )
#nltk.download( 'punkt' )

### Extraindo as informações do config file

config = configparser.ConfigParser()
config.read( "PC.cfg" )
file = config[ 'section' ][ 'LEIA' ]
file = file.replace( "'", "" )
consulta = config[ 'section' ][ 'CONSULTAS' ]
consulta = consulta.replace( "'", "" )


### Pacotes e estruturas utilizadas para fazer o pré-processamento/manipulação da Query

domtree = xml.dom.minidom.parse( file )
group = domtree.documentElement
queries = group.getElementsByTagName( 'QUERY' )

list_csv_consultas = []
porter_nltk_st = PorterStemmer()
stopw = stopwords.words( 'english' )

### Extraindo as informações do XML da Query (Query Number, Query Text, Results, Records)

for query in queries:

    dict_csv_consultas = {}
    
    querynumber = query.getElementsByTagName( 'QueryNumber' )[0].childNodes[0].nodeValue
    querytext = query.getElementsByTagName( 'QueryText' )[0].childNodes[0].nodeValue
    
    tokenizer = RegexpTokenizer(r'\w+')
    querytext = ''.join(c for c in querytext if not c.isdigit())
    tokens = tokenizer.tokenize( querytext )
    querytext = [ w for w in tokens if not w.lower() in stopw]
    #querytext = list( map( porter_nltk_st.stem, querytext ) )
    
    for term_index in range( len( querytext ) ):
        querytext[ term_index ] = querytext[ term_index ].upper()

    
    dict_csv_consultas[ 'Query_Number' ] = int( querynumber )
    dict_csv_consultas[ 'Query_Text' ] = querytext
    list_csv_consultas.append( dict_csv_consultas )

### Criando arquivo CSV das consultas processadas

with open( consulta , mode = 'w' ) as csvfile:
    
    fieldnames = list_csv_consultas[0].keys()
    writer = csv.DictWriter( csvfile, fieldnames = fieldnames, delimiter = ";" )
    writer.writeheader()
    writer.writerows( list_csv_consultas )

### Criando arquivo CSV dos resultados esperados

# with open( consulta , mode = 'w' ) as csvfile:
    
#     fieldnames = list_csv_consultas[0].keys()
#     writer = csv.DictWriter( csvfile, fieldnames = fieldnames, delimiter =";" )
#     writer.writeheader()
#     writer.writerows( list_csv_consultas )