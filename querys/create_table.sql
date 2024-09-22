CREATE TABLE Cidade (
    ID_Cidade SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Estado VARCHAR(50),
    Latitude DECIMAL(9, 6),
    Longitude DECIMAL(9, 6)
);

CREATE TABLE Usuario (
    ID_Usuario SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefone VARCHAR(15),
    ID_Cidade INTEGER REFERENCES Cidade(ID_Cidade) ON DELETE CASCADE
);


CREATE TABLE Leitura_Climatica (
    ID_Leitura SERIAL PRIMARY KEY,
    Data_Hora TIMESTAMPTZ NOT NULL,
    Precipitação DECIMAL(5, 2),
    Temperatura DECIMAL(5, 2),
    Umidade DECIMAL(5, 2),
    ID_Cidade INTEGER REFERENCES Cidade(ID_Cidade) ON DELETE CASCADE
);


CREATE TABLE Alerta_Climatico (
    ID_Alerta SERIAL PRIMARY KEY,
    Data_Hora_Emissão TIMESTAMPTZ NOT NULL,
    Descrição TEXT NOT NULL,
    Nível_Alerta VARCHAR(50),
    ID_Cidade INTEGER REFERENCES Cidade(ID_Cidade) ON DELETE CASCADE,
    ID_Usuario INTEGER REFERENCES Usuario(ID_Usuario) ON DELETE SET NULL
);