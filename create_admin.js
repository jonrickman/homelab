use admin;
db.createUser(
   {
    user: "admin",
    pwd: "pass",
     roles:
       [
         { role: "readWrite", db: "admin" },
         "clusterAdmin"
       ]
   }
)