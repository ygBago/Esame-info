import csv

class ExamException(Exception):
    pass

class CSVFile:

    def __init__(self, name):
        self.name = name

    def get_data(self):
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))
            return None

        else:
            data = []
            my_file = open(self.name, 'r')

            for line in my_file:
                
                elements = line.split(',')
                #pulisco il \n 
                elements[-1] = elements[-1].strip()
                
                if elements[0] != 'date':
                                
                    data.append(elements)
            
            my_file.close()
            
            # Quando ho processato tutte le righe, ritorno i dati
            return data
class CSVTimeSeriesFile(CSVFile):
    
    def get_data(self):
        
        set_valori = set()
        string_data = super().get_data()


        lunghezza_lista = len(string_data)
        for i in range(lunghezza_lista):
            for j in range(i + 1, lunghezza_lista):
                if string_data[i] == string_data[j]:
                    raise ExamException("Duplicated Data")

        if not string_data:
            raise ExamException("File CSV invalido: {}".format(self.name))
        
        numerical_data = []
        
        for string_row in string_data:
            
            numerical_row = []

            if not string_row:
                continue
            
            for i,element in enumerate(string_row):
                
                if i == 0:
                    numerical_row.append(element)
                    
                else:
                    try:
                        numerical_row.append(float(element))
                    except Exception as e:
                        print('Errore in conversione del valore "{}" a numerico: "{}"'.format(element, e))
                        break
                
            if len(numerical_row) == len(string_row):
                numerical_data.append(numerical_row)
        return numerical_data



def compute_increments(time_series, first_year, last_year):
    primo=False
    secondo=False
    for l in time_series:
        if first_year in l[0]:
            primo= True
    for l in time_series:
        if last_year in l[0]:
            secondo = True

    if primo == False or secondo == False:
        raise ExamException("Date non presenti nel csv")

    cont = 0
    anno = None
    anno_p = None
    dati_dict = dict()  #chiamo il costruttore e inizializzo il dict
    final_dict = dict()
    if not isinstance(first_year, str) or not isinstance(last_year, str):
        raise ExamException("Entrambe le variabili devono essere di tipo stringa")


    try:
        first_year = int(first_year)
    except Exception:
        raise ExamException("first_year")

    try:
        last_year = int(last_year)
    except Exception:
        raise ExamException("last_year")

    if (last_year < first_year):
        t = first_year
        first_year = last_year
        last_year = t

    for s in time_series:
        anni_l = (s[0].split('-'))
        anni_l[0] = int(anni_l[0])
        if anni_l[0] >= first_year and anni_l[0] <= last_year:
            anno = anni_l[0]
            if anno_p == None:
                anno_p = anno 
            dati_dict[anno] = dati_dict.get(anno, 0) + s[1]
            if anno_p == anno:
                cont+=1
            elif cont == 0:
                raise Exception("Impossibile")
            else:
                dati_dict[anno_p] = float(dati_dict.get(anno_p,0) / cont)
                cont = 1 
            anno_p = anno
    dati_dict[anno] =  float(dati_dict.get(anno,0) / cont)
    dati_dict_b = {chiave: valore for chiave, valore in dati_dict.items() if valore != 0.0}
    anni = list(dati_dict_b.keys())
    
    for e in range(len(anni)-1):
        
        chiave = str(anni[e]) + "-" +str(anni[e+1])

        final_dict[chiave] = dati_dict_b.get(anni[e+1],0) - dati_dict_b.get(anni[e],0)
    return final_dict
