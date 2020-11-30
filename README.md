# capstone-api
___
I have deployed a simple example on : https://algo-capstone-api.herokuapp.com
Here's the list of its endpoints: 
```
1. / , method = GET
  Menampilkan halaman pembuka
 
2. /docs , method = GET
  Menampilkan halaman dokumentasi
 
3. /top5artists/ country_name , method = GET
  Mendapatkan 5 artis paling populer di country_name
 
4. /number/invoices/ year , method = GET
  Mendapatkan jumlah tagihan pada year
 
5. /customers/table/get , method = GET
  Mendapatkan tabel customers dari database chinook
 
6. /employees/table/get , method = GET
  Mendapatkan tabel employees dari database chinook
 
7. /tagihan/negara/ , method = GET
  Mendapatkan tabel total tagihan per tahun untuk setiap negara, negara yang tidak memiliki tagihan di tahun tersebut akan diisi dengan 0
```

If you want to try it, you can access (copy-paste it) : 
- https://algo-capstone-api.herokuapp.com/
- https://algo-capstone-api.herokuapp.com/docs
- https://algo-capstone-api.herokuapp.com/tagihan/negara
- https://algo-capstone-api.herokuapp.com/top5artists/USA
- https://algo-capstone-api.herokuapp.com/employees/table/get
- https://algo-capstone-api.herokuapp.com/customers/table/get
