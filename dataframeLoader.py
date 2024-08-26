## Load Dataframe
import pandas as pd
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
        df1.loc[df1['metrics_name'].str.contains('t-appliance-downloader-tasks-queue', regex=False), 'metrics'] = 'downloadq_'+fileAggFunc
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