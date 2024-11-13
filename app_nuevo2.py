from flask import Flask, jsonify, request
import db_nuevo1

app = Flask(__name__)

# Endpoint para obtener todos los productos
@app.route("/products", methods=["GET"])
def get_products():
    products = db_nuevo1.get_products()  # Ahora obtenemos los productos de la base de datos
    clean_products = []
    for product in products:
        clean_products.append({
            "id": product["rowid"],
            "index": product["index"],
            "product": product["product"],
            "category": product["category"],
            "sub_category": product["sub_category"],
            'brand': product["brand"],
            'sale_price': product["sale_price"],
            'market_price': product["market_price"],
            'type': product["type"],
            'rating': product["rating"],
            'description': product["description"],
        })
    return jsonify(clean_products), 200


# Endpoint para obtener un producto por ID
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db_nuevo1.get_product(id)  # Obtener producto de la base de datos por ID
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product), 200


# Endpoint para añadir un nuevo producto
@app.route("/products", methods=["POST"])
def add_product():
    product_details = request.get_json()
    db_nuevo1.add_product(
        product_details["index"], 
        product_details["product"], 
        product_details["category"], 
        product_details["sub_category"], 
        product_details["brand"], 
        product_details["sale_price"], 
        product_details["market_price"], 
        product_details["type"], 
        product_details["rating"], 
        product_details["description"]
    )
    return jsonify({"message": "Product successfully created"}), 201


# Endpoint para actualizar un producto por ID
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product_details = request.get_json()
    updated_product = db_nuevo1.update_product(
        id, 
        product_details["index"], 
        product_details["product"], 
        product_details["category"], 
        product_details["sub_category"], 
        product_details["brand"], 
        product_details["sale_price"], 
        product_details["market_price"], 
        product_details["type"], 
        product_details["rating"], 
        product_details["description"]
    )
    if updated_product:
        return jsonify({"message": "Product successfully updated"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


# Endpoint para eliminar un producto por ID
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    deleted_product = db_nuevo1.delete_product(id)
    if deleted_product:
        return jsonify({"message": "Product successfully deleted"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@app.route("/products/eur", methods=["GET"])
def get_products_euro():
    valor_euro = db_nuevo1.obtener_valores_dolar()
    if valor_euro is None:
        return jsonify({"message": "Error al obtener el valor del euro"}), 500

    products = db_nuevo1.get_products()
    result = [
        {
            "id": product["rowid"],
            "index": product["index"],
            "product": product["product"],
            "category": product["category"],
            "sub_category": product["sub_category"],
            "brand": product["brand"],
            "sale_price": product["sale_price"] / valor_euro,
            "market_price": product["market_price"] / valor_euro,
            "type": product["type"],
            "rating": product["rating"],
            "description": product["description"],
        }
        for product in products
    ]
    return jsonify(result), 200


if __name__ == "_main_":
    db_nuevo1.crear_tabla()
    db_nuevo1.importar_productos()  # Asegurarse de que la base de datos esté inicializada correctamente
    app.run(debug=True)  # Inicia el servidor de Flask
