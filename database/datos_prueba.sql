USE tiusr15pl_ProvedoresRaicesBosque;
GO

IF NOT EXISTS (SELECT 1 FROM ProvedorEntregas_Entregas WHERE NumeroOrden = 1001)
BEGIN
    INSERT INTO ProvedorEntregas_Entregas (
        NumeroOrden,
        TrackingNumber,
        DireccionEntrega,
        Estado
    )
    VALUES (
        1001,
        'RBX-20260727-DEMO01',
        'Cartago, Costa Rica',
        'Registrada'
    );
END;
GO
