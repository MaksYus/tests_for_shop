from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class DB:
    def __init__(self, session=None):
        self.session = session
        self.connection = None

    def create_session(self):
        self.connection = create_engine(getenv("DATABASE_URL"))
        Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        return Session()

    def get(self, table_name: any, condition: dict, limit: int = 0, offset: int = 0):
        try:
            result = self.session.query(table_name).filter_by(
                **condition).limit(limit).offset(offset).all()
            items = []
            for row in result:
                tmp = {}
                for _row in vars(row):
                    if _row not in ['_sa_instance_state']:
                        tmp[_row] = row.__dict__[_row]
                items.append(tmp)
            return items
        except BaseException as e:
            print(e.args)
            return False

    def create(self, query_object: any):
        try:
            self.session.add(query_object)
            self.session.commit()
            return query_object
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def create_all(self, query_object: any):
        try:
            self.session.add_all(query_object)
            self.session.commit()
            ids = []
            for item in query_object:
                ids.append(item.id)
            return {'ids': ids}
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def update(self, table_name: any, condition: dict, update_value: dict):
        try:
            self.session.query(table_name).filter_by(
                **condition).update(update_value)
            self.session.commit()
            return 'Successful updated'
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def delete(self, table_name: any, condition: dict):
        try:
            self.session.query(table_name).filter_by(**condition).delete()
            self.session.commit()
            return 'Successful deleted'
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False

    def execute(self, query: str):
        """
            execute("SELECT * FROM user WHERE id=5")
            :param query: str
            :return:
        """
        try:
            result = self.session.execute(query)
            self.session.commit()
            items = []
            for row in result:
                items.append(row)
            return items
        except BaseException as e:
            print(e.args)
            self.session.rollback()
            return False
