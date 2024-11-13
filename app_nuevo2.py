from flask import Flask, jsonify, request
import db_nuevo1
import requests

app = Flask(__name__)
products = db_nuevo1.get_products()


#endpoint para obtener todos los productos
@app.route("/products", methods=["GET"])
def get_products():
    products = db_nuevo1.get_products()
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


#endpoint para obtener un producto por ID
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for product in products: 
        if product["id"] == id:
            return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

#endpoint para añadir un nuevo producto
@app.route("/products", methods=["POST"])
def add_product():
    product_details = request.get_json()
    db_nuevo1.add_product(product_details["index"], 
                          product_details["product"], 
                          product_details["category"], 
                          product_details["sub_category"], 
                          product_details["brand"], 
                          product_details["sale_price"], 
                          product_details["market_price"], 
                          product_details["type"], 
                          product_details["rating"], 
                          product_details["description"], 
                          "", "", "", "", "", "", "", "", "", "")
    return jsonify({"message": "Product succesfully created"}), 200

#endpoint para actualizar un producto por ID
@app.route("/products/<int:id>", methods=["PUT"])  # /<> es para desp actualizar el id en particular que yo quiera
def update_product(id):
    product_details = request.get_json()
    for product in products:
        if(product["id"] == id): 
            product["index"] = product_details["index"]
            product["product"] = product_details["product"]
            product["category"] = product_details["category"]
            product["sub_category"] = product_details["sub_category"]
            product["brand"] = product_details["brand"]
            product["sale_price"] = product_details["sale_price"]
            product["market_price"] = product_details["market_price"]
            product["type"] = product_details["type"]
            product["rating"] = product_details["rating"]
            product["description"] = product_details["description"]
            return jsonify({"message": "Product succesfully updated"})
    return jsonify({"message": "Product not found"}), 400

#endpoint para eliminar un producto por ID
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    for product in products:
        if product["id"] == id: 
            products.remove(product)
            return jsonify({"message": "Product succesfully deleted"}), 200
    return jsonify({"message": "Product not found"}), 404

@app.route("/products/eur", methods=["GET"])
def get_products_euro():
    valor_euro = db_nuevo1.obtener_valores_dolar()
    if valor_euro is None:
        return jsonify({"message": "Error al obtener el valor del euro"}), 500

    products = db_nuevo1.get_products()
    result = [
        {
            "id": product["id"],
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




if __name__ == "__main__":
    db_nuevo1.crear_tabla()
    db_nuevo1.importar_productos()
    db_nuevo1.obtener_valores_dolar()
    
