from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_set import Session
from schemas import UserModel, UpdateUser, ResponseMesageAllUsers, ResponseMessage
import models
import os

app = FastAPI()


@app.get('/api/v1/users', response_model=ResponseMesageAllUsers, status_code=200)
def get_all_users():
    with Session() as db_session:
        users = db_session.query(models.User).all()
        return {'success': True, 'message': 'All users retrieved from the database!', 'data': users}


@app.get('/api/v1/users/{passed_id}', response_model=ResponseMessage, status_code=200)
def get_user_by_id(passed_id: int):
    with Session() as db_session:
        user = db_session.query(models.User).filter_by(id=passed_id).first()
        if user:
            return {'success': True, 'message': f'User with the id: {passed_id} successfully retrieved from the database!', 'data': user}
        raise HTTPException(status_code=404, detail=f'User with id {passed_id} not found.')


@app.post('/api/v1/users', response_model=ResponseMessage, status_code=201)
def create_user(userBody: UserModel):
    with Session() as db_session:
        check_email = db_session.query(models.User).filter_by(email=userBody.email).first()
        if check_email:
            raise HTTPException(status_code=400, detail=f'Email: {userBody.email} already exists in the database!')

        new_user = models.User(
            firstname=userBody.firstname,
            lastname=userBody.lastname,
            email=userBody.email,
            country=userBody.country,
            city=userBody.city
        )
        db_session.add(new_user)
        try:
            db_session.commit()
            db_session.refresh(new_user)  # Обновление объекта из БД
            return {'success': True, 'message': 'User successfully created!', 'data': new_user}
        except Exception as e:
            db_session.rollback()
            raise HTTPException(status_code=500, detail=f'Error creating user: {str(e)}')


@app.put('/api/v1/users/{passed_id}', response_model=ResponseMessage, status_code=200)
def update_user(passed_id: int, userBody: UpdateUser):
    with Session() as db_session:
        user = db_session.query(models.User).filter_by(id=passed_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f'User with id {passed_id} not found.')

        if userBody.firstname:
            user.firstname = userBody.firstname
        if userBody.lastname:
            user.lastname = userBody.lastname
        if userBody.email:
            user.email = userBody.email
        if userBody.country:
            user.country = userBody.country
        if userBody.city:
            user.city = userBody.city
        try:
            db_session.commit()
            db_session.refresh(user)  # Обновление объекта из БД
            return {'success': True, 'message': f'User with the id: {passed_id} successfully updated!', 'data': user}
        except Exception as e:
            db_session.rollback()
            raise HTTPException(status_code=500, detail=f'Error updating user: {str(e)}')


@app.delete('/api/v1/users/{passed_id}', response_model=ResponseMessage, status_code=200)
def delete_user(passed_id: int):
    with Session() as db_session:
        user = db_session.query(models.User).filter_by(id=passed_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f'User with id {passed_id} not found.')

        db_session.delete(user)
        try:
            db_session.commit()
            return {'success': True, 'message': f'User with the id: {passed_id} successfully deleted from the database!', 'data': user}
        except Exception as e:
            db_session.rollback()
            raise HTTPException(status_code=500, detail=f'Error deleting user: {str(e)}')
        

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены или укажите конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)