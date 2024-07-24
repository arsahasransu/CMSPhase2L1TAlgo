calculate_invM = '''TLorentzVector gen_el1, gen_el2;
                gen_el1.SetPtEtaPhiM({0}[0], {1}[0], {2}[0], {3});
                gen_el2.SetPtEtaPhiM({0}[1], {1}[1], {2}[1], {3});
                return (gen_el1 + gen_el2).M();'''