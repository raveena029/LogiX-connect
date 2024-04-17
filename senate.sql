+----------+---------------+--------------+------------------------+------+
| cr_netID | name          | phone_no     | major                  | year |
+----------+---------------+--------------+------------------------+------+
| ag012    | Anjali Gupta  | 444-789-1234 | Biology                | 2026 |
| as789    | Amit Singh    | 555-123-4567 | Physics                | 2025 |
| dv901    | Deepak Verma  | 111-222-3333 | Economics              | 2026 |
| nm678    | Neha Mishra   | 333-222-1111 | Chemistry              | 2025 |
| pp456    | Priya Patel   | 987-654-3210 | Electrical Engineering | 2025 |
| rp567    | Rajesh Patel  | 666-555-4444 | History                | 2026 |
| rs123    | Rahul Sharma  | 123-456-7890 | Computer Science       | 2025 |
| sg890    | Shivani Gupta | 123-987-4560 | Psychology             | 2026 |
| sr234    | Sneha Reddy   | 999-888-7777 | Political Science      | 2025 |
| td777    | Random Person | 777-777-7777 | Mathematics            | 2025 |
| vk345    | Vivek Kumar   | 777-888-9999 | Mathematics            | 2026 |
+----------+---------------+--------------+------------------------+------+
mysql> insert into senate values("vs279","Vanalee Saharia",9835474849,"English",2026);
ERROR 1264 (22003): Out of range value for column 'Phone_no' at row 1
mysql> insert into senate values("vs279","Vanalee Saharia",983547484,"English",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("vs279","Vanalee Saharia",983547484,"English",2026);
ERROR 1062 (23000): Duplicate entry 'vs279' for key 'senate.PRIMARY'
mysql> insert into senate values("eb949","Easwar Balakrishnan",894747484,"History",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("pk749","Pratyush Kamal",987578484,"Computer Science",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("jk585","Jaideep K",789978484,"Computer Science",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("ab669","Aarushi Bansal",674848484,"Biotechnology",2025);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("kk392","Kavyaa Kannan",987689484,"Economics",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("ag242","Amey Gautam",999878299,"Computer Science",2026);
Query OK, 1 row affected (0.01 sec)

mysql> update senate set year=2026 where name="Amey Gautam";
Query OK, 0 rows affected (0.01 sec)
Rows matched: 1  Changed: 0  Warnings: 0
 insert into senate values("as343","Anukriti Singh",987699484,"IR",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("ac510","Ashmita mittal",999699484,"Physics",2025);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("rn389","Rithvikha Tk Nair",767699484,"Biotech",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("pu546","Piyu Upadhyaya",989999675,"Biotech
",2026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("hs890","Harsh Srivastava",897699675,"Mathe
matics",2027);

insert into senate values("as765","Abhay Singh",887609689,"Physics",2
026);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("as765","Abhay Singh",964709689,"CSE",2024)
;
ERROR 1062 (23000): Duplicate entry 'as765' for key 'senate.PRIMARY'
mysql> insert into senate values("as760","Abhay Singh",964709689,"CSE",2024)
;
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("bk887","bhavye kohli",789678689,"ECE",2026
);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("rm657","Renee Mohan",980778699,"ECE",2026)
;
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("ds997","Devesh Sharma",789078540,"ECE",202
5);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("pg865","Priyanshu Goyal",908889078,"Chemic
al Engineering",2027);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("vp675","Vedant Patil",808989888,"Chemistry
",2024);
Query OK, 1 row affected (0.01 sec)

mysql> insert into senate values("kj879","Kartik Jalluri",899976589,"Eco-fin
",2027);
Query OK, 1 row affected (0.01 sec)
