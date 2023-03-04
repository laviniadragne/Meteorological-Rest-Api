from flask import Flask, request, Response, jsonify
import mysql.connector
import json
from os import getenv

app = Flask(__name__)


mydb = mysql.connector.connect(
  host = getenv('PMA_HOST'),
  port = int(getenv('PMA_PORT')),
  user = getenv('MYSQL_USER'),
  password = getenv('MYSQL_PASSWORD'),
  database = getenv('MYSQL_DATABASE')
)

mycursor = mydb.cursor()

def isFloat(var):
    if isinstance(var, float) or isinstance(var, int):
        return True
    return False


def exist_id_in_table(table, id):
    # Verific daca exista id-ul in baza de date:
    sql_exist_id = "SELECT * FROM {} WHERE id = {}".format(table, id)

    mycursor.execute(sql_exist_id)

    myresult = mycursor.fetchall()

    # Nu exista id-ul
    if len(myresult) == 0:
        return False
    return True


@app.route('/api/countries', methods=["POST"])
def post_countries():
    # Iau datele ce trebuie introduse
    try:
        nume = request.get_json()["nume"]
        lat = request.get_json()["lat"]
        lon = request.get_json()["lon"]
    except:
        return Response(status = 400)


    # Verific tipul variabilelor
    if not isinstance(nume, str) or not isFloat(lat) or not isFloat(lon):
        return Response(status = 400)


    sql = f"INSERT INTO Tari(nume_tara, latitudine, longitudine) VALUES (\"{nume}\", {lat}, {lon})"

    try:
        mycursor.execute(sql)
    except:
        return Response(status = 409)

    mydb.commit()

    return json.dumps({'id':mycursor.lastrowid}), 201


@app.route('/api/countries', methods=["GET"])
def get_countries():
    mycursor.execute("SELECT * FROM Tari")

    myresult = mycursor.fetchall()

    res_list = []
    for row in myresult:
        res_list.append({'id':row[0], 'nume':row[1], 'lat':row[2], 'lon':row[3]})

    return json.dumps(res_list), 200


@app.route('/api/countries/<int:id>', methods=["PUT"])
def put_countries(id):
    data = request.get_json()

    try:
        my_id = data["id"]
        nume = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
    except:
        return Response(status = 400)

    if id != my_id:
        return Response(status = 400)


    # Verific tipul variabilelor
    if not isinstance(my_id, int) or not isinstance(nume, str) or not isFloat(lat) or not isFloat(lon):
        return Response(status = 400)


    sql = "UPDATE Tari SET nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s", (nume, lat, lon, id)
    try:
        mycursor.execute(*sql)
    except Exception as e:
        # Intrare duplicata
        if e.errno == 1062:
            return Response(status = 409)
        else:
            return Response(status = 404)

    mydb.commit()

    return Response(status = 200)


def extract_orase(lst):
    return [item[0] for item in lst]

@app.route('/api/countries/<int:id>', methods=["DELETE"])
def delete_countries(id):

    # # Verific daca exista id-ul in baza de date:
    if not exist_id_in_table("Tari", id):
        return Response(status = 404)


    # Extrag orasele asociate acelei tari
    sql_orase = "SELECT id FROM Orase WHERE id_tara = %s"
    val_orase = (id, )
    mycursor.execute(sql_orase, val_orase)
    orase = mycursor.fetchall()

    if not len(orase) == 0 :
        orase1 = extract_orase(orase)
        # Sterg temperaturile asociate oraselor
        format_strings = ','.join(['%s'] * len(orase1))
        mycursor.execute("DELETE FROM Temperaturi WHERE id_oras IN (%s)" % format_strings, tuple(orase1))
        mydb.commit()

        # Sterg orasele
        sql_orase = "DELETE FROM Orase WHERE id_tara = %s"
        val_orase = (id, )
        mycursor.execute(sql_orase, val_orase)
        mydb.commit()

    # Sterg tarile
    sql = "DELETE FROM Tari WHERE id = %s"
    val = (id, )

    try:
        mycursor.execute(sql, val)
    except Exception as e:
        return Response(status = 404)

    mydb.commit()

    return Response(status = 200)


@app.route('/api/cities', methods=["POST"])
def post_cities():
    # Iau datele ce trebuie introduse
    try:
        id_tara = request.get_json()["idTara"]
        nume = request.get_json()["nume"]
        lat = request.get_json()["lat"]
        lon = request.get_json()["lon"]
    except:
        return Response(status = 400)

    # Verific tipul variabilelor
    if not isinstance(id_tara, int) or not isinstance(nume, str) or not isFloat(lat) or not isFloat(lon):
        return Response(status = 400)


    # Nu exista tara
    if not exist_id_in_table("Tari", id_tara):
        return Response(status = 404)


    sql = f"INSERT INTO Orase (id_tara, nume_oras, latitudine, longitudine) VALUES ({id_tara}, \"{nume}\", {lat}, {lon})"

    try:
        mycursor.execute(sql)
    except:
        return Response(status = 409)

    mydb.commit()

    return json.dumps({'id':mycursor.lastrowid}), 201


