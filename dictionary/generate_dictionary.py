import pandas as pd 
import re 
import os 
from collections import defaultdict
from configparser import ConfigParser
config = ConfigParser()
config.read('dictionary_config.ini')

def radioligist_dict(sequences = ['T1w', 'T2w', 'FLAIR'], 
                     rating_type=['image_quality', 'motion','susceptibility', 'flow_ghosting'], 
                     ratings_csv =config['inputs']['CSV_RATINGS'], 
                     dir_niis =config['inputs']['IN_NIIS']):
    bookji = '📜📜📜📜📜📜📜📜📜📜📜📜📜'

    print(f'\n\n{bookji} Getting Radiologist dictionary...{bookji} \n')

    df_in = pd.read_csv(ratings_csv)
    dic_seq = {}


    for sequence in sequences: 

        df = df_in[df_in['modality'] == sequence]
        dic_type = {}

        for rate in rating_type:
            dic_ratings = defaultdict(lambda: defaultdict(int))       
            
            dic_ratings = {
                str(i): {'files': {}, 'query_files': {}, 'count': 0} 
                for i in range(1, 6)
            }   
            cols = [val for val in df.columns if re.match(fr'.*_{rate}', val)]

            for idx, row in df.iterrows():
                aep_id = row['aep_id']
                modality = row['modality']

                scores = [row[val] for val in cols if not pd.isna(row[val])]
                raters = [val.replace(f'_{rate}', '').upper() for val in cols if not pd.isna(row[val])]

                avg_score = round(pd.Series(scores).mean()) if scores else None
                if avg_score:   
                    dic_ratings[str(int(avg_score))]['count'] += 1
                else: 
                    break
                dir_sub = f'{dir_niis}/sub-{aep_id}/'
                niis = [os.path.join(root, file) for root, dir, files in os.walk(dir_sub) for file in files if file.endswith('nii.gz') and modality in file]

                if len(raters) >1 and len(set(scores)) == 1:                        
                    ratings = f"\t 😡 MEAN 😡  : {avg_score}                "
                    for i, score in enumerate(scores):
                        ratings += f'* {raters[i]}: {score}        '
                    dic_ratings[str(int(avg_score))]['files'][niis[0]] = ratings
                else: 
                    filt_ratings = f"\t 🧐 FOUND 🧐 : {avg_score} \t\t"
                    for rater, filt_score in enumerate(scores):
                        filt_ratings += f'* {raters[rater]}: {filt_score}\t\t' 
                    dic_ratings[str(int(avg_score))]['query_files'][niis[0]] = filt_ratings

            # for rating in range(1,6):
            #     if len(dic_ratings[str(rating)]['files']) < 3:
            #         df_filter = df[(df[cols[1]] == rating) | (df[cols[2]] == rating) | (df[cols[0]] == rating)]
            #         filt_cols = ['aep_id', 'modality'] + cols
            #         df_filter = df_filter[filt_cols]
                    
            #         for filt_idx, filt_row in df_filter.iterrows():
            #             filt_aepid= filt_row['aep_id']
            #             filt_mod= filt_row['modality']
                        

            #             filter_scores = [filt_row[val] for val in cols if not pd.isna(filt_row[val])]
            #             filt_raters = [val.replace(f'_{rate}', '').upper() for val in cols if not pd.isna(filt_row[val])]
                    
            #             filt_dir = f'{dir_niis}/sub-{filt_aepid}/'
            #             filt_niis = [os.path.join(root, file) for root, dir, files in os.walk(filt_dir) for file in files if file.endswith('nii.gz') and filt_mod in file]
                        
            #             filt_ratings = f"\t 🧐 FOUND 🧐 : {rating} \t\t"
            #             for rater, filt_score in enumerate(filter_scores):
            #                 filt_ratings += f'* {filt_raters[rater]}: {filt_score}\t\t' 
            #             dic_ratings[str(rating)]['query_files'][filt_niis[0]] = filt_ratings


            dic_type[rate] = dic_ratings

        dic_seq[sequence] = dic_type
    return(dic_seq)

if __name__ == '__main__':
    config.read('dictionary_config.ini')
    radio_dict = radioligist_dict()
    print('done')
