from database.database import Base
from sqlalchemy import Column, String
import uuid
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship


class faculty(Base):
    __tablename__ = 'faculty'
    id = Column(String, primary_key=True)
    faculty_name = Column(String(100))
    faculty_phone = Column(String(15))
    email_addr = Column(String(100))
    dept_name = Column(String(100))
    is_grad = Column(Boolean)
    has_supervised_dla = Column(Boolean)
    projects = relationship("project", back_populates="fac")

    def __init__(self, f_name, f_phone, f_email_addr, f_dept_name, f_is_grad,f_has_supervised_dla ):
        self.id = str(uuid.uuid4())
        self.faculty_name = f_name
        self.faculty_phone = f_phone
        self.email_addr = f_email_addr
        self.dept_name = f_dept_name
        self.is_grad = f_is_grad
        self.has_supervised_dla = f_has_supervised_dla


    def __repr__(self):
        return self.faculty_name

    def get_id(self):
        return self.id