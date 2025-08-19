from sqlalchemy.orm import Session
from sqlalchemy import desc
from octopus_exercise.db.models import LocationTableModel, OperatorTableModel


def find_all_locations(
    db: Session,
    country: str | None = None,
    operator: str | None = None,
    order_by_last_updated: bool | None = None,
    descending: bool | None = None,
):
    query = db.query(LocationTableModel)

    # TODO extract this a write a test for it 
    if operator is not None:
        query = query.join(LocationTableModel.operator).filter(OperatorTableModel.name == operator)

    if country is not None:
        query = query.filter(LocationTableModel.country == country)

    if order_by_last_updated:
        if descending:
            query = query.order_by(desc(LocationTableModel.last_updated))
        else:
            query = query.order_by(LocationTableModel.last_updated)

    return query.all()

def find_specific_location(db: Session, location_reference: str):
    return db.query(LocationTableModel)\
         .filter(LocationTableModel.reference == location_reference)\
         .first()
