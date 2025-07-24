use erp;

-- Table: entreprises
CREATE TABLE entreprises (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table: clients
CREATE TABLE clients (
    id_client INT PRIMARY KEY,
    id_entreprise INT,
    name VARCHAR(255),
    address VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    client_type INT,
    FOREIGN KEY (id_entreprise) REFERENCES entreprises(id)
);

-- Table: sites
CREATE TABLE sites (
    id_site INT PRIMARY KEY,
    id_entreprise INT,
    id_client INT,
    site_name VARCHAR(255),
    address_site VARCHAR(255),
    site_type INT,
    FOREIGN KEY (id_entreprise) REFERENCES entreprises(id),
    FOREIGN KEY (id_client) REFERENCES clients(id_client)
);

-- Table: employees
CREATE TABLE employees (
    id_employee INT PRIMARY KEY,
    id_entreprise INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    address VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    contract_status VARCHAR(50),
    FOREIGN KEY (id_entreprise) REFERENCES entreprises(id)
);

-- Table: services
CREATE TABLE services (
    id_service INT PRIMARY KEY,
    id_entreprise INT,
    service_name VARCHAR(255),
    description TEXT,
    estimated_time TIME,
    FOREIGN KEY (id_entreprise) REFERENCES entreprises(id)
);

-- Table: contracts
CREATE TABLE contracts (
    id_contract INT PRIMARY KEY,
    id_entreprise INT,
    id_client INT,
    start_date DATE,
    end_date DATE,
    address_site VARCHAR(255),
    site_type INT,
    FOREIGN KEY (id_entreprise) REFERENCES entreprises(id),
    FOREIGN KEY (id_client) REFERENCES clients(id_client)
);

-- Table: planning
CREATE TABLE planning (
    id_intervention INT PRIMARY KEY,
    id_entreprise INT,
    id_site INT,
    id_service INT,
    planning_date DATE,
    start_time TIME,
    end_time TIME,
    id_employee INT,
    status VARCHAR(50),
    FOREIGN KEY (id_entreprise) REFERENCES entreprises(id),
    FOREIGN KEY (id_site) REFERENCES sites(id_site),
    FOREIGN KEY (id_service) REFERENCES services(id_service),
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee)
);
