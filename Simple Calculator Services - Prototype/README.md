# Simple Calculator Services

Simple Calculator Services adalah aplikasi kalkulator sederhana yang digunakan untuk menghitung / melakukan kalkulasi yang cukup berat. Oleh karena itu aplikasi ini dibuat secara asynchronous dengan memanfaatkan teknologi celery.

Spesifikasi Service:

- GET /api/prime/<index> : mencari bilangan prima yang ke <index>

Request Body: None

Response Body:
{
   “result”: <int>
}

- GET /api/prime/palindrome/<index> : mencari bilangan prima palindrome ke <index>

Request Body: None

Response Body:

{
   “result”: <int>
}