@app.route('/api/cities', methods=["GET"])
def get_cities():
    mycursor.execute("SELECT * FROM Orase")

    myresult = mycursor.fetchall()

    res_list = []
    for row in myresult:
        res_list.append({'id':row[0], 'idTara':row[1], 'nume':row[2], 'lat':row[3], 'lon':row[4]})

    return json.dumps(res_list), 200


@app.route('/api/cities/country/<int:id_tara>', methods=["GET"])
def get_city(id_tara):

    # Verific daca id-ul exista in baza de date
    if not exist_id_in_table("Tari", id_tara):
        return Response(status = 404)

    sql = "SELECT * FROM Orase WHERE id_tara = {}".format(id_tara)
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    res_list = []
    for row in myresult:
        res_list.append({'id':row[0], 'idTara':row[1], 'nume':row[2], 'lat':row[3], 'lon':row[4]})

    return json.dumps(res_list), 200


@app.route('/api/cities/<int:id>', methods=["PUT"])
def put_cities(id):
    data = request.get_json()

    try:
        my_id = data["id"]
        id_tara = data["idTara"]
        nume = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
    except:
        return Response(status = 400)

    # Verific tipul variabilelor
    if (not isinstance(my_id, int)
        or not isinstance(id_tara, int)
        or not isinstance(nume, str)
        or not isFloat(lat)
        or not isFloat(lon)):
        return Response(status = 400)


    if id != my_id:
        return Response(status = 400)

    # Nu exista tara in tabela de countries
    # cu care vreau sa fac update
    if not exist_id_in_table("Tari", id_tara):
        return Response(status = 404)


    sql = "UPDATE Orase SET id_tara = %s, nume_oras = %s, latitudine = %s, longitudine = %s WHERE id = %s", (id_tara, nume, lat, lon, id)
    try:
        mycursor.execute(*sql)
    except Exception as e:
        # Intrare duplicata
        if e.errno == 1062:
            return Response(status = 409)
        else:
            return Response(status = 404)

    mydb.commit()

    return Response(status = 200)


@app.route('/api/cities/<int:id>', methods=["DELETE"])
def delete_cities(id):

    # Verific daca exista id-ul in baza de date:
    if not exist_id_in_table("Orase", id):
        return Response(status = 404)


    # Sterg temperaturile asociate acelui oras
    sql = "DELETE FROM Temperaturi WHERE id_oras = %s"
    val = (id, )
    mycursor.execute(sql, val)
    mydb.commit()

    # Sterg orasele
    sql = "DELETE FROM Orase WHERE id = %s"
    val = (id, )

    try:
        mycursor.execute(sql, val)
    except Exception as e:
        return Response(status = 404)

    mydb.commit()

    return Response(status = 200)


@app.route('/api/temperatures', methods=["POST"])
def post_temperatures():
    # Iau datele ce trebuie introduse
    try:
        idOras = request.get_json()["idOras"]
        valoare = request.get_json()["valoare"]
    except:
        return Response(status = 400)

    # Verific tipul variabilelor
    if not isinstance(idOras, int) or not isFloat(valoare):
        return Response(status = 400)

    # Nu exista orasul
    if not exist_id_in_table("Orase", idOras):
        return Response(status = 404)

    sql = f"INSERT INTO Temperaturi (valoare, id_oras) VALUES ({valoare}, {idOras})"

    try:
        mycursor.execute(sql)
    except:
        return Response(status = 409)

    mydb.commit()

    return json.dumps({'id':mycursor.lastrowid}), 201


