#import os
import yaml

import ROOT

from define_new_df_columns import make_gen_df_cols
from make_histos import make_gen_histos

def main():

    hists_dict = {}

    with open('histmaker_config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        tree_name = config['tree_name']
        #xfilefts = config['crossfilefilters']

        # Loop over mc and datasets
        for fileset in config['input_nanoaod_files']:
            filetag = fileset['tag']
            files_path = fileset['filespath']

            print(f'Processing {filetag} with user choice {fileset["maxevents"]} entries')
            df = ROOT.RDataFrame(tree_name, files_path)
            ROOT.RDF.Experimental.AddProgressBar(df)
            maxE = fileset['maxevents'] if fileset['maxevents'] >= 0 else df.Count().GetValue()
            df = df.Range(maxE)
            
            # For Last Copy of Prompt Hard Process gen electrons
            genpromptelselection = fileset['gen_prompt_el_selection']
            df = make_gen_df_cols(df=df, selection=genpromptelselection, branch='GenPart', tag='promptHardLastGenEl')
            genfilter = fileset['genfilter']
            genF_df = df.Filter(genfilter)
            #genEBF_df = genF_df.Filter('promptHardLastGenEl_gen_eta[0] < 1.479 && promptHardLastGenEl_gen_eta[1] < 1.479')

            '''
            genfilt_df = df.Clone()

            # gen el only in the EB
            ebgenfilter = genfilter + ' && ' + fileset['ebfilter']
            df_geneb = make_general_gen_df_cols(df=df, genfilter=ebgenfilter, clone=True)
            eventfilter = fileset['eventfilter']
            puppielctrebfilter = eventfilter + '&&' + fileset['puppielctrfilter']
            puppielctrebfilter = puppielctrebfilter + ' && ' + fileset['ebfilter']
            df_geneb = make_puppi_el_eb_df_cols(df=df, pfcandfilter=puppielctrebfilter)

            hists_dict = make_puppi_el_eb_histos(hists_dict=hists_dict, df=df, tag=tag)
            '''
            # Fill hists_dict with selected generator particle variables
            hists_dict = make_gen_histos(hists_dict=hists_dict, df=df, tag='all', branch='GenPart')
            hists_dict = make_gen_histos(hists_dict=hists_dict, df=genF_df, tag='genF_promptHardLastGenElF', 
                                         branch='promptHardLastGenEl_gen')

            print('Writing output histograms.')
            with ROOT.TFile.Open(f'varhistos_{filetag}.root', 'RECREATE') as f:
                for _, hist in hists_dict.items():
                    hist.Write()

if __name__ == '__main__':
    main()