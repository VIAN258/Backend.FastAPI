from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(tags=["users"])

# Inicia el server: uvicorn users:app --reload

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name= "Angel", surname= "Morales", url= "https://moure.dev", age= 35 ),
         User(id=2, name= "Ana", surname= "Blanco", url= "https://moure.com", age= 38),
         User(id=3, name= "Lenis", surname= "Lopez", url= "https://haakon.com", age= 35)]


@router.get("/usersjson")
async def  usersjson():
    return [{ "name":"Angel", "surname": "Morales", "url": "https://moure.dev", "age": 35},
            { "name":"Ana", "surname": "Blanco", "url": "https://moure.com", "age": 33},
            { "name":"Lenis", "surname": "Lopez", "url": "https://haakon.com","age": 39}]



@router.get("/users")
async def  users():
    return users_list


# Path

@router.get("/user/{id}")
async def  user(id: int):
    return search_user(id)
    

# Query

@router.get("/userquery/")
async def  user(id: int):
    return search_user(id)
   
    
@router.post("/user/", response_model=User, status_code= 201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail= "El usuario ya existe")
        
    else:
        users_list.append(user)
        return user
        


@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"Error":"No se ha actualizado el usuario"}
    else:
        return user


@router.delete("/user/{id}")
async def  user(id: int):
     
     foud = False

     for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

     if not found:
        return {"Error":"No se ha eliminado el usuario"}
            



def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"No se ha encontrado el usuario"}
    






