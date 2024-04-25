import csv
import numpy as np
import pandas as pd	
import math
from collections import Counter
import configparser

dict = {}
rowcount = 0
palavra = 0
max = 0

config = configparser.ConfigParser()
config.read( "INDEX.cfg" )
input = config[ 'section' ][ 'LEIA' ]
outputs = config[ 'section' ][ 'ESCREVA' ].split()

with open( input, mode='r' ) as csv_file:
    
    csv_reader = csv.DictReader( csv_file, delimiter = ';') 

    for row in csv_reader:
        
        lista_invertida = eval( row[ 'ID' ] )
        numdoc = -1
        
        for docnum in lista_invertida:

            if docnum == numdoc:
                continue
            else:
                count = lista_invertida.count( docnum )
                if docnum in dict:
                    dict[ docnum ] += count
                else: dict[ docnum ] = count
            numdoc = docnum

            if max < docnum:
                max = docnum
        
        rowcount += 1
    
matriztd = np.zeros( ( rowcount , max ), dtype = float )

with open( input, mode='r' ) as csv_file:
    
    csv_reader = csv.DictReader( csv_file, delimiter = ';') 
    
    for row in csv_reader:

        lista_invertida = eval( row[ 'ID' ] )
        numdoc = -1
        
        df = len( Counter( lista_invertida ).keys() )

        for docnum in lista_invertida:

            count = 0
            if docnum == numdoc:
                continue
            else:
                count = lista_invertida.count( docnum )
                tf = float( count / dict[ docnum ] )
                idf = math.log( len( lista_invertida ) / df )
                matriztd[ palavra ][ docnum - 1 ] = tf * idf

            numdoc = docnum
        
        palavra += 1


matriztd = matriztd.transpose()
document_norm_vector = []

for i in range( max ):

    document_norm_vector += [ np.linalg.norm( matriztd[ i ] ) ]


df = pd.DataFrame( data = matriztd.astype( float ) ) 
df.to_csv( outputs[0], sep = ';', header = False, float_format = '%.2f', index = False )

df = pd.DataFrame( data = document_norm_vector ) 
df.to_csv( outputs[1], sep = ';', header = False, float_format = '%.2f', index = False )