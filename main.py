import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CARGAR DATOS
data = pd.read_csv('Renewable_Energy.csv')

# Dividir el dataset en dos según la columna 'Indicator'
grouped_data = data.groupby('Indicator')

# Crear dos datasets separados
generation = grouped_data.get_group('Electricity Generation')
capacity = grouped_data.get_group('Electricity Installed Capacity')

# Eliminar las columnas especificadas de ambos datasets
columns_to_drop = ['Source', 'CTS_Name', 'CTS_Code', 'CTS_Full_Descriptor', 'Indicator']
generation.drop(columns=columns_to_drop, inplace=True)
capacity.drop(columns=columns_to_drop, inplace=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Título y descripción
    st.title('Energías Renovables y Combustibles Fósiles')
    st.markdown(
        """
        Este proyecto analiza la generación y distribución de energía renovable y no renovable
        en distintos territorios y tecnologías.
        """
    )

with col2:
    # Imagen en la segunda columna
    st.image("imagen_introduccion.webp", width=200, caption="Energía sostenible")

# Diferentes páginas
opcion = st.sidebar.radio("Selecciona un tipo de visualización:", ["Energía por territorio", "Comparativas", "Energía en la UE"])

# GRAFICOS MARIA
if opcion == "Comparativas":
    # Seleccionar un rango de años
    years = st.slider('Años', 2000, 2022, (2000, 2022))

    # Crear dos columnas para la selección de tipo de energía y países
    col1, col2 = st.columns(2)

    with col1:
        # Seleccionar tipo de energía usando segmented control
        energy_type_options = ['Renovable', 'No Renovable', 'Total']
        selected_energy_type = st.segmented_control(
            'Seleccionar Tipo de Energía',
            options=energy_type_options,
            default='Total'
        )

    with col2:
        # Seleccionar países usando multiselect
        country_options = generation['Country'].unique()
        selected_countries = st.multiselect(
            'Seleccionar Países',
            options=country_options,
            default=['Spain', 'France', 'Portugal']
        )

    # Filtrar las columnas por el rango de años seleccionado
    selected_columns = [f'F{year}' for year in range(years[0], years[1] + 1)]

    # Filtrar por tipo de energía
    if selected_energy_type == 'Renovable':
        filtered_data = generation[generation['Energy_Type'] == 'Total Renewable']
    elif selected_energy_type == 'No Renovable':
        filtered_data = generation[generation['Energy_Type'] == 'Total Non-Renewable']
    else:
        filtered_data = generation

    # Crear el gráfico de líneas
    st.subheader(f'Evolución de la Energía {selected_energy_type} Generada ({years[0]}-{years[1]})')

    fig, ax = plt.subplots(figsize=(12, 8))

    # Graficar una línea para cada país seleccionado
    for country in selected_countries:
        country_data = filtered_data[filtered_data['Country'] == country]
        aggregated_data = country_data[selected_columns].sum().T
        years_index = [int(col[1:]) for col in aggregated_data.index]  # Convertir nombres de columnas a años
        ax.plot(
            years_index,
            aggregated_data.values,
            marker='o',
            label=f"{country}"
        )

    # Personalizar el gráfico
    ax.set_title(f"Evolución de la Energía {selected_energy_type} Generada ({years[0]}-{years[1]})", fontsize=14)
    ax.set_xlabel("Año", fontsize=12)
    ax.set_ylabel("Cantidad de Energía (GWh)", fontsize=12)
    ax.legend(title="País")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


#GRAFICO CARMEN

if opcion == 'Energía por territorio':

    # Crear un desplegable en Streamlit para seleccionar el país
    st.subheader('Generación de energía por territorio según el tipo de energía')
    paises = data['Country'].unique().tolist()
    pais_seleccionado = st.selectbox('Selecciona un territorio', paises)

    # Filtrar los datos para el país seleccionado
    datos_pais = generation[generation['Country'] == pais_seleccionado]

    # Seleccionar el rango de años
    year_range = st.slider('Selecciona el rango de años', 2000, 2022, (2000, 2022))
    years_selected = [f'F{year}' for year in range(year_range[0], year_range[1] + 1)]
    years_label = [year for year in range(year_range[0], year_range[1] + 1)]

    # Seleccionar la tecnologia
    tech = ["Todas"] + list(datos_pais['Technology'].dropna().unique())
    tech_selected = st.selectbox('Seleccionar tipo de energía', options=tech)

    # Filtrar los datos para la tecnología seleccionada
    if tech_selected != "Todas":
        datos_pais_tech = datos_pais[datos_pais['Technology'] == tech_selected][years_selected]
        # Generar gráfico de barras para la tecnología seleccionada
        st.write(f'Generación de Energía en {pais_seleccionado} - {tech_selected}')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=datos_pais_tech, color='olivedrab')
        ax.set_ylim(datos_pais_tech.min().min() * 0.9, datos_pais_tech.max().max() * 1.1)
        ax.set_xticklabels(years_label, rotation=45)
        st.pyplot(fig)
    
    
    else: 
        st.write(f'Generación de Energía en {pais_seleccionado} - Todas las tecnologías')
        datos_pais_tech = datos_pais[years_selected].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=datos_pais_tech, color='olivedrab')
        ax.set_ylim(datos_pais_tech.min().min() * 0.9, datos_pais_tech.max().max() * 1.1)
        ax.set_xticklabels(years_label, rotation=45)
        st.pyplot(fig)
    
    # Grafico total

    # Calcular el total de generación de energía para el rango de años seleccionado
    datos_pais['Total'] = datos_pais[years_selected].sum(axis=1)

    # Cambiar el nombre de la tecnología
    datos_pais['Technology'] = datos_pais['Technology'].replace('Hydropower (excl. Pumped Storage)', 'Hydropower')

    st.subheader(f'Total de energía generada según el tipo')

    # Crear un checkbox para incluir o excluir la tecnología 'Fossil Fuels'
    incluir_fossil_fuels = st.checkbox('Incluir combustibles fósiles', value=True)

    # Filtrar los datos según la selección del checkbox
    if not incluir_fossil_fuels:
        datos_pais = datos_pais[datos_pais['Technology'] != 'Fossil fuels']

    # Calcular el porcentaje de cada tecnología
    datos_pais['Percentage'] = (datos_pais['Total'] / datos_pais['Total'].sum()) * 100


    # Crear dos columnas para los gráficos
    columna1, columna2 = st.columns([1,2])

    # Gráfico circular de porcentajes en la primera columna
    with columna1:
        st.markdown("#### Porcentual")
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(datos_pais['Percentage'], labels=datos_pais['Technology'], autopct='%1.1f%%', startangle=90, pctdistance=0.85, labeldistance=1.1, colors=sns.color_palette("Set3"))
        st.pyplot(fig)

    # Gráfico de barras con los totales en la segunda columna
    with columna2:
        st.markdown("#### Total")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=datos_pais, x='Technology', y='Total', color='red')
        ax.set_xlabel('Technology')
        ax.set_ylabel('Total (GWh)')
        ax.set_xticklabels(datos_pais['Technology'], rotation=45)
        st.pyplot(fig)

