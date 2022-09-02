"""
Extract data near-Earth objects, close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
    objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    counter = 0

    with open(neo_csv_path) as csvfile:

        csvreader = csv.DictReader(csvfile)

        for i in csvreader:

            designation = i['pdes']

            if i['pha'] == 'Y':
                hazardous = True
            else:
                hazardous = False

            name = i['name']

            try:
                diameter = float(i['diameter'])
            except ValueError:
                diameter = None

            neo = NearEarthObject(designation, hazardous, name, diameter)

            neos.append(neo)

    # print('neos loaded')

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close
    approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    counter = 0
    with open(cad_json_path) as a:

        json_data = json.load(a)

        json_data_header = json_data['fields']
        json_data_data = json_data['data']

        for json_row in json_data_data:
            dict_row = dict(zip(json_data_header, json_row))

            time = dict_row['cd']

            try:
                distance = float(dict_row['dist'])
            except TypeError:
                distance = float('nan')

            try:
                velocity = float(dict_row['v_rel'])
            except TypeError:
                velocity = float('v_rel')

            designation = dict_row['des']

            neo = NearEarthObject('designation', True, 'name', '1.0')

            approach = CloseApproach(
                time=time,
                distance=distance,
                velocity=velocity,
                neo=neo,
                _designation=designation)

            approaches.append(approach)

    # print('approaches loaded')

    return approaches
