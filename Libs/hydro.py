
from numpy import isnan, mean
import pandas as pd
import geopandas as gpd
import plotly.express as px



def get_df(gdf,estation):
    ''' se pide el objeto de tipo deoDataFrame que contiene las estaciones y se pide la estacion para extraer los datos
    gdf (object)-> geodataframe 
    estation (str)-> string del numero de estacion

    Regresa un DataFrame con la informacion de la estacion solicitada en formato de serie de tiempo
    '''

    try:
        N = gdf[gdf['Name']== estation].index[0]

        df = pd.read_csv(gdf.loc[N,'link'], skiprows=7 )

        for i in df.index:
            df.loc[i,'fecha'] = pd.to_datetime(str(df.loc[i,'Mes']) +'/'+ str(df.loc[i,'Día']) +'/'+ str(df.loc[i,'Anio']))  

        df.set_index('fecha', inplace = True)

        df = df.drop(['Mes','Día','Anio'], axis=1)
    except:
        print('error')


    return df


def plot_station(df):

    try:
        fig = px.line(df, x=df.index ,y='Datos')
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.show()
    except:
        print("no se pudo... :'v checa la estacion")


def periodos_foc(est, foc='faltantes'):
    dd =[]
    ondas= pd.DataFrame(columns=['inicio','final','no_dias'])

    if foc == 'faltantes':

        for i in range(0,len(est)):

            if isnan(est.iloc[i,0]):

                dd.append(est.iloc[i,0])
            else:
                if len(dd)>0 : 

                    rr={'inicio':est.iloc[i-len(dd)].name,
                        'final':est.iloc[i-1].name, 
                        'no_dias':len(dd) }

                    ondas = ondas.append(rr, ignore_index=True)

                dd=[]
        ondas['%']= (ondas['no_dias']/len(est))*100
                
        return ondas

    elif foc == 'completos':

        for i in range(0,len(est)):

            if ~isnan(est.iloc[i,0]):

                dd.append(est.iloc[i,0])
            else:
                if len(dd)>0 : 

                    rr={'inicio':est.iloc[i-len(dd)].name,
                        'final':est.iloc[i-1].name, 
                        'no_dias':len(dd) }

                    ondas = ondas.append(rr, ignore_index=True)

                dd=[]
        ondas['%']= (ondas['no_dias']/len(est))*100
        return ondas