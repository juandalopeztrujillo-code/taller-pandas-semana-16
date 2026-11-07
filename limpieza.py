import pandas as pd


def _quitar_espacios(df):
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()
    return df


def _revisar_textos(df, columnas, nombre):
    """Muestra los valores distintos de columnas de texto para detectar
    valores que deberían ser iguales pero están escritos diferente."""
    for col in columnas:
        print(f"[{nombre}] Valores de '{col}':")
        print(df[col].value_counts().to_string())


def limpiar_clientes(clientes):
    print("\n[clientes] Nulos por columna:")
    print(clientes.isnull().sum())
    print(f"[clientes] Filas duplicadas: {clientes.duplicated().sum()}")

    clientes = _quitar_espacios(clientes)

    # TODO 1: poner la columna "ciudad" en formato título (.str.title()).
    clientes["ciudad"] = clientes["ciudad"].str.title()

    # TODO 2: eliminar las filas duplicadas (.drop_duplicates()) y reiniciar el índice (.reset_index(drop=True)).
    clientes = clientes.drop_duplicates().reset_index(drop=True)

    _revisar_textos(clientes, ["ciudad", "segmento_cliente"], "clientes")

    print("\n[clientes] Después de limpiar:")
    print(f"[clientes] Nulos totales: {clientes.isnull().sum().sum()}")
    print(f"[clientes] Filas duplicadas: {clientes.duplicated().sum()}")
    print(f"[clientes] Filas tras limpieza: {len(clientes)}")
    return clientes


def limpiar_ventas(ventas):
    print("\n[ventas] Nulos por columna:")
    print(ventas.isnull().sum())
    print(f"[ventas] Filas duplicadas: {ventas.duplicated().sum()}")

    ventas = _quitar_espacios(ventas)

    # TODO 3: rellenar los nulos de "producto" con el texto "Sin especificar" (.fillna()).
    #         Pista: no uses dropna(); estarías borrando una venta con dinero real.
    ventas["producto"] = ventas["producto"].fillna("Sin especificar")

    # TODO 4: convertir "fecha_venta" a fecha con pd.to_datetime().
    #         Pista: el formato de los datos es AAAA-MM-DD.
    ventas["fecha_venta"] = pd.to_datetime(ventas["fecha_venta"], format="%Y-%m-%d", errors="coerce")
    fechas_invalidas = ventas["fecha_venta"].isnull().sum()
    print(f"[ventas] Fechas que no se pudieron convertir: {fechas_invalidas}")

    # TODO 5: eliminar las filas duplicadas y reiniciar el índice.
    ventas = ventas.drop_duplicates().reset_index(drop=True)

    _revisar_textos(ventas, ["categoria", "canal", "metodo_pago"], "ventas")

    print("\n[ventas] Después de limpiar:")
    print(ventas.isnull().sum())
    print(f"[ventas] Filas duplicadas: {ventas.duplicated().sum()}")
    print(f"[ventas] Tipo de 'fecha_venta': {ventas['fecha_venta'].dtype}")
    print("\n[ventas] .info() después de limpiar:")
    ventas.info()
    print(f"[ventas] Filas tras limpieza: {len(ventas)}")
    return ventas


def limpiar_datos(clientes, ventas):
    return limpiar_clientes(clientes), limpiar_ventas(ventas)
