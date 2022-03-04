import pandas as pd
import os

def write_to_pandas(da, 
                    columns, 
                    index, 
                    column_dict={}, 
                    name='name', 
                    var='var'):
    """Write xr.DataArray to pd.DataFrame

    Parameters
    ----------
    da: xr.DaraArray
        
    columns: list
        List of xr.DataArray's coordinates which to set as pd.DataFrame columns

    index: xr.DataArray
       xr.DataArray containing the pd.DataFrame index information; e.g. da.time
    
    column_dict:  dict (optional)
        Dictionary containing new pd.DataFrame column names and corresponding values

    name: str (optional)
        Name of the pd.DataFrame rows; e.g. name of the xr.DataArray

    var: str (optional)
        Name of the xr.DataArray's CF variables

    Returns
    -------
    pd.DataFrame
    """

    df_output = pd.DataFrame(da, columns=columns,dtype=float)
    df_output[index.name] = index.values
    df_output['variable'] = [var]*len(index)
    for key, value in column_dict.items():
        df_output[key] = [value]*len(index)
    df_output['name'] = [name]*len(index)
    return df_output.set_index(index.name)

def concat_dataframe(dataframe, 
                     ds, 
                     variables,
                     index,
                     **kwargs):

    """Concatenate newly created Pd.DataFrame to already existing pd.DataFrame

    Parameters
    ----------
    dataframe: pd.DataFrame
        Already existing pd.DataFrame, can also be empty.
     
    ds: xr.DataSet

    variables: str or list
        Names(s) of the xr.Dataset variables to be written to the pd.DataFrame
    
    index: xr.DataArray
        xr.DataArray containing the pd.DataFrame index information; e.g. da.time


    kwargs:
        Opional parameters transferred to function `write_to_pandas`
        column_dict
        name
        var

    Returns
    -------
    pd.DataFrame
    """
    if isinstance(variables, str): variables = [variables]
    for var in variables:
        dataframe = pd.concat([dataframe,
                               write_to_pandas(ds[var],
                                               ds.field_region.values,
                                               index,
                                               **kwargs)
                               ])
    return dataframe

def write_to_csv(dataframe, output):
    """Write pd.DataFrame to csv table and save on disk
    
    Parameters
    ----------
    dataframe: pd.DataFrame

    output: str
        output name
        If directory path default name is 'spatial_average_table.csv'
    """

    if os.path.isdir(output):
        outfile=os.path.join(output, 'spatial_average_table.csv')
    elif output[-3:] == 'csv':
        outfile=output
    else:
        outfile=output+'.csv'
    dataframe.to_csv(outfile)
    print('File written: {}'.format(outfile))
