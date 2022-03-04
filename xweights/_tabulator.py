import pandas as pd

def write_to_pandas(da, 
                    columns, 
                    index, 
                    column_dict={}, 
                    name='name', 
                    var='var'):

    df_output = pd.DataFrame(output, columns=columns,dtype=float)
    df_output[index.name] = index.values
    df_output['variable'] = [var]*len(index)
    for key, value in column_dict.items():
        df_output[key] = [value]*len(index)
    df_output['name'] = [name]*len(index)
    return df_output.set_index(index.name)

def concat_dataframe(dataframe, 
                     variables, 
                     ds, 
                     column_dict={}, 
                     name='name', 
                     index=None):

    for var in variables:
        dataframe = pd.concat([dataframe,
                               write_to_pandas(ds[var],
                                               ds.field_region.values,
                                               index=index,
                                               column_dict=column_dict,
                                               name=name,
                                               var=var)
                               ])
return dataframe

def write_to_csv(dataframe, output):
    if os.path.isdir(output):
        outfile=os.path.join(output, 'spatial_average_table.csv')
    elif output[-3:] == 'csv':
        outfile=output
    else:
        outfile=output+'.csv'
    dataframe.to_csv(outfile)
    print('File written: {}'.format(outfile))
