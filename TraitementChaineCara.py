# Fonction 


def rreplace(s, old, new):  
    # fonction replace() pour les dernière occurence 

    li = s.rsplit(old, 4) 
    return new.join(li)

