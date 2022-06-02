import json
import re

from bson import json_util, ObjectId
from flask import Response
from werkzeug.security import generate_password_hash

from config import mongo, bd_table

db = mongo.get_database(bd_table).clients


def create_user(self):
    r = json.loads(self)
    id = r.get('_id')
    name = r.get('name')
    last_name = r.get('last_name')
    photo_link = r.get('photo_link')
    passw = r.get('password')
    street = r.get('street')
    number = r.get('number')
    neighborhood = r.get('neighborhood')
    complement = r.get('complement')
    city = r.get('city')
    email = r.get('email')
    if id is not None:
        return edit_user(id, name, passw, email, last_name, photo_link, photo_link, street, number, neighborhood,
                         complement, city)

    user = get_user_email(email)
    if user:
        response = json_util.dumps({'message': 'Já existe um usuário cadastrado com esse email.'})
        return Response(response, mimetype='application/json', status=400)

    hash_password = generate_password_hash(passw)
    id = db.insert_one(
        {'name': name, 'email': email, 'password': hash_password, 'last_name': last_name, 'photo_link': photo_link,
         "street": street, "number": number, "neighborhood": neighborhood, "complement": complement, "city": city}
    )
    jsonDate = {
        'id': str(id.inserted_id),
        'name': name,
        'password': hash_password,
        'last_name': last_name,
        'photo_link': photo_link,
        'street': street,
        'number': number,
        'neighborhood': neighborhood,
        'complement': complement,
        'city': city,
        'email': email
    }
    response = json_util.dumps(jsonDate)
    return Response(response, mimetype='application/json', status=201)


def edit_user(id, name, passw, email, last_name, photo_link, street, number, neighborhood, complement, city):
    if passw is not None:
        hash_password = generate_password_hash(passw)
        db.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'name': name, 'email': email, 'password': hash_password, 'last_name': last_name,
                      'photo_link': photo_link,
                      "street": street, "number": number, "neighborhood": neighborhood, "complement": complement,
                      "city": city}}
        )
        jsonDate = {
            'id': str(id),
            'name': name,
            'email': email,
            'last_name': last_name,
            'photo_link': photo_link,
            'street': street,
            'number': number,
            'neighborhood': neighborhood,
            'complement': complement,
            'city': city
        }
        response = json_util.dumps(jsonDate)
        return Response(response, mimetype='application/json', status=200)
    db.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'name': name, 'email': email, 'last_name': last_name, 'photo_link': photo_link,
                  "street": street, "number": number, "neighborhood": neighborhood, "complement": complement,
                  "city": city}}
    )
    jsonDate = {
        'id': str(id),
        'name': name,
        'email': email,
        'last_name': last_name,
        'photo_link': photo_link,
        'street': street,
        'number': number,
        'neighborhood': neighborhood,
        'complement': complement,
        'city': city
    }
    response = json_util.dumps(jsonDate)
    return Response(response, mimetype='application/json', status=200)


def get_user_email(email):
    return db.find_one({'email': email})


def list_user():
    find = db.find({}, {'password': 0})
    if find:
        response = json_util.dumps(find)
        return Response(response, mimetype='application/json', status=200)
    response = json_util.dumps({'message': 'Nenhum registro encontrado'})
    return Response(response, mimetype='application/json', status=400)


def find_user(self):
    args = json.loads(self)
    if args:
        name = args.get('name')
        email = args.get('email')
        filter = {}
        if email is not None:
            filter['email'] = email
        if name is not None:
            rgx = re.compile('.*' + name + '.*', re.IGNORECASE)
            filter['name'] = rgx

        response = json_util.dumps(db.find(filter))
        return Response(response, mimetype='application/json', status=200)
    else:
        return list_user()


def delete_user(self):
    r = json.loads(self)
    id = r.get('_id')
    find = db.delete_one({'_id': ObjectId(id)})
    if find:
        response = json_util.dumps({'message': 'Deletado com sucesso!'})
        return Response(response, status=200)
    response = json_util.dumps({'message': 'Id não encontrado'})
    return Response(response, status=400)
