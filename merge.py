from pathlib import Path

PROCESSED = Path(__file__).parent / "Data" / "processed"


def validar_premerge(clientes, ventas):
    """Revisa que el merge se pueda hacer. Devuelve True si todo está bien, False si no.

    Revisar:
    - Que exista la columna "id_cliente" en los dos dataframes.
    - Que "id_cliente" no esté repetido en clientes.
    - Que "id_cliente" tenga el mismo tipo en los dos dataframes.
    - Cuántas ventas no tienen cliente asociado (esto solo se informa, no falla).
    """
    # TODO 6: escribir las validaciones y devolver True o False.
    print("\n=== Validación antes del merge ===")

    if "id_cliente" not in clientes.columns or "id_cliente" not in ventas.columns:
        print("ERROR: falta la columna 'id_cliente' en alguna de las tablas.")
        return False
    print("OK: la columna 'id_cliente' existe en clientes y en ventas.")

    repetidos = clientes["id_cliente"].duplicated().sum()
    if repetidos > 0:
        print(f"ERROR: hay {repetidos} id_cliente repetidos en clientes.")
        return False
    print("OK: no hay id_cliente repetidos en clientes.")

    tipo_clientes = clientes["id_cliente"].dtype
    tipo_ventas = ventas["id_cliente"].dtype
    if tipo_clientes != tipo_ventas:
        print(f"ERROR: tipos distintos (clientes: {tipo_clientes}, ventas: {tipo_ventas}).")
        return False
    print(f"OK: id_cliente tiene el mismo tipo en ambas tablas ({tipo_clientes}).")

    sin_cliente = (~ventas["id_cliente"].isin(clientes["id_cliente"])).sum()
    print(f"Info: ventas sin cliente asociado: {sin_cliente}")

    return True


def unir(clientes, ventas):
    """Une ventas con clientes usando "id_cliente" y guarda el resultado en Data/processed/merge.csv.

    Pistas:
    - Usar pd.merge(...) o ventas.merge(...).
    - Usar how="left" para no perder ventas.
    - Usar validate="m:1" para confirmar que cada venta tiene un solo cliente.
    - Guardar con df.to_csv(...) en PROCESSED / "merge.csv".
    """
    # TODO 7: validar con validar_premerge(), hacer el merge, guardar el CSV y devolver el dataframe.
    if not validar_premerge(clientes, ventas):
        print("No se hizo el merge porque la validación falló.")
        return None

    df = ventas.merge(clientes, on="id_cliente", how="left", validate="m:1")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "merge.csv", index=False)

    print("\n=== Resultado del merge ===")
    print(f"Ventas: {ventas.shape} | Clientes: {clientes.shape} | Merge: {df.shape}")
    print(f"Filas: {len(df)} (igual a ventas: {len(df) == len(ventas)})")
    print(
        f"Columnas: {ventas.shape[1]} + {clientes.shape[1]} - 1 (id_cliente en común) "
        f"= {df.shape[1]}"
    )
    print(df.head())
    print(f"Guardado en: {PROCESSED / 'merge.csv'}")
    return df
