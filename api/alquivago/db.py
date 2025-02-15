from alquivago.f_filters import f_area, f_bathrooms, f_bedrooms, f_currency, f_price, f_typres, f_zones
from alquivago.sort_delete import sort_apply, delete__id

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
propertys = "collected_data"

def build_query_sort_project(filters, conv):
    """
    Builds the `query` predicate, `sort` and `projection` attributes for a given
    filters dictionary.
    """
    sort = filters["sort"]
    query = {}
    project = None # elije que datos traer, de momento traeremos todos

    #constantes
    more_bathrooms = 3
    more_bedrooms = 4
    conversion_min = None
    conversion_max = None
    conv = 40 #valor de cmabio entre UYU y USD

    #filtrado
    filters_list = []
    f_filters = {
        "currency": f_currency,
        "types": f_typres,
        "zones": f_zones,
        "bedrooms": f_bedrooms,
        "bathrooms": f_bathrooms,
        "price": f_price,
        "area": f_area}
    for k, v in filters.items():
        if v is not None and k in f_filters.keys():
            add = f_filters[k](v)
            if add is not None:
                filters_list.append(add)
    
    if "price" not in sort and "price" in filters:
        sort["price"] = 1# orden base acendente
    
    if "area" not in sort and "area" in filters:
        sort["area"] = -1# orden base desendente
    
    #filtro de proximidad con la latitud y longitud
    
    if filters_list:
        query["$and"] = filters_list
    
    return query, sort, project




def get_rents(conv, filters, page, rents_per_page):
    """
    Returns a cursor to a list of rental property documents.

    Based on the page number and the number of properties per page, the result may
    be skipped and limited.

    The `filters` from the API are passed to the `build_query_sort_project`
    method, which constructs a query, sort, and projection, and then that query
    is executed by this method (`get_rental_properties`).

    Returns 2 elements in a tuple: (properties, total_num_properties)
    """
    query, sort, project = build_query_sort_project(filters, conv)

    if project:
        cursor = db[propertys].find(query, project)
    else:
        cursor = db[propertys].find(query)
    
    rents = sort_apply(list(cursor), sort, conv)

    total_num_rents = len(rents)
    skip = (page - 1) * rents_per_page


    if (skip + rents_per_page) <= total_num_rents:
        rents = rents[skip:skip + rents_per_page]
    elif skip <= total_num_rents:
        rents = rents[skip:]
    else:
        rents = []
    rents = delete__id(rents)

    return (rents, total_num_rents, query)


def get_rent(id):
    """
    Given a rental property ID, return a property with that ID, with the comments for that
    property embedded in the property document. The comments are joined from the
    comments collection using expressive $lookup.
    """
    try:
        query = {"id": {"$in": id}}

        rents = db[propertys].find(query)

        return (list(rents))
    except StopIteration:
        return None

    except Exception as e:
        return {}


def get_all(conv, sort, page, rents_per_page):
    """
    List all type of rents
    """
    cursor = db[propertys].find()

    rents = sort_apply(list(cursor), sort, conv)

    total_num_rents = len(rents)
    skip = (page - 1) * rents_per_page


    if (skip + rents_per_page) <= total_num_rents:
        rents = rents[skip:skip + rents_per_page]
    elif skip <= total_num_rents:
        rents = rents[skip:]
    else:
        rents = []
    rents = delete__id(rents)

    return (rents, total_num_rents)