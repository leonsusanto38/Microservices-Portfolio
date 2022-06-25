# Student’s Research Paper Storage

Student’s Research Paper Storage adalah layanan dimana mahasiswa dapat menambahkan  / menyimpan paper pada service yang disediakan. Proses ini dilakukan dengan fungsi - fungsi:

- Login: masuk kedalam sistem dan menambahkan session. Login menggunakan email dan password.

- Logout: menghapus session

- Register User: menambahkan user kedalam sistem, proses ini akan menambahkan data user (nrp, nama, email, password) pada service.
 
- Upload Paper: proses melakukan upload paper dalam bentuk pdf yang dimana data judul dan abstract juga harus dimasukan, Upload akan memberikan info user mana yang memiliki paper tersebut. Proses ini memerlukan login

- Download Paper: proses yang dilakukan untuk mendownload paper, yang boleh melakukan download adalah mahasiswa yang merupakan pemilik file / dosen.
 
- Search: proses ini akan melakukan searching berdasarkan judul / abstract / author.  Untuk kasus ini anda dapat melakukan dengan memanfaatkan teknologi Elastic Search.