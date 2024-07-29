from my_pyroot_tools import calculate_invM

def make_3p_df_cols(*, df, selection, branch, tag):
    df = df.Define(tag+'_pt', branch+'_pt[{0}]'.format(selection))
    df = df.Define(tag+'_eta', branch+'_eta[{0}]'.format(selection))
    df = df.Define(tag+'_phi', branch+'_phi[{0}]'.format(selection))
    return df    
    
def make_pfpart_df_cols(*, df, selection, branch, tag):
    df = df.Define('n'+tag, 'Sum({0})'.format(selection))
    df = make_3p_df_cols(df=df, selection=selection, branch=branch, tag=tag)
    df = df.Define(tag+'_pdgId', branch+'_pdgId[{0}]'.format(selection))
    return df

def make_gen_df_cols(*, df, selection, branch, tag):
    df = make_pfpart_df_cols(df=df, selection=selection, branch=branch, tag=tag+'_gen')
    df = df.Define(tag+'_gen_statusFlags', branch+'_statusFlags[{0}]'.format(selection))
    df = df.Define(tag+'_gen_invM', calculate_invM.format(tag+'_gen', 0.000511))
    return df

def make_puppi_el_eb_df_cols(*, df, pfcandselection, tag):
    df = df.Define('npuppi_el_eb', 'Sum({0})'.format(pfcandselection))
    df = make_3p_df_cols(df=df, selection=pfcandselection, branch='L1PuppiCand', tag=tag+'_puppi_el_eb')
    df = df.Define('puppi_el_eb_pdg', 'L1PuppiCand_pdgId[{0}]'.format(pfcandselection))
    return df
