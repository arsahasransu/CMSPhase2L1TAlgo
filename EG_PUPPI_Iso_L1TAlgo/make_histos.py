def make_3p_histos(*, hists_dict, df, tag, branch):
    hists_dict[tag+'_pt'] = df.Histo1D((tag+'_pt', tag+'_pt', 200, 0, 200), 
                                       branch+'_pt')
    hists_dict[tag+'_eta'] = df.Histo1D((tag+'_eta', tag+'_eta', 200, -5, 5), 
                                        branch+'_eta')
    hists_dict[tag+'_phi'] = df.Histo1D((tag+'_phi', tag+'_phi', 200, -4, 4), 
                                        branch+'_phi')
    return hists_dict

def make_pfpart_histos(*, hists_dict, df, tag, branch):
    hists_dict[tag+'_n'] = df.Histo1D((tag+'_n', tag+'_n', 50, 1, 51),
                                                 'n'+branch)
    hists_dict = make_3p_histos(hists_dict=hists_dict, df=df, tag=tag, branch=branch)
    hists_dict[tag+'_pdgId'] = df.Histo1D((tag+'_pdgId', tag+'_pdgId', 200, -100, 100), 
                                          branch+'_pdgId')
    return hists_dict

def make_gen_histos(*, hists_dict, df, tag, branch):
    hists_dict = make_pfpart_histos(hists_dict=hists_dict, df=df, tag=tag+'_gen', branch=branch)
    hists_dict[tag+'_gen_statusFlags'] = df.Histo1D((tag+'_gen_statusFlags', tag+'_gen_statusFlags', 40000, 0, 40000),
                                                    branch+'_statusFlags')
    if df.HasColumn(branch+'_invM'):
        hists_dict[tag+'_gen_invM'] = df.Histo1D((tag+'_gen_invM', tag+'_gen_invM', 200, 0, 200),
                                                 branch+'_invM')
    return hists_dict
