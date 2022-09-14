from allennlp_models import pretrained
allenslr=pretrained.load_predictor('structured-prediction-srl-bert')
import string
import re
def extract(sentence):
    """
    from a sentence use AllenNLP SRLtool to extrac (subject-object, predicate) tuples
    
    Arguments
        sentence :: str
    
    Returns:
        If possible
        (str, str) list 
        Else
        None
    """
    remove='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'
    input=sentence.translate(str.maketrans('', '', remove))
    count=[]                                        # num de palabras sin anotar por verbo
    counter=0
    output=allenslr.predict(input)

    if len(output['verbs'])==0:                     # Ningun verbo anotado
        print("ERROR: Ningún verbo anotado")
        return None
    elif len(output['verbs'])==1:                   # Un verbo anotado
        tags=output['verbs'][0]['tags']             # Valida el etiquetado
        if bool(re.search('ARG[0-5]', string) for string in tags):
            tuple=create_tuples(output)             # Extracción de información
        else:
            print("ERROR: Insuficientes etiquetas para crear la tupla")
            return None
    else:                                           # Más de un verbo anotado
        for verb in output['verbs']:                
            for tag in verb['tags']:
                if tag == 'O':
                    counter+=1                      # Cuenta las palabras sin anotar
            count.append(counter)
            counter=0
        tags=output['verbs'][search(count)]['tags'] #selecciona la mejor anotación
        if bool(re.search('ARG[0-5]', string) for string in tags):  # Valida etiquetas
            tuple=create_tuples(output, search(count))  # Extracción de información
        else:
            print("ERROR: Insuficientes etiquetas para crear la tupla")
            return None
    return tuple
def search(a):
    """
    search algorithm to find the smallest amount of unlabel words

    Args:
    a :: list

    Return
    index of  the list :: int
    """
    j=0
    for i in range(1,len(a)):
        if a[i]<a[j]:
            j=i
    return j
def create_tuples(output, index=0):
    """
    Create a tuple from PropBank Anotations

    Arg:
    output :: Dict create with AllenNLP SLR
    index :: int to acces to the correct labeling 
    
    Returns:
    (sj_oj, prd) list
    """
    SP=[]
    O=[]
    tags=output['verbs'][index]['tags']
    words=output['words']
    for a in range(0,5):
        if any('ARG'+str(a) in string for string in tags):
            for i in range(len(tags)):
                if bool(re.search('ARG['+str(a+1)+'-5]', tags[i])):
                    O.append(words[i])
                elif not 'O' in tags[i]:
                    SP.append(words[i])
            break
    SP=" ".join(SP)
    O=" ".join(O)
    return [SP,O]