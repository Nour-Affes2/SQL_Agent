import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Entreprise(Base):
    __tablename__ = "entreprises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    clients = relationship("Client", back_populates="entreprise")
    sites = relationship("Site", back_populates="entreprise")
    contracts = relationship("Contract", back_populates="entreprise")
    services = relationship("Service", back_populates="entreprise")
    employees = relationship("Employee", back_populates="entreprise")
    planning = relationship("Planning", back_populates="entreprise")

    def __repr__(self):
        return f"<Entreprise(id={self.id}, name='{self.name}')>"

class Client(Base):
    __tablename__ = "clients"

    id_entreprise = Column(Integer, ForeignKey("entreprises.id"))
    id_client = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    client_type = Column(Integer, index=True)

    entreprise = relationship("Entreprise", back_populates="clients")
    sites = relationship("Site", back_populates="client")
    contracts = relationship("Contract", back_populates="client")

    def __repr__(self):
        return f"<Client(id_client={self.id_client}, name='{self.name}')>"

class Site(Base):
    __tablename__ = "sites"

    id_entreprise = Column(Integer, ForeignKey("entreprises.id"))
    id_site = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey("clients.id_client"), index=True)
    site_name = Column(String, index=True)
    address_site = Column(String)
    site_type = Column(Integer, index=True)

    entreprise = relationship("Entreprise", back_populates="sites")
    client = relationship("Client", back_populates="sites")
    planning = relationship("Planning", back_populates="site")

    def __repr__(self):
        return f"<Site(id_site={self.id_site}, site_name='{self.site_name}')>"

class Contract(Base):
    __tablename__ = "contracts"

    id_entreprise = Column(Integer, ForeignKey("entreprises.id"))
    id_contract = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey("clients.id_client"), index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    address_site = Column(String)
    site_type = Column(Integer, index=True)

    entreprise = relationship("Entreprise", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")

    def __repr__(self):
        return f"<Contract(id_contract={self.id_contract}, start_date={self.start_date})>"

class Service(Base):
    __tablename__ = "services"

    id_entreprise = Column(Integer, ForeignKey("entreprises.id"))
    id_service = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    description = Column(String)
    estimated_time = Column(Time)

    entreprise = relationship("Entreprise", back_populates="services")
    planning = relationship("Planning", back_populates="service")

    def __repr__(self):
        return f"<Service(id_service={self.id_service}, name='{self.service_name}')>"

class Employee(Base):
    __tablename__ = "employees"

    id_entreprise = Column(Integer, ForeignKey("entreprises.id"))
    id_employee = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    address = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    contract_status = Column(String)

    entreprise = relationship("Entreprise", back_populates="employees")
    planning = relationship("Planning", back_populates="employee")

    def __repr__(self):
        return f"<Employee(id_employee={self.id_employee}, name='{self.name}')>"

class Planning(Base):
    __tablename__ = "planning"

    id_entreprise = Column(Integer, ForeignKey("entreprises.id"))
    id_intervention = Column(Integer, primary_key=True, index=True)
    id_site = Column(Integer, ForeignKey("sites.id_site"))
    id_service = Column(Integer, ForeignKey("services.id_service"))
    planning_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    id_employee = Column(Integer, ForeignKey("employees.id_employee"))
    status = Column(String)

    entreprise = relationship("Entreprise", back_populates="planning")
    site = relationship("Site", back_populates="planning")
    service = relationship("Service", back_populates="planning")
    employee = relationship("Employee", back_populates="planning")

    def __repr__(self):
        return f"<Planning(id_intervention={self.id_intervention}, date={self.planning_date})>"

# --- Database Setup ---
DATABASE_URL = "sqlite:///./test.db"  # Change to your actual DB URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

# --- Mock Data Insertion Function ---
def init_db():
    from datetime import date, time

    session = SessionLocal()

    entreprises_data = [
        Entreprise(name="ProNet Solutions"),
        Entreprise(name="EcoClean France"),
        Entreprise(name="Horizon Nettoyage ERP")
    ]

    session.add_all(entreprises_data)
    session.commit()

    for ent in entreprises_data:
        clients = [
            Client(id_entreprise=ent.id, name="SNCF Paris", address="10 Rue de Lyon, Paris", email=f"sncf_{ent.id}@client.fr", phone=f"060100{ent.id}01", client_type=1),
            Client(id_entreprise=ent.id, name="Mairie de Lyon", address="1 Place de la Comédie, Lyon", email=f"lyon_{ent.id}@client.fr", phone=f"060100{ent.id}02", client_type=2)
        ]
        session.add_all(clients)
        session.commit()

        sites = [
            Site(id_entreprise=ent.id, id_client=clients[0].id_client, site_name="Gare de Lyon", address_site="Paris Gare de Lyon", site_type=1),
            Site(id_entreprise=ent.id, id_client=clients[1].id_client, site_name="Hôtel de Ville", address_site="Lyon Centre", site_type=2)
        ]
        session.add_all(sites)
        session.commit()

        services = [
            Service(id_entreprise=ent.id, service_name="Nettoyage de bureaux", description="Nettoyage quotidien des bureaux", estimated_time=time(2, 0)),
            Service(id_entreprise=ent.id, service_name="Nettoyage de vitres", description="Nettoyage des vitres en hauteur", estimated_time=time(1, 30))
        ]
        session.add_all(services)
        session.commit()

        employees = [
            Employee(id_entreprise=ent.id, name="Jean", surname="Martin", address="3 Rue Victor Hugo, Paris", email=f"jean_{ent.id}@pro.fr", phone=f"060200{ent.id}01", contract_status="CDI"),
            Employee(id_entreprise=ent.id, name="Claire", surname="Dupont", address="12 Rue de Marseille, Lyon", email=f"claire_{ent.id}@pro.fr", phone=f"060200{ent.id}02", contract_status="CDD")
        ]
        session.add_all(employees)
        session.commit()

        contracts = [
            Contract(
                id_entreprise=ent.id,
                id_client=clients[0].id_client,
                start_date=date(2024, 1, 1),
                end_date=date(2025, 1, 1),
                address_site=sites[0].address_site,
                site_type=sites[0].site_type
            ),
            Contract(
                id_entreprise=ent.id,
                id_client=clients[1].id_client,
                start_date=date(2024, 6, 1),
                end_date=date(2025, 6, 1),
                address_site=sites[1].address_site,
                site_type=sites[1].site_type
            )
        ]
        session.add_all(contracts)
        session.commit()

        planning_entries = [
            Planning(
                id_entreprise=ent.id,
                id_site=sites[0].id_site,
                id_service=services[0].id_service,
                planning_date=date(2025, 7, 24),
                start_time=time(8, 0),
                end_time=time(10, 0),
                id_employee=employees[0].id_employee,
                status="Planifié"
            ),
            Planning(
                id_entreprise=ent.id,
                id_site=sites[1].id_site,
                id_service=services[1].id_service,
                planning_date=date(2025, 7, 25),
                start_time=time(14, 0),
                end_time=time(15, 30),
                id_employee=employees[1].id_employee,
                status="En attente"
            )
        ]
        session.add_all(planning_entries)
        session.commit()

    session.close()
    print("✅ Mock data inserted successfully.")

# --- Main entry point ---
if __name__ == "__main__":
    init_db()


