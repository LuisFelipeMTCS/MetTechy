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
    uf TEXT NOT NULL,
    entidade TEXT,
    resumo TEXT,
    temp_max TEXT,
    temp_min TEXT,
    int_vento TEXT,
    umidade_max TEXT,
    umidade_min TEXT,
    temp_max_tende TEXT,
    periodo TEXT,
    ID_Cidade INTEGER REFERENCES Cidade(ID_Cidade) ON DELETE CASCADE
);



