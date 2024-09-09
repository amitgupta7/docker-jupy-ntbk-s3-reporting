## Load Dataframe
import pandas as pd
import plotly.express as px
import warnings
import fnmatch
import os
# Example
# import dataframeLoader as dfl
# dfl.loadDataFrameFromFileRegex('dataDir', 'securiti_appliance_cpu_used-max*.csv', metrics='cpu-max')
pd.set_option('future.no_silent_downcasting', True)

def loadPrometheusData(root, fileRegex, metricsName, fileAggFunc, fileExtn, aggfunction):
    print("processing "+fileRegex+metricsName+'-'+fileAggFunc+'*'+fileExtn)
    df1 = loadDataFrameFromFileRegex(root, fileRegex+metricsName+'-'+fileAggFunc+'*'+fileExtn, metrics=metricsName+'_'+fileAggFunc)
    if(metricsName == 'task_queue_length'):
        df1.loc[df1['metrics_name'].str.contains('securiti-appliance-downloader-tasks-queue', regex=False), 'metrics'] = 'taskq_'+fileAggFunc
        df1.loc[df1['metrics_name'].str.contains('t-appliance-downloader-tasks-queue', regex=False), 'metrics'] = 'tmp_taskq_'+fileAggFunc
        df1.loc[df1['metrics_name'].str.contains('securiti-appliance-linker', regex=False), 'metrics'] = 'linkerq_'+fileAggFunc

    if(metricsName == 'infra_access_latency'):
        df1.loc[df1['metrics_name'].str.contains('appliance_es_access_latency', regex=False), 'metrics'] = 'esLatency_'+fileAggFunc
        df1.loc[df1['metrics_name'].str.contains('appliance_postgres_access_latency', regex=False), 'metrics'] = 'pgLatency_'+fileAggFunc
        df1.loc[df1['metrics_name'].str.contains('appliance_redis_access_latency', regex=False), 'metrics'] = 'redisLatency_'+fileAggFunc

    df1['node_ip']=df1['node_ip'].fillna("master")
    df1 = df1.groupby(['appliance_id','ts', 'node_ip', 'metrics']).agg(value=('value', aggfunction)).reset_index()   
    df1['ts']=pd.to_datetime(df1['ts'],unit='s')
    return df1[['appliance_id','ts', 'node_ip', 'metrics', 'value']] 

def loadDataFrameFromFileRegex(root, regex, **kwargs):
    metrics = kwargs.get('metrics', None)
    df_arr = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch.fnmatch(name, regex) and os.path.getsize(os.path.join(path, name)) > 0:
                # print(os.path.join(path, name))
                df = pd.read_csv(os.path.join(path, name))
                df.insert(1, 'metrics', metrics)
                df_arr.append(df)
    if not df_arr:
        warnings.warn("No matching file found in "+root+" for regex: "+regex+". Empty dataframe will be returned." )
        return pd.DataFrame()    
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)      
        return pd.concat(df_arr, ignore_index=True)
    
def plotMetricsFacetForApplianceId(df, appliance_id, fromDt, toDt, ttl):
    dfp = df[(df['appliance_id'] == appliance_id) & (df['ts'] >= fromDt) & (df['ts'] <= toDt) ]
    dfp = dfp.pivot_table(index=['appliance_id','ts'], columns=['node_ip', 'metrics'], values='value', aggfunc='max').reset_index()
    dfp = dfp.drop('appliance_id', axis=1, level=0)
    dfp = dfp.set_index(['ts'])
    dfp = dfp.reindex(pd.date_range(dfp.index[0], dfp.index[-1], freq='h')).fillna(0)
    dfp.reset_index(level=[])
    dfp = pd.melt(dfp, ignore_index = False)
    fig = px.line(dfp, x=dfp.index, y="value", color='node_ip', facet_row='metrics', height=6000, facet_row_spacing=0.005, category_orders={"metrics": ["dataScannedinGB", "numberOfColsScanned" ,"cpu_used_avg", "cpu_used_max", "scanTime", "uniqPodCount", "memory_used_max"]}, markers=False, title=ttl)
    fig = fig.update_yaxes(matches=None)
    return fig

def loadStrucDataFromFileRegex(root, regex):
    print("loading Strctured Data from file: "+regex)
    df9 = loadDataFrameFromFileRegex(root, regex, metrics='strcutured_Scan')
    df9.rename(columns={'pod':'appliance_id'}, inplace=True)
    df9.rename(columns={'ds':'node_ip'}, inplace=True)
    df9=df9.groupby(['appliance_id', 'ts', 'node_ip']).agg(\
    numFilesScanned=('numberOfTablesScanned', 'sum'), \
    numberOfColsScanned=('numberOfColsScanned', 'sum'), \
    uniqPodCount=('uniqPodCount', 'max'), \
    scanTime=('processingTimeinHrs', 'sum'), \
    IdleTimeInHrs=('IdleTimeInHrs', 'sum'), \
    numberOfChunksScanned=('numberOfChunksScanned', 'max')).reset_index()
    df9['ts']=pd.to_datetime(df9['ts'],unit='ms')
    df9 = pd.melt(df9, id_vars=['appliance_id','ts', 'node_ip'], var_name='metrics', value_name='value')
    return df9


def loadUnstrucDataFromFileRegex(root, regex):
    print("loading Unstrctured Data from file: "+regex)
    df9 = loadDataFrameFromFileRegex(root, regex, metrics='unStrcutured_Scan')
    df9.rename(columns={'pod':'appliance_id'}, inplace=True)
    df9.rename(columns={'ds':'node_ip'}, inplace=True)
    df9=df9.groupby(['appliance_id', 'ts', 'node_ip']).agg(\
    dataScannedinGB=('dataScannedInGB', 'sum'), \
    scanTime=('processingTimeinHrs', 'sum'), \
    IdleTimeInHrs=('IdleTimeInHrs', 'sum'), \
    numFilesScanned=('numberOfFilesScanned', 'sum'), \
    uniqPodCount=('uniqPodCount', 'max')).reset_index()
    df9['ts']=pd.to_datetime(df9['ts'],unit='ms')
    df9['avgFileSizeInMB']=df9['dataScannedinGB']*1000/df9['numFilesScanned']
    df9 = pd.melt(df9, id_vars=['appliance_id','ts', 'node_ip'], var_name='metrics', value_name='value')
    return df9

def loadPrometheusDataFromFileRegex(root, filePrefix, metricsArr, fileExtn):
    df_arr = []
    for metricsName in metricsArr:
        for fileAggFunc in ['max', 'avg']:
            aggfunction = 'mean'
            if(fileAggFunc == 'max'):
                aggfunction = 'max'
            df_tmp = loadPrometheusData(root, filePrefix, metricsName, fileAggFunc, fileExtn, aggfunction)
            df_arr.append(df_tmp)

    df = pd.concat(df_arr, ignore_index=True)
    return df