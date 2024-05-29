#%% Libraries
import pandas as pd
import numpy as np



def determine_growth_direction(value):
    if value < 0:
        return 'Decrease'
    elif value > 0:
        return 'Increase'
    else:
        return 'Equal'



def clean_data(df):
    print("Before of cleaning the database {} rows".format(df.shape[0]))

    
    # Corregir valores de forma manual
    # El archivo correccion datos tiene las columnas
    # CONTRACT_ID, ESTIMATED_COST_ORIG, CONTRACT_VALUE_ORIG, ADDITIONAL_COST_ORIG, FINAL_COST_ORIG
    correccion = pd.read_excel("correccion_datos.xlsx")
    for index, row in correccion.iterrows():
        contract_id = row['CONTRACT_ID']
        for col_index, col_value in row.iloc[1:].items():
            df.loc[df['CONTRACT_ID'] == contract_id, col_index] = col_value
            
    # Recalcular algunas variables
    # Scale all values of contracto to monthly legal minimimun salary 
    
    df['CONTRACT_VALUE_ORIG_MILLIONS'] = df['CONTRACT_VALUE_ORIG']/1e6
    df['ADDITIONAL_COST_ORIG_MILLIONS'] = df['ADDITIONAL_COST_ORIG']/1e6
    df['FINAL_COST_ORIG_MILLIONS'] = df['FINAL_COST_ORIG']/1e6
    
    df['PROJECT_INTENSITY_ORIG'] = df['CONTRACT_VALUE_ORIG']/df['ORIGINAL_DEADLINE']
    df['AWARD_GROWTH_ORIG'] = ((df['CONTRACT_VALUE_ORIG'] - df['ESTIMATED_COST_ORIG'])/df['ESTIMATED_COST_ORIG'])*100
    df['COST_DEVIATION_ORIG'] = (df['FINAL_COST_ORIG'] - df['CONTRACT_VALUE_ORIG'])/df['CONTRACT_VALUE_ORIG']
            
    # Filters

    # Quitar contratos sin costo estimado registrado
    df = df.loc[~(df['ESTIMATED_COST_ORIG'] == 0)].copy()
    
    # Seleccionar contratos por valor superior a 20 millones
    df = df[df['CONTRACT_VALUE_ORIG'] > 20e6].copy()
    
    # Quitar algunos contratos que no hacen parte de la muestra
    eliminar_contratos = [
        '17-12-7312505-6645201', # Convenio
        '17-12-7222328-6566950', # Convenio
        '15-12-4210058-3886615', # Convenio
        '18-4-8537252-7766100',  # Convenio
        '15-12-3977166-3689414',  # Convenio
        '15-12-3977324-3689541'
        ]
    df = df.loc[~(df['CONTRACT_ID'].isin(eliminar_contratos))].copy()
    
    # Transform existing columns
    df['OBJETC_DETAIL'] = df['OBJETC_DETAIL'].str.upper()
    # Quitar convenios interadministrativos
    kw_convenios = [
        'AUNAR',
        'CONVENIO',
        'ANUAR',
        'AUNNAR',
        'INTERADMINISTRATIVO',
        'COMPLEMENTACION DE ESFUERZOS INSTITUCIONALES',
        'COMPLEMENTAR ESFUERZOS INSTITUCIONALES',
        'UNIR  ESFUERZOS',
        'UNIR ESFUERZOS',
        'UNION DE ESFUERZOS',
        'COMPELMENTACION DE ESFUERZOS'
                ]
    kw_convenios = '|'.join(kw_convenios)
    df = df.loc[~df['OBJETC_DETAIL'].str.contains(kw_convenios)].copy()

    # Quitar contratos que no son obra
    kw_otros = ['ESTUDIOS',
                'DISENOS',
                'ESTUDIO',
                'DISENO',
                'INTERVENTORIA',
                'INTERVENTORA',
                'INTRERVENTORIA',
                'ADMINISTRACION',
                'INVENTARIO',
                'ELABORACION DE UN  MANUAL',
                'SUMINISTRO',
                'INSTITUCIONES EDUCATIVAS',
                'INSTITUCION EDUCATIVA',
                'MANTENIMIENTO RUTINARIO',
                'COFINANCIACIÓN',
                'PRESTACION DE SERVICIO',
                'PRESTACION DE SERVICIOS',
                'ARRENDAMIENTO',
                'PRESTAR EL SERVICIOS'
                'LIMPIEZA',
                'REMOCION',
                'SERVICIO DE ALQUILER',
                'PRESTAR SERVICIO',
                'RECUPERACION',
                'COFINANCIA',
                'PRESTAR EL SERVICIOS',
                'MITIGACION',
                'DESASTRE',
                'EMERGENCIA',
                'DESLIZAMIENTO DE TALUD',
                'DESASTRE',
                'ALQUILER',
                'AFECTACIONES',
                'OLA INVERNAL',
                'MANTEMIENTO',
                'LIMPIEZA'
                ]

    kw_otros = '|'.join(kw_otros)

    df = df.loc[~df['OBJETC_DETAIL'].str.contains(kw_otros)].copy()

    # 5. Quitar otros tipos de obras
    kw_otras_obras = ['ACUEDUCTO',
                    'ALCANTARILLADO',
                    'PARQUE',
                    'COLEGIO']

    kw_otras_obras = '|'.join(kw_otras_obras)

    df = df.loc[~df['OBJETC_DETAIL'].str.contains(kw_otras_obras)].copy()
    
    # 6. Seleccionar solo proyectos viales
    df = df[df['OBJETC_DETAIL'].str.contains('VIA|VIAS|VIAL')].copy()
    
    # 7. Seleccionar solo proyectos de vías rurales según la definición técnica 
    df = df[df['OBJETC_DETAIL'].str.contains('VEREDA|VEREDAL|TERCIARIA|VEREDAS|RURAL')].copy()

    
    # 8. Estandarizar el tipo de proceso
    tipo_proceso_mod = ['CONTRATACIÓN DIRECTA','LICITACIÓN','SELECCIÓN ABREVIADA','MÍNIMA CUANTÍA','RÉGIMEN ESPECIAL']
    df['PROCESS_TYPE_MOD'] = ''
    for i in tipo_proceso_mod:
        df.loc[df['PROCESS_TYPE'].str.contains(i), ['PROCESS_TYPE_MOD']] = i
    df.loc[df['PROCESS_TYPE_MOD'] == '', ['PROCESS_TYPE_MOD']] = 'OTRO'

    # 9. Limpiar el nombre de los dapartamentos
    dep_mod = {'BOGOT DC':'BOGOTÁ DC',
                'BOYAC':'BOYACÁ',
                'CAQUET':'CAQUETÁ',
                'CRDOBA':'CÓRDOBA',
                'SAN ANDRÉS PROVIDENCIA Y SANTA CATALINA':'SAN ANDRÉS PROV. Y STA. CAT.',
                'BOLVAR':'BOLÍVAR',
                'CHOC':'CHOCÓ'}
    df['DEPARTMENT'].replace(dep_mod, inplace=True)

    # 10. Asignar tipo de obra
    df['TIPO_OBRA_CONSTRUCCION'] = df['OBJETC_DETAIL'].str.contains('CONSTRUCCION|PAVIMENTACION|COSNTRUCCION|COSNTRUCCION|CONTRUCCION|CONSTRUIR|ADECUACUACION')
    df['TIPO_OBRA_MANTENIMIENTO'] = df['OBJETC_DETAIL'].str.contains('MANTENIMIENTO|MANTEMIENTO|MANTENER|MANTEMIENTO|MATENIMIENTO|MANTANIMIENTO|MANTENIIENTO|MATENIMIENTO|MANTANIMIENTO|MANTANIMIENTO|MANTENIIENTO')
    df['TIPO_OBRA_REHABILITACION'] = df['OBJETC_DETAIL'].str.contains('REHABILITACION|REHABILITAR|REHABLITACION|RECUPERACION|REHABLITACION')
    df['TIPO_OBRA_MEJORAMIENTO'] = df['OBJETC_DETAIL'].str.contains('MEJORAMIENTO|MEJORAR|MEJORAMENTO|MEJORAMAIENTO|MEKJORAMIENTO|MEJORAMAIENTO|MEJORAMENTO|MEKJORAMIENTO|MEJORAMENTO')
    df['TOTAL_CLASS_TIPO'] = np.int32(df['TIPO_OBRA_CONSTRUCCION'] + df['TIPO_OBRA_MANTENIMIENTO'] + df['TIPO_OBRA_REHABILITACION'] + df['TIPO_OBRA_MEJORAMIENTO'])
    df['TIPO_OBRA_OTROS'] = df['TOTAL_CLASS_TIPO'] == 0
    cols_tipo_obra = ['TIPO_OBRA_CONSTRUCCION', 'TIPO_OBRA_MANTENIMIENTO',
       'TIPO_OBRA_REHABILITACION', 'TIPO_OBRA_MEJORAMIENTO',
       'TIPO_OBRA_OTROS']
    df['TYPE_WORK'] = ''
    for i in cols_tipo_obra:
        df.loc[df[i] == True, 'TYPE_WORK'] = i

    # 11. Filtro por monto del contrato: contratos de mas de 20 millones

    # 12. Filtro por tipo de proceso
    df = df[~(df['PROCESS_TYPE_MOD'] == 'OTRO')].copy()

    # 13. Cost deviation frequency
    df['TIME_DEVIATION_FREC'] = df['TIME_DEVIATION'] > 0
    df['COST_DEVIATION_FREC'] = df['ADDITIONAL_COST_NORM'] > 0
    
    # 14. Crear la variable de tamaño del proyecto
    df['CONTRACT_VALUE_RANGE'] = pd.cut(df['CONTRACT_VALUE_ORIG_MILLIONS'], 
                                        bins=[0,100,500,1000,np.infty],
                                        labels=['(20-100]','(100-500]','(500-1000]','>1000'], 
                                        include_lowest=True)

    # 15. Work classification
    df['TIPO_OBRA_CONSTRUCCION'] = df['OBJETC_DETAIL'].str.contains('CONSTRUCCION|PAVIMENTACION|COSNTRUCCION|COSNTRUCCION|CONTRUCCION')
    df['TIPO_OBRA_MANTENIMIENTO'] = df['OBJETC_DETAIL'].str.contains('MANTENIMIENTO')
    df['TIPO_OBRA_REHABILITACION'] = df['OBJETC_DETAIL'].str.contains('REHABILITACION')
    df['TIPO_OBRA_MEJORAMIENTO'] = df['OBJETC_DETAIL'].str.contains('MEJORAMIENTO')
    df['TOTAL_CLASS_TIPO'] = np.int32(df['TIPO_OBRA_CONSTRUCCION'] + df['TIPO_OBRA_MANTENIMIENTO'] + df['TIPO_OBRA_REHABILITACION'] + df['TIPO_OBRA_MEJORAMIENTO'])
    df['TIPO_OBRA_OTROS'] = df['TOTAL_CLASS_TIPO'] == 0
    cols_tipo_obra = {
        'TIPO_OBRA_CONSTRUCCION': 'Construction', 
        'TIPO_OBRA_MANTENIMIENTO': 'Maintenance',
       'TIPO_OBRA_REHABILITACION':'Improvement', 
       'TIPO_OBRA_MEJORAMIENTO':'Rehabilitation',
       'TIPO_OBRA_OTROS':'Others'}
    df['TYPE_WORK'] = ''
    for i in cols_tipo_obra.keys():
        df.loc[df[i] == True, 'TYPE_WORK'] =  cols_tipo_obra[i]
        
    # 16. Rename process type
    rename_process = {
        'CONTRATACIÓN DIRECTA':'Direct Contracting', 
        'MÍNIMA CUANTÍA':'Minimum Amount', 
        'RÉGIMEN ESPECIAL':'Special Regime',
        'SELECCIÓN ABREVIADA':'Abbreviated Selection', 
        'LICITACIÓN':'Bidding'
    }
    df['PROCESS_TYPE_MOD'].replace(rename_process, inplace=True)
    
    
    # 19. Ordenar algunas variables categóricas
    # Define the order of categories
    cat_order_type_work = ['Construction','Improvement','Rehabilitation','Maintenance','Others']
    df['TYPE_WORK'] = pd.Categorical(df['TYPE_WORK'], categories=cat_order_type_work, ordered=True)
    
    cat_order_process = ['Direct Contracting','Special Regime','Minimum Amount','Abbreviated Selection','Bidding']
    df['PROCESS_TYPE_MOD'] = pd.Categorical(df['PROCESS_TYPE_MOD'], categories=cat_order_process, ordered=True)
    
    map_municipality_replace = {
        'TYPE_1':'Type 1',
        'TYPE_2':'Type 2', 
        'TYPE_3':'Type 3',
        'TYPE_4':'Type 4',
        'TYPE_5':'Type 5',
        'TYPE_6':'Type 6',  
        'NACIONAL DESCENTRALIZADO':'Other', 
        'Territorial':'Other',
        'OTHER':'Other'
        }
    df['MUNICIPALITY_TYPE'] = df['MUNICIPALITY_TYPE'].replace(map_municipality_replace) 
    cat_order_municipality = ['Type 1', 'Type 2', 'Type 3', 'Type 4', 'Type 5', 'Type 6', 'Other']
    df['MUNICIPALITY_TYPE'] = pd.Categorical(df['MUNICIPALITY_TYPE'], categories=cat_order_municipality, ordered=True)
    
    # Crear una variable para indicar el 'AWARD_GROWTH_DIRECTION'
    df['AWARD_GROWTH_DIRECTION'] = df['AWARD_GROWTH_ORIG'].apply(determine_growth_direction)
    cat_order_AWARD_GROWTH_DIRECTION = ['Decrease','Equal','Increase']
    df['AWARD_GROWTH_DIRECTION'] = pd.Categorical(df['AWARD_GROWTH_DIRECTION'], 
                                                  categories=cat_order_AWARD_GROWTH_DIRECTION, 
                                                  ordered=True)
    
    # Crear la variable de project intensity range
    df['PROJECT_INTENSITY_RANGE'] = pd.cut(df['PROJECT_INTENSITY_ORIG']/1e6, 
                                           bins=[0,1,2,3,np.infty],
                                           labels=['(0.0 - 1.0]', '(1.0 - 2.0]', '(2.0 - 3.0]', '>3.0'])
    
    
    print("Before of cleaning the database has {} rows".format(df.shape[0]))


    return df






