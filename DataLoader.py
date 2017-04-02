import pandas as pd

# CSV files location
data_loc = 'data/'
csv_loc = data_loc + 'csv/'
pkl_loc = data_loc + 'pkl/'

# Load all the data columns
columns = dict()
with open(data_loc + 'csv_schema.txt', 'r') as f:
    lines = f.readlines()
    for l in lines:
        l = l.replace('\n', '').split(',')
        columns[l[0]] = l[1:]


def load_csv(name, test=True):
    """ Load the given CSV file only """
    assert isinstance(name, str) and name in columns.keys()
    assert isinstance(test, bool)
    if test:
        df = pd.read_csv(csv_loc + name + '.csv', nrows=10000, header=None, escapechar='\\',
                         names=columns[name], index_col='id')
    else:
        tp = pd.read_csv(csv_loc + name + '.csv', iterator=True, chunksize=10000, header=None, escapechar='\\',
                         names=columns[name], index_col='id')
        df = pd.concat(tp)
    df.name = name
    return df


def load_pickle(name):
    """ Load the given CSV file only """
    assert isinstance(name, str) and name in columns.keys()
    df = pd.read_pickle(pkl_loc + name + '.pkl')
    return df


def load_all_csv(test=True):
    """ Load all the csv data files """
    assert isinstance(test, bool)
    dfs = []
    for k in columns.keys():
        print('Loading %s' % k)
        dfs.append(load_csv(k, test))
    return dfs


def get_table_names():
    from os import walk
    filenames = [f.split('.')[0] for f in next(walk(pkl_loc))[2] if f.split('.')[1] == 'pkl']
    return filenames


def is_column_name(c):
    return any(c in cols for cols in columns.values())


if __name__ == "__main__":
    print(is_column_name('person_role_id'))

    # Pickle all the files
    for k in columns.keys():
        if k in get_table_names():
            continue
        print('Pickling %s' % k)
        df = load_csv(k, test=False)
        df.to_pickle(pkl_loc + k + '.pkl')
        del df