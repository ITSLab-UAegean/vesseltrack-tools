"""_summary_

Returns:
    _type_: _description_
"""
import copy
import pandas as pd
from vesseltrack_tools.density.vessel_type import get_vessel_type_dataframe


grid = None
gridEL = None

def simple_density_init(_config, _grid, _gridEL):
    """_summary_

    Args:
        _config (_type_): _description_
        _grid (_type_): _description_
        _gridEL (_type_): _description_
    """
    global grid
    global gridEL
    grid  = copy.deepcopy(_grid[['gridID']].set_index('gridID'))
    gridEL = _gridEL


def vessels_count(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    pos = pd.read_csv(file_path)
    pos['xGrid'] = pos['X'] / gridEL
    pos['yGrid'] = pos['Y'] / gridEL
    pos['xGrid'] = pos['xGrid'].astype(int).astype(str)
    pos['yGrid'] = pos['yGrid'].astype(int).astype(str)
    pos['gridID'] = pos['xGrid'] + '_' + pos['yGrid']
    cellsVisited = pos['gridID'].unique()
    res= grid.loc[grid.index.intersection(cellsVisited)]
    res = res.assign(density=1)
    return res, get_vessel_type_dataframe(pos)



def positions_count(file_path):
    """_summary_

    Args:
    file_path (_type_): _description_

    Returns:
    _type_: _description_
    """
    pos = pd.read_csv(file_path)
    pos['xGrid'] = pos['X'] / gridEL
    pos['yGrid'] = pos['Y'] / gridEL
    pos['xGrid'] = pos['xGrid'].astype(int).astype(str)
    pos['yGrid'] = pos['yGrid'].astype(int).astype(str)
    pos['gridID'] = pos['xGrid'] + '_' + pos['yGrid']
    res = pos.merge(grid, on='gridID', how='inner')
    res = res.groupby('gridID').count()[['TIMESTAMP']].rename(columns={'TIMESTAMP': 'density'})
    
    return res, get_vessel_type_dataframe(pos)



def passes_count(file_path):
    """_summary_

    Args:
    file_path (_type_): _description_

    Returns:
    _type_: _description_
    """
    pos = pd.read_csv(file_path)
    pos['xGrid'] = pos['X'] / gridEL
    pos['yGrid'] = pos['Y'] / gridEL
    pos['xGrid'] = pos['xGrid'].astype(int).astype(str)
    pos['yGrid'] = pos['yGrid'].astype(int).astype(str)
    pos['gridID'] = pos['xGrid'] + '_' + pos['yGrid']
    pos[['lag_gridID']] = pos[['gridID']].shift(1)
    pos=pos[pos['gridID']!=pos['lag_gridID']]
    res = pos.merge(grid, on='gridID', how='inner')
    res = res.groupby('gridID').count()[['TIMESTAMP']].rename(columns={'TIMESTAMP': 'density'})
    
    return res, get_vessel_type_dataframe(pos)