@app.route('/api/temperatures', methods=["GET"])
def get_temperatures_1():

    # Iau argumentele
    lat = request.args.get('lat', default = -1)
    lon = request.args.get('lon', default = -1)
    fr = request.args.get('from', default = -1)
    until = request.args.get('until', default = -1)

    sql = "SELECT Temperaturi.id, \
                  Temperaturi.valoare, \
                  Temperaturi.timestamp \
           FROM Orase JOIN Temperaturi ON \
           Temperaturi.id_oras = Orase.id"

    # Are cel putin un parametru
    if (lat != -1) or (lon != -1) or (fr != -1) or (until != -1):
        sql += " WHERE "
        val = []
        is_first = True
        if not fr == -1:
            sql += "UNIX_TIMESTAMP(Temperaturi.timestamp) >= UNIX_TIMESTAMP(%s)"
            val.append(fr)
            is_first = False

        if not until == -1:
            if not is_first:
                sql += " AND "
            else:
                is_first = False
            sql += "UNIX_TIMESTAMP(Temperaturi.timestamp) <= UNIX_TIMESTAMP(%s)"
            val.append(until)
    
        if not lon == -1:
            if not is_first:
                sql += " AND "
            else:
                is_first = False
            sql += "Orase.longitudine = %s"
            val.append(lon)

        if not lat == -1:
            if not is_first:
                sql += " AND "
            else:
                is_first = False
            sql += "Orase.latitudine = %s"
            val.append(lat)

    val_tuple = tuple(val)
    mycursor.execute(sql, val_tuple)
    myresult = mycursor.fetchall()

    res_list = []
    for row in myresult:
        res_list.append({'id':row[0], 'valoare':row[1], 'timestamp':row[2]})

    return jsonify(res_list), 200


@app.route('/api/temperatures/cities/<int:id_oras>', methods=["GET"])
def get_temperatures_2(id_oras):

    # Iau argumentele
    fr = request.args.get('from', default = -1)
    until = request.args.get('until', default = -1)

    # Construiesc clauza
    sql = "SELECT * FROM Temperaturi WHERE id_oras = %s"
    val = [id_oras]

    if not fr == -1:
        sql += "AND UNIX_TIMESTAMP(timestamp) >= UNIX_TIMESTAMP(%s)"
        val.append(fr)

    if not until == -1:
        sql += "AND UNIX_TIMESTAMP(timestamp) <= UNIX_TIMESTAMP(%s)"
        val.append(until)

    val_tuple = tuple(val)
    mycursor.execute(sql, val_tuple)
    myresult = mycursor.fetchall()

    res_list = []
    for row in myresult:
        res_list.append({'id':row[0], 'valoare':row[1], 'timestamp':row[2]})

    return jsonify(res_list), 200


@app.route('/api/temperatures/countries/<int:id_tara>', methods=["GET"])
def get_temperatures_3(id_tara):

    # Iau argumentele
    fr = request.args.get('from', default = -1)
    until = request.args.get('until', default = -1)

    sql = "SELECT Temperaturi.id, \
                  Temperaturi.valoare, \
                  Temperaturi.timestamp \
           FROM Orase JOIN Temperaturi ON \
                Temperaturi.id_oras = Orase.id \
           WHERE \
                Orase.id_tara = %s"
    val = [id_tara]

    # Are cel putin un parametru
    if not fr == -1:
        sql += "AND UNIX_TIMESTAMP(timestamp) >= UNIX_TIMESTAMP(%s)"
        val.append(fr)

    if not until == -1:
        sql += "AND UNIX_TIMESTAMP(timestamp) <= UNIX_TIMESTAMP(%s)"
        val.append(until)

    val_tuple = tuple(val)
    mycursor.execute(sql, val_tuple)
    myresult = mycursor.fetchall()

    res_list = []
    for row in myresult:
        res_list.append({'id':row[0], 'valoare':row[1], 'timestamp':row[2]})

    return jsonify(res_list), 200


@app.route('/api/temperatures/<int:id>', methods=["PUT"])
def put_temperatures(id):
    data = request.get_json()

    try:
        my_id = data["id"]
        id_oras = data["idOras"]
        valoare = data["valoare"]
    except:
        return Response(status = 400)

    # Verific tipul variabilelor
    if not isinstance(my_id, int) or not isinstance(id_oras, int) or not isFloat(valoare):
        return Response(status = 400)

    if id != my_id:
        return Response(status = 400)

    # Nu exista orasul in tabela de orase
    # cu care vreau sa fac update
    if not exist_id_in_table("Orase", id_oras):
        return Response(status = 404)


    sql = "UPDATE Temperaturi SET valoare = %s, id_oras = %s WHERE id = %s", (valoare, id_oras, id)
    try:
        mycursor.execute(*sql)
    except Exception as e:
        # Intrare duplicata
        if e.errno == 1062:
            return Response(status = 409)
        else:
            return Response(status = 404)

    mydb.commit()
    return Response(status = 200)


@app.route('/api/temperatures/<int:id>', methods=["DELETE"])
def delete_temperatures(id):

    # Verific daca exista temperatura in baza de date:
    if not exist_id_in_table("Temperaturi", id):
        return Response(status = 404)

    sql = "DELETE FROM Temperaturi WHERE id = %s"
    val = (id, )

    try:
        mycursor.execute(sql, val)
    except:
        return Response(status = 404)

    mydb.commit()
    return Response(status = 200)


if __name__ == "__main__":
    app.run('0.0.0.0', port = 6000, debug=True)
