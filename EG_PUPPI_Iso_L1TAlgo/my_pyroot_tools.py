calculate_invM = '''if({0}_pt.size()<2) return -9999.0;
                TLorentzVector gen_el1, gen_el2;
                gen_el1.SetPtEtaPhiM({0}_pt[0], {0}_eta[0], {0}_phi[0], {1});
                gen_el2.SetPtEtaPhiM({0}_pt[1], {0}_eta[1], {0}_phi[1], {1});
                return (gen_el1 + gen_el2).M();'''