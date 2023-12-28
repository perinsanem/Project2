from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


DATABASE = "products.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_no INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            city TEXT,
            image TEXT,
            category TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def add_sample_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    if count == 0:
       
        products = [
            (1, "Villa", "Kiralık Villa", 220.000, "Istanbul", "images/konut1.jpg", "Konut"),
            (2, "Apartman Dairesi", "Satılık Daire", 2.850000, "Izmir", "images/konut2.jpg", "Konut"),
            (3, "Dükkan", "Kiralık Köşe Dükkan", 45.000, "Antalya", "images/işyeri1.jpg", "İş Yeri"),
            (4, "Ön Cepheli Dükkan", "Satılık Ana Cadde Üzeri Dükkan", 13.500000, "Tekirdag", "images/işyeri2.jpg", "İş Yeri"),
            (5, "Arsa", "Asfalt Yola Cephe Arsa", 2.595000, "Istanbul", "images/arsa.jpg", "Arsa"),
            (6, "Peugot", "Peugot 2008 GT 1.5", 1.560000, "Bursa", "images/otomobil1.jpg", "Otomobil"),
            (7, "Ferrari", "F8 Tributo", 31.950000, "Antalya", "images/otomobil2.jpg", "Otomobil"),
            (8, "Golf", "Golf 8 Life - R Görünüm - Hatasız,Boyasız,Tramersiz", 1.207000, "Ankara", "images/otomobil3.jpg", "Otomobil"),
            (9, "Dodge", "Dodge RAM 2500 Mega Laramice", 3.100000, "Aydın", "images/pickup.jpg", "Arazi, SUV & Pickup"),
            (10, "Jeep", "Jeep Wrangler 2.8 CRD", 3.525000, "Manisa", "images/araziaraba.jpg", "Arazi, SUV & Pickup"),
            
        ]

        cursor.executemany(
            """
            INSERT INTO products (ad_no, name, description, price, city, image, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            products
        )

        conn.commit()
    
    conn.close()


def get_all_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def setup_and_get_products():
    create_table()
    add_sample_products()
    return get_all_products()

@app.route('/')
def index():
   
    products = setup_and_get_products()

   
    isyeri_products = [product for product in products if product[7] == 'İş Yeri']
    konut_products = [product for product in products if product[7] == 'Konut']
    arsa_product = [product for product in products if product[7] == 'Arsa']
    emlak_products = [product for product in products if product[7] in {'İş Yeri', 'Konut', 'Arsa'}]
    otomobil_products = [product for product in products if product[7] == 'Otomobil']
    arazisuvpickup_products = [product for product in products if product[7] == 'Arazi, SUV & Pickup']
    vasıta_products = [product for product in products if product[7] in {'Otomobil', 'Arazi, SUV & Pickup'}]
    isyeri_count = len(isyeri_products)
    konut_count = len(konut_products)
    arsa_count = len(arsa_product)
    emlak_count = len(emlak_products)
    otomobil_count = len(otomobil_products)
    arazisuvpickup_count = len( arazisuvpickup_products)
    vasıta_count = len(vasıta_products)

    return render_template('index.html', products=products, isyeri_count=isyeri_count, konut_count=konut_count, arsa_count=arsa_count, emlak_count=emlak_count, otomobil_count=otomobil_count, arazisuvpickup_count=arazisuvpickup_count,  vasıta_count=vasıta_count)


@app.route('/konut')
def konut():
    products = get_all_products()  
    konut_products = products[0:2]
    return render_template('konut_template.html', products=konut_products)

@app.route('/isyeri')
def isyeri():
    products = get_all_products()
    isyeri_products = products[2:4]
    return render_template('isyeri_template.html', products=isyeri_products)

@app.route('/arsa')
def arsa():
   
    products = get_all_products()
    arsa_product = products[4:5]
    return render_template('arsa_template.html', products=arsa_product)

@app.route('/otomobil')
def otomobil():
    products = get_all_products()
    otomobil_products = products[5:8]
    return render_template('otomobil_template.html', products=otomobil_products)

@app.route('/arazisuvpickup')
def arazisuvpickup():
    products = get_all_products()
    arazisuvpickup_products = products[8:10]
    return render_template('arazisuvpickup_template.html', products=arazisuvpickup_products)

def get_product_by_id(product_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    conn.close()
    return product

@app.route('/product/<int:product_id>')
def product_details(product_id):
    
    product = get_product_by_id(product_id)

    if product:
        return render_template('product_details.html', product=product)
    else:
       
        return render_template('product_not_found.html')
    
def perform_search(query, products):
   
    
    query_lower = query.lower()
    
    search_results = [product for product in products if any(query_lower in str(attr).lower() for attr in product[1:])]

    return search_results

@app.route('/search', methods=['GET'])
def search():
    products = get_all_products()
    query = request.args.get('query', '')
    results = perform_search(query, products)
    
    return render_template('search_results.html', results=results, query=query)



if __name__ == '__main__':
    app.run(debug=True)
