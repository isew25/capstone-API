from flask import Flask, request 
import pandas as pd 
app = Flask(__name__) 



# tampilan home
@app.route('/')
def homepage():
    return 'Hallo'

# halaman dokumentasi
@app.route('/docs')
def index():
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Dokumentasi API Chinnook.db</h1>
    </body>
</html>
<html>
    <font size="4"> 1. / , method = GET </font><br>
    <font size="4"> &ensp; Menampilkan halaman pembuka  </font><br>
    <font size="4"> &ensp; </font><br>
    <font size="4"> 2. /docs , method = GET </font><br>
    <font size="4"> &ensp; Menampilkan halaman dokumentasi  </font><br>
    <font size="4"> &ensp; </font><br>
    <font size="4"> 3. /top5artists/<font color="red"> country_name </font> , method = GET </font><br>
    <font size="4"> &ensp; Mendapatkan 5 artis paling populer di <font color="red"> country_name </font><br> 
    <font size="4"> &ensp; </font><br>
    <font size="4"> 4. /number/invoices/<font color="red"> year </font> , method = GET </font><br>
    <font size="4"> &ensp; Mendapatkan jumlah tagihan pada <font color="red"> year </font><br>  
    <font size="4"> &ensp; </font><br>
    <font size="4"> 5. /customers/table/get , method = GET </font><br>
    <font size="4"> &ensp; Mendapatkan tabel customers dari database chinook  </font><br>
    <font size="4"> &ensp; </font><br>
    <font size="4"> 6. /employees/table/get , method = GET </font><br>
    <font size="4"> &ensp; Mendapatkan tabel employees dari database chinook  </font><br>
    <font size="4"> &ensp; </font><br>
    <font size="4"> 7. /tagihan/negara/ , method = GET </font><br>
    <font size="4"> &ensp; Mendapatkan tabel total tagihan per tahun untuk setiap negara, negara yang tidak memiliki tagihan di tahun tersebut akan diisi dengan 0  </font><br>
    <font size="4"> &ensp; </font><br>
</html>
'''


# mendapatkan 5 artis paling populer di suatu negara
@app.route('/top5artists/<country_name>', methods=['GET'])
def top5artists(country_name):
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/chinook.db")
    
    list_country = pd.read_sql_query(
        '''
        SELECT
        Country
        FROM
        customers
        ''',conn)['Country'].values
    
    if country_name in list_country:
    
        artist = pd.read_sql_query(
         '''
         SELECT 
         Country, artists.Name AS artist_name, COUNT(Country) as Total_Count
         FROM customers
         LEFT JOIN invoices USING(customerid)
         LEFT JOIN invoice_items USING(invoiceid)
         LEFT JOIN tracks USING(trackid) 
         LEFT JOIN albums USING(albumid)
         LEFT JOIN artists USING(artistid)
         GROUP BY Country, artist_name
         ORDER BY Country, Total_Count DESC
          ''',conn).groupby('Country').head()
        top_5 = artist[artist['Country'] == str(country_name)]['artist_name'].reset_index().drop(['index'],axis=1)
        return (top_5.to_json())
    
    else:
        return "Nama negara tidak ada di database"
     

# mendapatkan jumlah tagihan per tahun
@app.route('/number/invoices/<year>', methods=['GET'])
def numberinvoices(year):
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/chinook.db")
    
    if int(year) in list(range(2009,2014)):
        data = pd.read_sql_query(
            '''
            SELECT
            InvoiceDate
            FROM
            invoices
            ''',conn,parse_dates='InvoiceDate')
        data['Year'] = data['InvoiceDate'].dt.year
        data = data.groupby('Year')['Year'].count().reset_index(name = 'Number of Invoices').set_index('Year')
        return data.loc[int(year)].to_json()
    else:
        return "Data tidak tersedia di database"
        
        
# mendapatkan tabel customers
@app.route('/customers/table/get') 
def get_customers(): 
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/chinook.db")
    data = pd.read_sql_query(
     '''
     SELECT 
     *
     FROM customers
      ''',conn)
    return (data.to_json())

# mendapatkan tabel employees
@app.route('/employees/table/get') 
def get_employees(): 
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("data/chinook.db")
    data = pd.read_sql_query(
     '''
     SELECT 
     *
     FROM employees
      ''',conn)
    return (data.to_json())

# mendapatkan tabel total tagihan per tahun untuk setiap negara, negara yang tidak memiliki tagihan di tahun tersebut akan diisi dengan 0
@app.route('/tagihan/negara/')
def tagihan_per_tahun():
    import sqlite3
    import pandas as pd
    conn = sqlite3.connect("data/chinook.db")
    
    data = pd.read_sql_query(
    """
    SELECT 
    country, invoicedate, total
    FROM customers
    LEFT JOIN invoices ON customers.customerid = invoices.customerid
    """, conn, parse_dates='InvoiceDate')
    data['Year'] = data['InvoiceDate'].dt.to_period('Y')
    data = data.groupby(['Country', 'Year']).sum().unstack().unstack().unstack().fillna(0).droplevel(0)
    return data.to_json()

 
if __name__ == '__main__':
    app.run(debug=True, port=5000) 