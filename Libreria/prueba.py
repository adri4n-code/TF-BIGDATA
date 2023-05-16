

import requests

def buscarbook(nombre_libro):

    url = f'https://www.googleapis.com/books/v1/volumes?q={nombre_libro}'
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        item = data['items'][0]
        titulo = item['volumeInfo']['title']
        autores = item['volumeInfo'].get('authors', 'Autor desconocido')
        editorial = item['volumeInfo'].get('publisher', '')
        categoria = item['volumeInfo'].get('categories', '')
    
        print(f"Autor(es): {autores}")
        print(f"Título: {titulo}")
        print(f"Editorial: {editorial}")
        print(f"Categoría: {categoria}")


nombre_libro = input(f'Pon el nombre del libro:')
buscarbook(nombre_libro)
