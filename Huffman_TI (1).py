# Autor:** Carlos J. Escudero
# Asignatura** Teoría de la Información. Grado en Ciencia e Ingeniería de Datos (GCED)
# Creación:** Universidade da Coruña (UDC) [Febrero 2024]
# Basado en el código del artículo: https://bitybyte.github.io/Huffman-coding/

import heapq

class Huffman:
    def __init__(self, diccionario):
        self.diccionario = diccionario  # Diccionario => simbolo: probabilidad (o frecuencia)
        self.arbol=self.genera_arbol(diccionario)   # Tupla con el árbol Huffman creado desde el diccionario
        self.codigo=self.genera_codigo(self.arbol)  # Diccionario => simbolo: codigo 

    def genera_arbol(self,dic):
        """
        Obtiene tuplas anidadas que contienen el árbol de la codificación Huffman.

        Parámetros:
        dic -- Diccionario => simbolo: probabilidad (o frecuencia)

        Retorna:
        res -- Tupla anidada con el árbol Huffman
        """
        q = []
        # Agregamos todos los símbolos a la pila
        for ch,pr in dic.items():
            # La fila de prioridad está ordenada por
            # prioridad y profundidad
            heapq.heappush(q,(pr,0,ch))

        # Empezamos a mezclar símbolos juntos
        # hasta que la fila tenga un elemento
        while len(q) > 1:
            e1 = heapq.heappop(q) # El símbolo menos probable
            e2 = heapq.heappop(q) # El segundo menos probable
            
            # Este nuevo nodo tiene probabilidad e1[0]+e2[0]
            # y profundidad mayor al nuevo nodo
            nw_e = (e1[0]+e2[0],max(e1[1],e2[1])+1,[e1,e2])
            heapq.heappush(q,nw_e)
        return q[0] # Devolvemos el arbol sin la fila

    def genera_codigo(self,tree):
        """
        Obtiene el diccionario de simbolos y sus códigos binarios.

        Parámetros:
        tree -- Tupla anidada con el árbol del algoritmo de Huffman

        Retorna:
        res -- Diccionario => simbolo: codigo 
        """
        res = {} # La estructura que vamos a devolver
        search_stack = [] # Pila para DFS
        # El último elemento de la lista es el prefijo!
        search_stack.append(tree+("",)) 

        while len(search_stack) > 0:
            elm = search_stack.pop()
            if type(elm[2]) == list:
                # En este caso, el nodo NO es una hoja del árbol, es decir que tiene nodos hijos
                prefix = elm[-1]

                # El hijo izquierdo tiene "0" en el prefijo
                search_stack.append(elm[2][1]+(prefix+"0",))
                # El hijo derecho tiene "1" en el prefijo
                search_stack.append(elm[2][0]+(prefix+"1",))
                continue
            else:
                # El nodo es una hoja del árbol, así que obtenemos el código completo y lo agregamos
                code = elm[-1]
                res[elm[2]] = code
            pass
        res=dict(sorted(res.items()))
        return res

    def print_code(self,N=0):
        """
        Imprime el diccionario => simbolo: codigo

        Parámetros:
        N -- número de simbolos mostrados en consola (N=0 => se ven todos)

        Retorna:
        res -- True
        """
        contador = 0
        for s,c in self.codigo.items():
            if N==0:
                print(f'{s:>4}: {c}')
            else:
                if contador != N:
                    print(f'{s:>4}: {c}')
                    contador += 1
                else:
                    print('...')
                    break
        return True

    def codifica(self,content):
        """
        Obtiene un string con la secuencia binaria codificada según Huffman.

        Parámetros:
        x -- Secuencia de símbolos

        Retorna:
        codificado -- String de la secuencia codificada
        """

        codificado = ""
        # Iteramos sobre cada elemento del archivo de entrada
        for val in content:
            code = self.codigo[val]
            codificado = codificado + code
        # Agregamos el 1 a la izquierda, y el marcador de final a la derecha
        # codificado = '1' + codificacdo + self.codigo['end']
        # Agregamos ceros para que la longitud del resultado sea un múltiplo de 8
        # codificado = codificado + (len(codificado) % 8 * "0")
        #return int(res,2) # Convertimos a entero! (2 porque es base 2)
        return codificado

    def decodifica(self,cadena_codificada):
        """
        Obtiene una lista con la secuencia decodificada según Huffman.

        Parámetros:
        cadena_codificada -- String con la secuencia binaria codificada según Huffman.

        Retorna:
        decodificado -- Lista con la secuencia decodificada
        """
        # Invertir el diccionario de codificación para facilitar la búsqueda
        codigos_invertidos = {v: k for k, v in self.codigo.items()}
        
        decodificado = []  # Cadena para almacenar el resultado decodificado
        codigo_temporal = ""  # Cadena temporal para acumular bits hasta encontrar un código válido
        for bit in cadena_codificada:
            codigo_temporal += bit  # Añadir el bit actual al código temporal
            if codigo_temporal in codigos_invertidos:
                # Si el código temporal coincide con un código en el diccionario, añadir el símbolo correspondiente
                #decodificado += str(codigos_invertidos[codigo_temporal])
                decodificado.append(codigos_invertidos[codigo_temporal])
                codigo_temporal = ""  # Reiniciar el código temporal para el siguiente símbolo
        return decodificado

# Pruebas al ejecutar este código directamente
if __name__ == "__main__":
    #x = 'abcdeabcdabcaba'
    #codec = Huffman({'a': 5, 'b':4, 'c':3, 'd': 2, 'e':1})
    x=[0,1,2,3,4]
    codec = Huffman({0:2, 1:5, 2:2, 3:3, 4:2})

    print('codec.diccionario')
    print(type(codec.diccionario))
    print(codec.diccionario,'\n')

    print('codec.arbol')
    print(type(codec.arbol))
    print(codec.arbol,'\n')

    print('codec.codigo')
    print(type(codec.codigo))
    print(codec.codigo)
    codec.print_code()
    
    
    print('\nSecuencia codificada')
    cadena_c = codec.codifica(x)
    print(type(cadena_c))
    #print(bin(cadena_c)[2:])
    print(cadena_c)

    print('\nSecuencia decodificada')
    cadena_r = codec.decodifica(cadena_c)
    print(type(cadena_r))
    print(cadena_r)