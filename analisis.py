import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)


def analizar(df):
    print("\nInfo general:")
    df.info()
    print("\nEstadísticas numéricas:")
    print(df.describe())

    ingresos_por_categoria(df)
    canal_que_mas_vende(df)
    clientes_vip_vs_regular(df)
    metodo_pago_mas_usado(df)
    top5_clientes(df)
    ventas_por_mes(df)


def ingresos_por_categoria(df):
    """Pregunta 1: ¿Qué categoría genera más ingresos?

    Pista: df.groupby("categoria")["total"].sum().sort_values(ascending=False)
    """
    # TODO 8: calcular e imprimir los ingresos por categoría y la categoría que más ingresa.
    print("\n=== Pregunta 1: ingresos por categoría ===")
    ingresos = df.groupby("categoria")["total"].sum().sort_values(ascending=False)
    print(ingresos)

    # .iloc[0] toma la primera posición: como está ordenado de mayor a menor, es la mayor.
    mejor = ingresos.index[0]
    print(f"Respuesta: la categoría que más ingresa es {mejor} con ${ingresos.iloc[0]:,.0f}")


def canal_que_mas_vende(df):
    """Pregunta 2: ¿Qué canal vende más?

    Pista: agrupar por "canal" y usar .agg(ventas=("id_venta", "count"), ingresos=("total", "sum")).
    """
    # TODO 9: calcular e imprimir ventas e ingresos por canal.
    print("\n=== Pregunta 2: ventas por canal ===")
    resumen = df.groupby("canal").agg(
        ventas=("id_venta", "count"),
        ingresos=("total", "sum"),
    ).sort_values("ingresos", ascending=False)

    # concat: agregamos una fila TOTAL debajo de la tabla por canal.
    fila_total = pd.DataFrame(
        {"ventas": [resumen["ventas"].sum()], "ingresos": [resumen["ingresos"].sum()]},
        index=["TOTAL"],
    )
    print(pd.concat([resumen, fila_total]))

    canal_ingresos = resumen["ingresos"].idxmax()
    canal_ventas = resumen["ventas"].idxmax()
    print(
        f"Respuesta (criterio: ingresos): el canal que más vende es {canal_ingresos} "
        f"con ${resumen.loc[canal_ingresos, 'ingresos']:,.0f}"
    )
    print(
        f"Por cantidad de ventas también gana {canal_ventas} "
        f"con {resumen.loc[canal_ventas, 'ventas']} ventas"
    )


def clientes_vip_vs_regular(df):
    """Pregunta 3: ¿Los clientes VIP compran más que los Regulares?

    Pista: como hay más clientes Regular que VIP, compare promedios por cliente, no totales.
    Calcular: número de clientes (nunique), compras y gasto total por segmento,
    y luego dividir compras y gasto entre el número de clientes.
    """
    # TODO 10: calcular e imprimir compras y gasto promedio por cliente según segmento_cliente.
    print("\n=== Pregunta 3: VIP vs Regular ===")
    resumen = df.groupby("segmento_cliente").agg(
        clientes=("id_cliente", "nunique"),
        compras=("id_venta", "count"),
        gasto_total=("total", "sum"),
    )
    resumen["compras_por_cliente"] = (resumen["compras"] / resumen["clientes"]).round(2)
    resumen["gasto_por_cliente"] = (resumen["gasto_total"] / resumen["clientes"]).round(0)
    print(resumen)

    vip = resumen.loc["VIP"]
    regular = resumen.loc["Regular"]
    if vip["gasto_por_cliente"] > regular["gasto_por_cliente"]:
        conclusion = "Sí, los VIP gastan más por cliente que los Regulares"
    else:
        conclusion = "No, los VIP no gastan más por cliente que los Regulares"
    print(
        f"Respuesta (criterio: promedio por cliente): {conclusion} "
        f"(${vip['gasto_por_cliente']:,.0f} vs ${regular['gasto_por_cliente']:,.0f}; "
        f"compras por cliente {vip['compras_por_cliente']} vs {regular['compras_por_cliente']})"
    )


def metodo_pago_mas_usado(df):
    """Pregunta 4: ¿Qué método de pago es más usado?

    Pista: df["metodo_pago"].value_counts()
    """
    # TODO 11: calcular e imprimir el conteo por método de pago y cuál es el más usado.
    print("\n=== Pregunta 4: método de pago ===")
    conteo = df["metodo_pago"].value_counts()
    print(conteo)
    print(
        f"Respuesta (criterio: número de ventas): el método más usado es "
        f"{conteo.index[0]} con {conteo.iloc[0]} ventas"
    )


def top5_clientes(df):
    """Pregunta 5: ¿Top 5 clientes con más compras?

    Pista: agrupar por ["id_cliente", "nombre_cliente"], contar compras y sumar total,
    ordenar por compras (y por gasto como desempate) y tomar las primeras 5 con .head(5).
    """
    # TODO 12: calcular e imprimir el top 5.
    print("\n=== Pregunta 5: top 5 clientes ===")
    top = (
        df.groupby(["id_cliente", "nombre_cliente"])
        .agg(compras=("id_venta", "count"), gasto_total=("total", "sum"))
        .sort_values(["compras", "gasto_total"], ascending=[False, False])
        .head(5)
        .reset_index()
    )
    print(top)
    print("Respuesta (criterio: número de compras, desempate por gasto total):")
    for i in range(len(top)):
        fila = top.iloc[i]
        print(
            f"  {i + 1}. {fila['nombre_cliente']} - {fila['compras']} compras, "
            f"${fila['gasto_total']:,.0f}"
        )


def ventas_por_mes(df):
    """Bonus: ventas por mes usando to_period("M")."""
    print("\n=== Bonus: ventas por mes ===")
    df = df.copy()
    df["mes"] = df["fecha_venta"].dt.to_period("M")
    por_mes = df.groupby("mes").agg(ventas=("id_venta", "count"), ingresos=("total", "sum"))
    print(por_mes)
    mejor_mes = por_mes["ingresos"].idxmax()
    print(
        f"Respuesta: el mes que más vendió fue {mejor_mes} "
        f"con ${por_mes.loc[mejor_mes, 'ingresos']:,.0f}"
    )
