from flask import Flask, jsonify, request
import db_nuevo1

app = Flask(__name__)

# Endpoint para obtener todos los productos
@app.route("/products", methods=["GET"])
def get_products():
    products = db_nuevo1.get_products()  # Obtener productos de la base de datos
    clean_products = []
    for product in products:
            clean_products.append({"id": product[0],
            "index": product[1],
            "product": product[2],
            "category": product[3],
            "sub_category": product[4],
            'brand':product[5],
            'sale_price': product[6],
            'market_price': product[7],
            'type': product[8],
            'rating': product[9],
            'description': product[10],
            })
    return jsonify(clean_products), 200


# Endpoint para obtener un producto por ID
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db_nuevo1.get_product(id)  # Obtener producto por ID de la base de datos
    if "message" in product:
        return jsonify(product), 404  # Si el producto no se encuentra, devuelve 404
    return jsonify(product), 200


# Endpoint para añadir un nuevo producto
@app.route("/products", methods=["POST"])
def add_product():
    product_details = request.get_json()  # Obtener datos del producto desde el cuerpo de la solicitud
    db_nuevo1.add_product(product_details)  # Añadir el producto a la base de datos
    return jsonify({"message": "Product successfully created"}), 201


# Endpoint para actualizar un producto por ID
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product_details = request.get_json()  # Obtener los detalles del producto desde el cuerpo de la solicitud
    db_nuevo1.update_product(id, product_details)  # Actualizar el producto
    return jsonify({"message": "Product successfully updated"}), 200


# Endpoint para eliminar un producto por ID
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    db_nuevo1.delete_product(id)  # Eliminar producto por ID
    return jsonify({"message": "Product successfully deleted"}), 200


@app.route("/products/eur", methods=["GET"])
def get_products_euro():
    valor_euro = db_nuevo1.obtener_valores_dolar()  # Obtener el valor del euro
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
            "sale_price": product["sale_price"] / valor_euro,  # Conversión de precio a euros
            "market_price": product["market_price"] / valor_euro,  # Conversión de precio a euros
            "type": product["type"],
            "rating": product["rating"],
            "description": product["description"],
        }
        for product in products
    ]
    return jsonify(result), 200


if __name__ == "__main__":
    db_nuevo1.crear_tabla()  # Crear tabla si no existe
    db_nuevo1.importar_productos()  # Importar productos desde el CSV
    app.run(debug=True)  # Iniciar el servidor de Flask
