
import pandas as pd

def calidad_datos(data):
    tipos = pd.df({'tipo': data.dtypes},index=data.columns)
    na = pd.df({'nulos': data.isna().sum()}, index=data.columns)
    na_prop = pd.df({'porc_nulos':data.isna().sum()/data.shape[0]}, index=data.columns)
    ceros = pd.df({'ceros':[data.loc[data[col]==0,col].shape[0] for col in data.columns]}, index= data.columns)
    ceros_prop = pd.df({'porc_ceros':[data.loc[data[col]==0,col].shape[0]/data.shape[0] for col in data.columns]}, index= data.columns)
    summary = data.describe(include='all').T
    summary['limit_inf'] = summary['mean'] - summary['std']*1.5
    summary['limit_sup'] = summary['mean'] + summary['std']*1.5
    summary['outliers'] = data.apply(lambda x: sum(np.where((x<summary['limit_inf'][x.name]) | (x>summary['limit_sup'][x.name]),1 ,0))if x.name in summary['limit_inf'].dropna().index else 0)
    return pd.concat([tipos, na, na_prop, ceros, ceros_prop, summary], axis=1).sort_values('tipo')


def get_descriptives(df):
    for k, v in df.iteritems():
        print (k)
        print(v.describe())
        print('-'*100)
    return get_descriptives(df)

def get_null_cases(df, var, print_list=False):
    tmp = df.copy()
    tmp['flagnull'] = tmp[var].isnull()
    counter_na = 0
    for i, r in tmp.iterrows():
        if r['flagnull'] == True:
            counter_na += 1
            if print_list == True:
                print(r['cname'])
    
    print('Casos nulos para {}: {}'.format(var,counter_na))
    print('Porcentaje nulos para {}: {}'.format(var,counter_na/df.shape[0]))
    
    #calidad_datos(df).loc[:,['nulos','porc_nulos']].sort_values('porc_nulos', ascending=False)
    
def hist_plot(sample_df, full_df, var, mean_frac=False, true_mean=False):
    tmp = sample_df[var].dropna()
    plt.hist(tmp, color='grey', alpha=.5)
    plt.title('Histograma {}'.format(var))
    if mean_frac:
        plt.axvline(np.mean(tmp), color ='blue')
    if true_mean:
        plt.axvline(np.mean(full_df[var]), color ='red')
    plt.show()
    
def dotplot(df, plot_var, plot_by = 'ht_region', statistic='mean'):
    tmp= df.loc[:,[plot_var, plot_by]]
    tmp_group = tmp.groupby(plot_by).agg({plot_var:statistic})
    plt.plot(tmp_group.values, tmp_group.index, 'o', color ='grey')
    if statistic == 'mean':
        plt.axvline(tmp[plot_var].mean(), color='red', linestyle='--')
    if statistic == 'median':
        plt.axvline(tmp[plot_var].median(), color='blue', linestyle='--')
    plt.show()