import sqlite3
import requests
import pandas as pd
from flask import Flask, jsonify, request


DATABASE = "base1.db"
CSV_FILE = "https://raw.githubusercontent.com/Paulita11111/TPinf/main/Updated_Clothing_Products.csv"

def crear_tabla():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute ('DROP TABLE IF EXISTS bigbasket')
        c.execute('''
                    CREATE TABLE IF NOT EXISTS bigbasket (
                    "index" INT,
                    product VARCHAR(100), 
                    category VARCHAR(100), 
                    sub_category VARCHAR(100), 
                    brand VARCHAR(100), 
                    sale_price REAL, 
                    market_price REAL, 
                    type VARCHAR(100), 
                    rating REAL, 
                    description VARCHAR(1000),
                    sale_price_euro REAL,
                    market_price_euro REAL)
                    ''')
        conn.commit()  

def importar_productos():
    # Diagnóstico previo para ver las líneas del archivo CSV en caso de error
    # Descomenta las siguientes líneas si necesitas inspeccionar el archivo
    # with open(CSV_FILE, 'r') as f:
    #     lines = f.readlines()
    #     for i in range(40, 60):  # Ajusta el rango si es necesario
    #         print(lines[i])

    # Ahora leeremos el CSV especificando que ignora las líneas con errores
    try:
        df = pd.read_csv(CSV_FILE, on_bad_lines='skip', delimiter=",")  # Usa ',' o el delimitador adecuado
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            for _, row in df.iterrows():
                c.execute(
                        """
                    INSERT INTO bigbasket ("index", product, category, sub_category, brand, sale_price, market_price, type, rating, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, 
                        (
                            row["index"],
                            row["product"],
                            row["category"],
                            row["sub_category"],
                            row["brand"],
                            row["sale_price"],
                            row["market_price"],
                            row["type"],
                            row["rating"],
                            row["description"],
                        ), 
                    )
            conn.commit()
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

def get_products():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        products = conn.execute("SELECT * FROM bigbasket").fetchall() 
        return products

def get_product(id):
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        product = conn.execute("SELECT rowid, * FROM bigbasket WHERE rowid = ?", (id,)).fetchone()
        if product is None:
            return {"message": "Product not found"}, 404
        return dict(product)

def add_product():
    new_product = request.get_json()
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            INSERT INTO bigbasket ("index", product, category, sub_category, brand, sale_price, market_price, type, rating, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            new_product['index'], new_product['product'], new_product['category'], new_product['sub_category'],
            new_product['brand'], new_product['sale_price'], new_product['market_price'], new_product['type'],
            new_product['rating'], new_product['description']
        ))
        conn.commit()

def update_product(id):
    with sqlite3.connect(DATABASE) as conn:
        product_details = request.get_json()
        conn.execute('''
            UPDATE bigbasket SET "index" = ?, product = ?, category = ?, sub_category = ?, brand = ?, sale_price = ?, market_price = ?, type = ?, rating = ?, description = ?
            WHERE rowid = ?
        ''', (
            product_details['index'], product_details['product'], product_details['category'], product_details['sub_category'],
            product_details['brand'], product_details['sale_price'], product_details['market_price'], product_details['type'],
            product_details['rating'], product_details['description'], id
        ))
        conn.commit()

def delete_product(id):
    with sqlite3.connect(DATABASE) as conn:
        result = conn.execute("DELETE FROM bigbasket WHERE id = ?", (id,)) 
        conn.commit()

def obtener_valores_dolar():
    base_url = "https://dolarapi.com/v1/cotizaciones/"
    currency = "eur"
    url = f"{base_url}{currency}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        venta = data.get("venta")
        if venta:
            return venta
        else:
            print("Error: 'venta' no encontrado en la respuesta de la API")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos de la API: {e}")
        return None

if __name__ == "__main__":
    try:
        crear_tabla()
        importar_productos()
        print("Database and table creation successful, and products imported.")
    except Exception as e:
        print(f"An error occurred: {e}")

