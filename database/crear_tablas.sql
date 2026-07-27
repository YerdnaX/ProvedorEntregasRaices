USE master;
GO

IF DB_ID('tiusr15pl_ProvedoresRaicesBosque') IS NULL
BEGIN
    CREATE DATABASE tiusr15pl_ProvedoresRaicesBosque;
END;
GO

USE tiusr15pl_ProvedoresRaicesBosque;
GO

IF OBJECT_ID('ProvedorEntregas_Entregas', 'U') IS NULL
BEGIN
    CREATE TABLE ProvedorEntregas_Entregas (
        IdEntregaProvedor INT IDENTITY(1,1) PRIMARY KEY,
        NumeroOrden       INT NOT NULL UNIQUE,
        TrackingNumber    VARCHAR(50) NOT NULL UNIQUE,
        DireccionEntrega  VARCHAR(300) NOT NULL,
        Estado            VARCHAR(50) NOT NULL,
        FechaCreacion     DATETIME NOT NULL DEFAULT GETDATE()
    );
END;
GO
