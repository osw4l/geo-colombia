import requests
import json
import re



def _red(msj):
    return "\033[0;31m{0}\033[0m".format(msj)


def _green(msj):
    return "\033[0;32m{0}\033[0m".format(msj)


def _orange(msj):
    return "\033[0;33m{0}\033[0m".format(msj)


def _blue(msj):
    return "\033[0;34m{0}\033[0m".format(msj)


def _purple(msj):
    return "\033[0;35m{0}\033[0m".format(msj)


def _cyan(msj):
    return "\033[0;36m{0}\033[0m".format(msj)

def remove_yen(chain):
    return chain.replace('¥', 'Ñ')


def run():
    print('\n')
    print(_green('Welcome to api colombia by 0sw4l'))

    request = requests.get('https://raw.githubusercontent.com/santiblanko/colombia.geojson/master/mpio.json')
    response = request.json()

    print('{} {} {}'.format(_green('Request'), _cyan('Municipios'), _green('Ready')))
    request_municipios = requests.get('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json')
    response_departamentos = request_municipios.json()
    print('{} {} {}'.format(_green('Request'), _orange('Departamentos'), _green('Ready')))

    data = {}

    for item in response_departamentos['features']:

        departamento = remove_yen(item['properties']['NOMBRE_DPT'].upper())

        if not departamento in data.keys():
            data[departamento] = {
                'numero': item['properties']['DPTO'],
                'perimetro': item['properties']['PERIMETER'],
                'area_total': item['properties']['AREA'],
                'hectareas': item['properties']['HECTARES'],
                'area': item['geometry'],
                'municipios': {}
            }
            print('{} : {}'.format('se creo el departamento', _cyan(departamento)))

    for item in response['features']:
        municipio = remove_yen(item['properties']['NOMBRE_MPI'].upper())
        departamento = remove_yen(item['properties']['NOMBRE_DPT'].upper())

        if not municipio in data[departamento]['municipios'].keys():
            data[departamento]['municipios'][municipio] = {
                'nombre': municipio,
                'departamento': departamento,
                'cabecera_municipa': item['properties']['NOMBRE_CAB'],
                'area': item['geometry']
            }

        print('Municipio {} , se le asigno el departamento {}'.format(
            _green(municipio),
            _cyan(departamento),
        ))

    print(_green(data))

    with open('outputs/colombia.json', 'w') as json_file:
        json.dump(data, json_file)

    print(_orange('Bye ;) informacion llena'))


run()
