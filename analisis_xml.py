from lxml import etree
import pandas as pd


def extract(file):

    df = pd.read_csv(file, encoding='latin')
    
    return df

def write_xml(df,padre,name):

    columnas = df.columns.values
    num_c = len(columnas)
    tipos = df.dtypes
    nans = df.isnull().sum()

    padre.set('nombre_documento', name)
    padre.set('numero_columnas',str(num_c))

    for columna in columnas:
        
        tipo = tipos[columna]

        hijo = etree.SubElement(padre, 'columna')
        hijo.set('nombre_columna', str(columna))
        hijo.set('NaN', str(nans[columna]))
        hijo.set('tipo_datos', str(tipo))

    return

def write_xml_recomend(padre,df):

    ingredientes = list(df['Ingredientes'])
    valores = df['Unidades a comprar']

    for index in range(len(ingredientes)):

        ingrediente = ingredientes[index]
        valor = valores[index]

        hijo = etree.SubElement(padre, 'ingrediente')
        hijo.set('nombre_ingrediente', ingrediente)
        hijo.set('cantidad_recomendada', str(valor))


    return

if __name__ == '__main__':

    head = etree.Element('analisis')
    head.text = 'Analisis de la tipologia de datos presente en los csvs dados'

    csvs = ['pizzas.csv', 'pizza_types.csv', 'orders_clean.csv', 'order_details_clean.csv', 'data_dictionary.csv']

    # Hago el análisis por archivos y voy formando a la ver el arbol que compondrá el archivo XML

    for index in range(0,len(csvs)):
        name = csvs[index]
        hijo = etree.SubElement(head, f'archivo_{index+1}')
        df = extract(name)

        write_xml(df,hijo,name)

    tree = etree.ElementTree(head)


    # Creo el arbol con los datos del dataset de recomendación creado en la practica anterior

    df_rec = extract('recomendacion_ingredientes.csv')
    head_2 = etree.Element('recomendacion')
    head_2.text = 'Compra semanal recomendada a Maeven Pizzas (medida mediante la técnica de ventana deslizante)'

    write_xml_recomend(head_2,df_rec)

    tree_2 = etree.ElementTree(head_2)

    # Cargamos el arbol creado en un archivo XML

    with open("analisis.xml", "wb") as file:
        tree.write(file,xml_declaration=True, pretty_print=True, encoding="utf-8")

    with open("recomendacion.xml", "wb") as file:
        tree_2.write(file,xml_declaration=True, pretty_print=True, encoding="utf-8")

    print('Archivos XML creado')




