################################################
'''
Given a directory of cifs, this script will create a csv file with the following columns:
- id
- cif
- tc
- pretty_formula
'''
################################################
from tqdm import tqdm
import os
import glob
import pandas as pd
import argparse
# from cdvae.common.utils import PROJECT_ROOT


def make_cif(folder_filepath, csv_filepath, val_split=0.1, test_split=0.1):
    """folder_filepath contains cif files
    csv_filepath is the filepath to the csv that already contains the id, tc, and pretty_formula columns
    """
    csv = pd.read_csv(csv_filepath)
    all_files = sorted(glob.glob(os.path.join(folder_filepath, '*.cif')))
    # only take the first 100

    cif_dict = {}
    for path in tqdm(all_files):
        crystal = open(path, 'r').read()
        id = os.path.basename(path).rsplit('.', 1)[0]
        cif_dict[id] = crystal
    cif_df = pd.DataFrame.from_dict(cif_dict, orient='index', columns=['cif'])
    # combine cif_df with csv
    cif_df = cif_df.reset_index()
    cif_df = cif_df.rename(columns={'index': 'id'})
    print(cif_df)
    csv = csv.merge(cif_df, on='id', how='inner')
    print(csv)
    # split into train val test
    train_df = csv.sample(frac=1 - val_split - test_split)
    val_df = csv.drop(train_df.index).sample(frac=val_split / (val_split + test_split))
    test_df = csv.drop(train_df.index).drop(val_df.index)
    train_df.to_csv('train.csv', index=False)
    val_df.to_csv('val.csv', index=False)
    test_df.to_csv('test.csv', index=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Preprocessing.')
    PROJECT_ROOT = "/mnt/c/Users/axema/cdvae"
    parser.add_argument("--folder_filepath", type=str, default='cifs')
    parser.add_argument("--csv_filepath", type=str, default='combined.csv')
    parser.add_argument("--val_split", type=float, default=0.1)
    parser.add_argument("--test_split", type=float, default=0.1)
    options = parser.parse_args()
    make_cif(os.path.join(PROJECT_ROOT, 'database', options.folder_filepath), os.path.join(PROJECT_ROOT, 'database', options.csv_filepath), options.val_split, options.test_split)
