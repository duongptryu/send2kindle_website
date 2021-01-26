from db.db import Base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

Subdomain_Port = Table('subdomain_port', Base.metadata,
    Column('sub_id', Integer, ForeignKey('subdomains.id')),
    Column('port_id', Integer, ForeignKey('ports.id'))
)

Domain_Port = Table('domain_port', Base.metadata,
    Column('domain_id', Integer, ForeignKey('domains.id')),
    Column('port_id', Integer, ForeignKey('ports.id')),
)


User_Domain = Table('user_domain', Base.metadata,
    Column('domain_id', Integer, ForeignKey('domains.id')),
    Column("user_id", Integer, ForeignKey('users.id'))
)


# class Subdomain_Port(Base):
#     __tablename__ = "subdomain_port"
#     sub_id = Column(Integer, ForeignKey('subdomains.id'), primary_key=True)
#     port_id = Column(Integer, ForeignKey('ports.id'), primary_key=True)

#     subdomains = relationship("Subdomain", back_populates="ports")
#     ports = relationship("Port", back_populates="subdomains")


# class Domain_Port(Base):
#     __tablename__ = "domain_port"
#     domain_id = Column(Integer, ForeignKey('domains.id'), primary_key=True)
#     port_id = Column(Integer, ForeignKey('ports.id'), primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

#     domains = relationship("Domain", back_populates="ports")
#     ports = relationship("Port", back_populates="domains")

