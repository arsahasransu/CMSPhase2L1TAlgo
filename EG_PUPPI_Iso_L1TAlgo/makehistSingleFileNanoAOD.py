#import os
import yaml

import ROOT

from my_pyroot_tools import calculate_invM

def main():

    hists_dict = {}

    with open('histmaker_config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        tree_name = config['tree_name']
        df_xtra_columns = config['new_df_columns']

        # Loop over mc and datasets
        for fileset in config['input_nanoaod_files']:
            tag = fileset['tag']
            files_path = fileset['filespath']
            maxE = fileset['maxevents']

            df = ROOT.RDataFrame(tree_name, files_path)

            print(f'Processing {tag} with {maxE} of {df.Count().GetValue()} entries')
            df = df.Range(maxE)
            
            # Last Copy of Prompt Hard Process gen electron filter
            genfilter = fileset['genfilter']
            for dfxtra_key in df_xtra_columns.keys():
                if dfxtra_key == 'genfilter':
                    for genfilterkeys in df_xtra_columns[dfxtra_key].keys():
                        df = df.Define(genfilterkeys, 
                                       df_xtra_columns[dfxtra_key][genfilterkeys].format( genfilter ) )
                else:
                    df = df.Define(dfxtra_key, df_xtra_columns[dfxtra_key])
            df = df.Define('gen_prompt_el_invM', calculate_invM.format('gen_prompt_el_pt', 
                                                                       'gen_prompt_el_eta', 
                                                                       'gen_prompt_el_phi', 
                                                                       0.000511) )

            hists_dict[tag+'gen_el_n'] = df.Histo1D('gen_prompt_el_n')
            hists_dict[tag+'gen_el_pt'] = df.Histo1D('gen_prompt_el_pt')
            hists_dict[tag+'gen_el_eta'] = df.Histo1D('gen_prompt_el_eta')
            hists_dict[tag+'gen_el_phi'] = df.Histo1D('gen_prompt_el_phi')
            hists_dict[tag+'gen_el_pdg'] = df.Histo1D(('gen_el_pdg', 'gen_el_pdg', 200, -100, 100), 
                                                      'gen_prompt_el_pdg')
            hists_dict[tag+'gen_el_status'] = df.Histo1D('gen_prompt_el_status')
            hists_dict[tag+'gen_el_invM'] = df.Histo1D(('gen_el_invM', 'gen_el_invM', 200, 0, 200), 
                                                       'gen_prompt_el_invM')

            print('Writing output histograms.')
            with ROOT.TFile.Open(f'histograms_{tag}.root', 'RECREATE') as f:
                for _, hist in hists_dict.items():
                    hist.Write()


if __name__ == '__main__':
    main()