import numpy as np
import csv
import pandas as pd
import configparser


config = configparser.ConfigParser()
config.read( "BUSCA.cfg" )
resultfile = config[ 'section' ][ 'RESULTADOS' ]
inputs = config[ 'section' ][ 'MODELO' ].split()
consulta = config[ 'section' ][ 'CONSULTAS' ]

palavras = []
query_matrix = []
query_norm_vector = []

with open( 'lista_invertida.csv', mode='r' ) as csv_file:
    
    csv_reader = csv.DictReader( csv_file, delimiter = ';') 

    for row in csv_reader:
        
        palavra = row[ 'PALAVRA' ]
        palavras += [ palavra ]


with open( consulta , mode='r' ) as csv_file:
    
    csv_reader = csv.DictReader( csv_file, delimiter = ';') 

    for row in csv_reader:
        
        query_vector = np.zeros( ( len( palavras ),  ), dtype = int )
        query_terms = eval( row[ 'Query_Text' ] )

        for term in query_terms:
            
            try: 
                query_vector[ palavras.index( term ) ] = 1
            except ValueError:
                continue
        
        query_matrix += [ query_vector ]


for vector in range( len( query_matrix ) ):

    query_norm_vector += [ np.linalg.norm( query_matrix[ vector ] ) ]


matriztd = np.loadtxt( inputs[0], delimiter = ';', dtype = float )

document_norm_vector = np.loadtxt( inputs[1], delimiter = ';', dtype = float )


### Matriz de porduto escalar M[Q][D]

def gerarMatrizEscalar( matrizqpesos, matrizpesos ):
    
    matriz_produto_escalar = []

    for query in matrizqpesos:

        vector_produto_escalar = []
        
        for document in matrizpesos:

            vector_produto_escalar += [ np.dot( query, document ) ]
        
        matriz_produto_escalar += [ vector_produto_escalar ]
    
    return matriz_produto_escalar


### Matriz de produto de normas no formato M[Q][D]

def gerarMatrizNormas( querynv, documentnv ):
    
    matriz_produto_normas = []

    for query in querynv:

        matriz_produto_normas += [ documentnv * query ]
    
    return matriz_produto_normas

### Matriz de similaridade

def gerarMatrizSimilaridade( matrizpe, matrizpn ):

    matriz_similaridade = []

    for query in range( len( matrizpe ) ):

        vector_similaridade = []
        for document in range( len( matrizpe[0] ) ):
            vector_similaridade += [ matrizpe[ query ][ document ] / matrizpn[ query ][ document ] ]
        
        matriz_similaridade += [ vector_similaridade ]
    
    return matriz_similaridade

x = gerarMatrizEscalar( query_matrix, matriztd )
y = gerarMatrizNormas( query_norm_vector, document_norm_vector )
z = gerarMatrizSimilaridade( x, y )

matriz_output = []

for querynum in range( len( z ) ) :

    vector_output = []

    vector_output += [ querynum + 1 ]

    vector_output += [ [ max( z[ querynum ] ), z[ querynum ].index( max( z[ querynum ] ) ) + 1 ] ]
    matriz_output += [ vector_output ]

df = pd.DataFrame( data = matriz_output ) 
df.to_csv( resultfile, sep = ';', header = False, float_format = '%.2f', index = False )


