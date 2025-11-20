from flask import Flask, render_template, request, redirect, url_for

import database

# remember to $ pip install flask

database.initialize("pets.db")

app = Flask(__name__)

@app.route("/", methods=["GET"]) 
@app.route("/list", methods=["GET"])
def get_list():
    pets = database.get_pets()  # List of Pet model instances
    pet_dicts = [pet.__data__ for pet in pets]  # Convert each to a dictionary
    return render_template("list.html", pets=pet_dicts)

@app.route("/kind", methods=["GET"])
@app.route("/kind/list", methods=["GET"])
def get_kind_list():
    kinds = database.get_kinds()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/create", methods=["GET"])
def get_create():
    kinds = database.get_kinds() 
    # print("<<<<",kinds) # List of Kind model instances
    kind_dicts = [{"id": kind.id, "name": kind.name} for kind in kinds]
    return render_template("create.html", kinds=kind_dicts) 

@app.route("/create", methods=["POST"])
def post_create():
    data = dict(request.form)
    print("DATA=",data)
    database.create_pet(data)
    return redirect(url_for("get_list"))  

@app.route("/delete/<id>", methods=["GET"])
def get_delete(id):
    database.delete_pet(id)
    return redirect(url_for("get_list"))  

@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    pet = database.get_pet_by_id(id)

    data = {
        "id": pet.id,
        "name": pet.name,
        "age": pet.age,
        "kind": pet.kind.name,  # assuming you want kind name as "type"
        "owner": pet.owner
    }
    return render_template("update.html", data=data)

@app.route("/update/<id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)
    kind_name = data.get("kind")
    kind = database.get_kind_by_name(kind_name)
    if not kind:
        return render_template("error.html", error_text=f"Kind '{kind_name}' not found.")
    data["kind_id"] = kind.id
    del data["kind"]  
    database.update_pet(id, data)
    return redirect(url_for("get_list"))  

@app.route("/kind/create", methods=["GET"])
def get_kind_create():
        return render_template("kind_create.html")

@app.route("/kind/create", methods=["POST"])
def post_kind_create():
    data = dict(request.form)
    database.create_kind(data)
    return redirect(url_for("get_kind_list"))

@app.route("/kind/delete/<id>", methods=["GET"])
def get_kind_delete(id):
    try:
        database.delete_kind(id)
    except Exception as e:
        return render_template("error.html", error_text=str(e))
    return redirect(url_for("get_kind_list"))

@app.route("/kind/update/<id>", methods=["GET"])
def get_kind_update(id):
    data = database.get_kind(id)
    return render_template("kind_update.html",data=data)

@app.route("/kind/update/<id>", methods=["POST"])
def post_kind_update(id):
    data = dict(request.form)
    database.update_kind(id, data)
    return redirect(url_for("get_kind_list"))
