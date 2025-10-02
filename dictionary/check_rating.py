from dictionary.generate_dictionary import radioligist_dict
import random
import subprocess
import os 

SEQUENCES = ['T1w', 'T2w', 'FLAIR']
RATING_TYPE = ['image_quality', 'motion','susceptibility', 'flow_ghosting']
moveji = '🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀🌀'
suscpji= '✨✨✨✨✨✨✨✨✨✨✨✨✨'
ghostji= '👻👻👻👻👻👻👻👻👻👻👻👻👻'
qualiji= '✅✅✅✅✅✅✅✅✅✅✅✅✅'
wrongji= '❌❌❌❌❌❌❌❌❌❌❌❌❌'
modaliji='❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇❇'
DICTJI = {'image_quality': qualiji, 'motion': moveji,
          'susceptibility': suscpji,'flow_ghosting': ghostji}

def check_radiologists(dic_seq, seq = False, rtype = False):
    msg_break ='\n****************\nInvalid entry, try again. \n****************\n'

    print(f'\n{DICTJI[rtype]} Rating type: {seq} {rtype} {DICTJI[rtype]}')

    if not seq and not rtype:
        while True:
            try:
                if not seq:
                    print(f'Available sequences: {SEQUENCES}')
                    seq = int(input('\t * Sequence: '))
                    in_seq = SEQUENCES[seq-1]

                if not rtype:
                    print(f'Available ratings: {RATING_TYPE}')
                    rtype = int(input('\t * Rating type: '))
                
                if int(seq) not in range(1,len(SEQUENCES)+1) or int(rtype) not in range(1,len(RATING_TYPE)+1):
                    print(msg_break)
                    in_rtype = RATING_TYPE[rtype-1]

                else:
                    break
            except ValueError:
                print(msg_break)
    else:
        in_seq = seq
        in_rtype = rtype
    

    in_pred = input('\n\t * Proposed score: ')

    while True:
        while True:
            try: 
                choice_dict = dic_seq[in_seq][in_rtype][in_pred]
                break
            except: 
                print(f'\n{wrongji} Invalid rating ({in_pred}), reenter {rtype} rating{wrongji}')
                in_pred = input('\n\t * Proposed score: ')


        choice_files = choice_dict['files']
        shuffles_files = list(choice_files.keys())
        if len(shuffles_files) >= 4:
            shuffles_files = random.sample(shuffles_files, 4)
        else: 
            N_queries = len(choice_dict['query_files'].keys())
            n_queries = 4 - len(shuffles_files) if N_queries > 4 - len(shuffles_files) else N_queries
            print(f'\nTotal shuffles files: {len(shuffles_files) }')
            print(f"\nTotal query_files: {n_queries}")
            print(f'\nGetting n query_files: {4- len(shuffles_files)}')
            shuffles_queries = random.sample(list(choice_dict['query_files'].keys()), n_queries) if n_queries > 0 else []
            shuffles_files = shuffles_files + shuffles_queries

        print(f'\n~~~~~~~~~~~~~~~~~~~~~~\n{in_seq} {in_rtype} ratings for {in_pred}:\n\t')

        if len(shuffles_files) == 0:
            print(f'\n{wrongji} No files for these constraints for {rtype} {wrongji}')
            print(f'\n\t * Modality: {in_seq} \t * Rating: {in_rtype} \t * Prediction: {in_pred}')
            print('\nOptions: \n\t1. 👆          2. 👇         3. 👍')
            in_option= input()

        else:
            for i, f in enumerate(shuffles_files[:4]):
                try:
                    print(f"{i+1}. {os.path.basename(f)}{choice_files[f]}")
                except KeyError: 
                    print(f"{i+1}. {os.path.basename(f)}{choice_dict['query_files'][f]}")

            command = ['itksnap', '-g', shuffles_files[0]] + ['-o'] + shuffles_files[1:4]
            viewer = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            prop_dict = dic_seq[in_seq][in_rtype]


            props_str = ''
            total = 0
            for key in prop_dict.keys():
                count_rated = prop_dict[key]['count']
                props_str += f"\tScore {key}: {count_rated}\t"
                total += count_rated
            
            prop_perc = round((choice_dict['count']/total)*100, 3)
            print("\nProportions: " + props_str + f"\n\t * Choice proprotion: {prop_perc}%")
            print('\nOptions: \n\t1. 👆          2. 👇         3. 👍')
            in_option= input()

            viewer.terminate()
            viewer.wait()
        print('\n****************\n')

        if in_option == '2':
            in_pred = str(int(in_pred) -1)
        if in_option == '1':
            in_pred = str(int(in_pred) +1)
        if in_option == '3':
            break
    print(f'\nFinal predictions: {in_pred}')
    return(in_pred)


if __name__ == "__main__":
    dict_radiologists = radioligist_dict()

    while True:
        
        print(f'Available sequences: {SEQUENCES}')
        seq = int(input('\t * Sequence: '))
        in_seq = SEQUENCES[seq-1]
        print(f'\n\n{modaliji}{modaliji}{modaliji}')
        print(f'{modaliji}       Sequence: {in_seq}      {modaliji}')
        print(f'{modaliji}{modaliji}{modaliji}')


        for i, rate in enumerate(RATING_TYPE):
            prediction = check_radiologists(dic_seq=dict_radiologists, rtype=rate, seq=in_seq)
