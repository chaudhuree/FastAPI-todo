```
docker compose up -d
```

[Open Database UI](loacalhost:5050)

<details>
  <summary>login credentials</summary>
  
  email: admin@test.com </br>
  password: admin
</details>

---

- go to server tab then create server using this data.

#### Add server:

```
Server Name: postgres-db
Host: postgres
Port: 5432
Database: fastapi_db
User: admin
Password: admin
```

#### Entry point - db.py
- here we need to create a session. for this we need engine. and we can create engine by the dtabase url.
- using this session we can inititate db like get_db() function is doing so.
- we need this engine for further usage

- then we will go to base.py and create a Base declarative

- now to create tables we need to do a method call `Base.metadata.create_all(bind=engine)`

- then we can call the get_db() and then do query , commit and refresh.



#### Fast api flow
```
Request
   ↓
Pydantic validation
   ↓
Dependency injection (db session)
   ↓
Create SQLAlchemy object
   ↓
Add to session
   ↓
Commit to PostgreSQL
   ↓
Refresh object
   ↓
```