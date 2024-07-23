import configparser
import xml.dom.minidom
import nltk
import glob
import csv
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


config = configparser.ConfigParser()
config.read( "GLI.cfg" )
lista_invertida_csv = config[ 'section' ][ 'ESCREVA' ]
lista_invertida_csv = lista_invertida_csv.replace( "'", "" )

list_csv_abstract = []
lista_invertida = []
dict_lista_invertida = {}
porter_nltk_st = PorterStemmer()
stopw = stopwords.words( 'english' )

def preProcessamento( lista, records ):
    
    for record in records:

        
        dict_csv_abstract = {}
        recordnum  = record.getElementsByTagName( 'RECORDNUM' )[0].childNodes[0].nodeValue
        
        try:
            abstract = record.getElementsByTagName( 'ABSTRACT' )[0].childNodes[0].nodeValue
        except IndexError:
            try:
                abstract = record.getElementsByTagName( 'EXTRACT' )[0].childNodes[0].nodeValue
            except IndexError:
                abstract = ""

        tokenizer = RegexpTokenizer(r'\w+')
        abstract = ''.join(c for c in abstract if not c.isdigit())
        tokens = tokenizer.tokenize( abstract )
        abstract = [ w for w in tokens if not w.lower() in stopw]
        abstract = list( map( porter_nltk_st.stem, abstract ) )

        for term_index in range( len( abstract ) ):
            abstract[ term_index ] = abstract[ term_index ].upper()
        
        dict_csv_abstract[ 'RECORDNUM' ] = int( recordnum )
        dict_csv_abstract[ 'ABSTRACT' ] = abstract
        lista.append( dict_csv_abstract )

    return lista


def gerarListaInvertida( lista, lista_preprocessada, grouprecords ):
    
    for record in preProcessamento( lista_preprocessada, grouprecords ):

        for term in record[ 'ABSTRACT' ]:
            
            if term in dict_lista_invertida:
                dict_lista_invertida[ term ] += [ int( record[ "RECORDNUM" ] ) ]
            else: 
                dict_lista_invertida[ term ] = [ int( record[ "RECORDNUM" ] ) ]



for file in glob.glob( "cf7[4-9].xml"):
    
    # file = config[ 'section' ][ 'LEIA' ]
    # file = file.replace( "'", "" )
    domtree = xml.dom.minidom.parse( file )
    group = domtree.documentElement
    records = group.getElementsByTagName( 'RECORD' )
    gerarListaInvertida( lista_invertida, list_csv_abstract, records )
    list_csv_abstract = []
    
for key in dict_lista_invertida:

    dupla = { "PALAVRA": key, "ID": dict_lista_invertida[ key ] }
    lista_invertida.append(dupla)



with open( lista_invertida_csv , mode = 'w' ) as csvfile:
    
    fieldnames = lista_invertida[0].keys()
    writer = csv.DictWriter( csvfile, fieldnames = fieldnames, delimiter = ";" )
    writer.writeheader()
    writer.writerows( lista_invertida )
    