#GRAFICO PABLO

if opcion == "Energía en la UE":

    # Crear gráfico de barras con st.bar_chart
    st.subheader(f"Distribución porcentual de la generación de energía en la UE (2000 - 2023)")

    # Lista de países de la Unión Europea
    eu_countries = [
        "Austria", "Belgium", "Bulgaria", "Croatia, Rep. of", "Cyprus", "Czech Rep.",
        "Denmark", "Estonia, Rep. of", "Finland", "France", "Germany", "Greece", "Hungary",
        "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands, The",
        "Poland, Rep. of", "Portugal", "Romania", "Slovak Rep.", "Slovenia, Rep. of", "Spain", "Sweden"
    ]

    # Filtrar datos para países de la UE
    eu_data = generation[generation['Country'].isin(eu_countries)]

    # Selección de países
    country_options = ["Todos"] + eu_countries
    selected_countries = st.multiselect('Seleccionar Países', options=country_options, default="Todos")

    # Selección de tecnología
    technology_options = ["Todas"] + list(generation['Technology'].dropna().unique())
    selected_technology = st.selectbox('Seleccionar Tecnología', options=technology_options)

    if selected_technology != "Todas":
        eu_data = eu_data[eu_data['Technology'] == selected_technology]

    # Selección de rango de años
    year_columns = [col for col in eu_data.columns if col.startswith('F')]
    years = [int(col[1:]) for col in year_columns]
    year_range = st.slider('Seleccionar Rango de Años', min_value=min(years), max_value=max(years) - 1, value=(min(years), max(years) - 1))
    selected_columns = [f'F{year}' for year in range(year_range[0], year_range[1] + 1)]

    # Calcular el total de generación de energía para los países de la UE en el rango de años seleccionado
    eu_data['Total_Generation'] = eu_data[selected_columns].sum(axis=1)
    total_generation_eu = eu_data['Total_Generation'].sum()

    # Calcular el porcentaje de cada país
    eu_data['Percentage'] = (eu_data['Total_Generation'] / total_generation_eu) * 100

    if "Todos" not in selected_countries:
        eu_data = eu_data[eu_data['Country'].isin(selected_countries)]

    # Ordenar por porcentaje
    eu_data_sorted = eu_data.sort_values(by='Percentage', ascending=False)

    # Preparar datos para st.bar_chart
    chart_data = eu_data_sorted[['Country', 'Percentage', 'Technology']]
    chart_data = chart_data.sort_values(by='Percentage', ascending=False)

    # Mostrar gráfico en Streamlit
    st.bar_chart(chart_data, x='Country', y='Percentage', color='Technology', use_container_width=True)
