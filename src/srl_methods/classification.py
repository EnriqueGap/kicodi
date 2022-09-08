from allennlp_models import pretrained
allenslr=pretrained.load_predictor('structured-prediction-srl-bert')
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
    count=[]                                        # num de palabras sin anotar por verbo
    counter=0
    output=allenslr.predict(sentence)

    if len(output['verbs'])==0:                     # Ningun verbo anotado
        print("ERROR: Ningún verbo anotado")
        return None
    elif len(output['verbs'])==1:                   # Un verbo anotado
        tags=output['verbs'][0]['tags']             # Valida el etiquetado
        if any('ARG' in string for string in tags):
            labels=output['verbs'][0]['description']
            tuple=create_tuples(labels)             # Extracción de información
        else:
            print("ERROR: Insuficientes argumentos para crear la tupla")
            return None
    else:                                           # Más de un verbo anotado
        for verb in output['verbs']:                # Valida eitquetas para cada verbo
            for tag in verb['tags']:
                if tag == 'O':
                    counter+=1                      # Cuenta las palabras sin anotar
            count.append(counter)
            counter=0
        labels=output['verbs'][search(count)]['description']
        tuple=create_tuples(labels)                 # Extracción de información
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
def create_tuples(labels):
    """
    Create a tuple from PropBank Anotations

    Arg:
    sentence :: str
    
    Returns:
    (sj_oj, prd) list
    """
    copy = labels
    SP=''
    O=''
    agent='ARG0' in labels
    patient='ARG1' in labels
    if agent:
        SP=re.findall(r'ARG0: (.+?)\]',labels)[0]
    SP=SP+" "+re.findall(r'\[V: (.+?)\]',labels)[0]    
    if object:
        O=re.findall(r'ARG1: (.+?)\]',labels)[0]
    copy=copy.replace(SP, "")
    copy=copy.replace(O, "")
    for item in re.findall(r':(.+?)\]',copy):
        SP+=item
    SP.strip()
    O.strip()
    return [SP,O]