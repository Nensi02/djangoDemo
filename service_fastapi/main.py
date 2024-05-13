from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException # type: ignore
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

DATABASE_URL = "postgresql://postgres:nensi@localhost/justdial_service"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

metadata = MetaData()
metadata.reflect(bind=engine)
service_table = metadata.tables['service_app_services']


class Service(BaseModel):
    service_name: Optional[str] = None
    description: Optional[str] = None
    status : Optional[bool] = None

@app.post('/add_service')
async def post_service(serivce: Service, db: Session = Depends(get_db)):
    new_record = service_table.insert().values(
        name=serivce.service_name,
        description=serivce.description,
        status=serivce.status,
        created_date=datetime.utcnow(),
        modified_date=datetime.utcnow()
    )
    try:
        db.execute(new_record)
        db.commit()
        return {"message": "Data inserted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

@app.get('/list_service')
async def get_service(db: Session = Depends(get_db)):
    try:
        list_services = db.query(service_table).filter(service_table.c.status == True).all()
        serialized_services = []
        for service in list_services:
            serialized_service = {
                "id": service.id,
                "service_name": service.name,
                "description": service.description,
                "status": service.status,
                "create date": service.created_date,
                "modified date": service.modified_date
            }
            serialized_services.append(serialized_service)
        return serialized_services
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occured: {str(e)}")

@app.get('/list_service/{service_id}')
async def get_service(service_id: int, db: Session = Depends(get_db)):
    try:
        list_services = db.query(service_table).filter(service_table.c.id == service_id, service_table.c.status == True).all()
        serialized_services = []
        for service in list_services:
            serialized_service = {
                "id": service.id,
                "service_name": service.name,
                "description": service.description,
                "status": service.status,
                "create date": service.created_date,
                "modified date": service.modified_date
            }
            serialized_services.append(serialized_service)
        return serialized_services
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occured: {str(e)}")

@app.put('/update_service/{service_id}')
async def get_service(service_id: int,  serivce: Service, db: Session = Depends(get_db)):
    updated_values = {}
    if serivce.service_name is not None:
        updated_values['name'] = serivce.service_name
    if serivce.description is not None:
        updated_values['description'] = serivce.description
    if serivce.status is not None:
        updated_values['status'] = serivce.status
    updated_values['modified_date'] = datetime.utcnow()

    try:
        # Update the specified fields
        db.execute(
            service_table.update()
            .where(service_table.c.id == service_id)
            .values(updated_values)
        )
        db.commit()
        return {"message": "Service updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

@app.delete('/delete_service/{service_id}')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    delete_statement = service_table.delete().where(service_table.c.id == service_id, service_table.c.status == True)
    try:
        result = db.execute(delete_statement)
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Service not found")
        return {"message": "Service deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")