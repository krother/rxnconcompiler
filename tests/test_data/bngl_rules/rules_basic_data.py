#!/usr/bin/env python

"""
rules_basic_data.py contains dictionary with basic reactions. 

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}

It anables to check whether rxncon input produces correct bngl rules code.
"""

# TODO: Relocalisation reactions are not tested yet.

REACTIONS_DATA = {
# basic reactions without contingencies.
'Kinase_P+_Target1': {
    'Rules':[
    'Kinase + Target1(Kinase~U) -> Kinase + Target1(Kinase~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']},

'Phosphatase_P-_Target1': {
    'Rules':[
    'Phosphatase + Target1(Phosphatase~P) -> Phosphatase + Target1(Phosphatase~U)'],
    'Tags': [
    1, 'P-', 'no contingencies']},

'Kinase_AP_Kinase': {
    'Rules':[
    'Kinase + Kinase(Kinase~U) -> Kinase + Kinase(Kinase~P)'],
    'Tags': [
    1, 'AP', 'no contingencies']},

'PDonor_PT_PAcceptor': {

'Rules':[
'PDonor(PAcceptor~P) + PAcceptor(PDonor~U) -> PDonor(PAcceptor~U) + PAcceptor(PDonor~P)'],
'Tags': [
1, 'PT', 'no contingencies']},


'Enzyme_GEF_GProt': {
    'Rules':[
    'Enzyme + GProt(Enzyme~U) -> Enzyme + GProt(Enzyme~P)'],
    'Tags': [
    1, 'GEF', 'no contingencies']},

'Enzyme_GAP_GProt': {
    'Rules':[
    'Enzyme + GProt(Enzyme~P) -> Enzyme + GProt(Enzyme~U)'],
    'Tags': [
    1, 'GAP', 'no contingencies']},

'EnzymeUb_Ub+_TargetUb': {
    'Rules':[
    'EnzymeUb + TargetUb(EnzymeUb~U) -> EnzymeUb + TargetUb(EnzymeUb~Ub)'],
    'Tags': [
    1, 'Ub+', 'no contingencies']},

'EnzymeUb_Ub-_TargetUb': {
    'Rules':[
    'EnzymeUb + TargetUb(EnzymeUb~Ub) -> EnzymeUb + TargetUb(EnzymeUb~U)'],
    'Tags': [
    1, 'Ub-', 'no contingencies']},

'EnzymeCUT_CUT_TargetCUT': {
    'Rules':[
    'EnzymeCUT + TargetCUT(EnzymeCUT~U) -> EnzymeCUT + TargetCUT(EnzymeCUT~Truncated)'],
    'Tags': [
    1, 'CUT', 'no contingencies']},

'A_P+_B': {
    'Rules':[
    'A + B(A~U) -> A + B(A~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']},

'A_ppi_B': {
    'Rules':[
    'A(AssocB) + B(AssocA) <-> A(AssocB!1).B(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

'Ligand_i_Receptor': {
    'Rules':[
    'Ligand(AssocReceptor) + Receptor(AssocLigand) <-> Ligand(AssocReceptor!1).Receptor(AssocLigand!1)'],
    'Tags': [
    1, 'i', 'no contingencies']}, 

'TF_BIND_DNA': {
    'Rules':[
    'TF(AssocDNA) + DNA(AssocTF) <-> DNA(AssocTF!1).TF(AssocDNA!1)'],
    'Tags': [
    1, 'BIND', 'no contingencies']},

'PolII_Trsc_Gene': {
    'Rules':[
    'PolII -> PolII + GenemRNA'],
    'Tags': [
    1, 'TRSC', 'no contingencies']},

'Ribo_TRSL_Gene': {
    'Rules':[
    'Ribo + GenemRNA -> Ribo + GenemRNA + Gene'],
    'Tags': [
    1, 'TRSC', 'no contingencies']},

'Proteasome_DEG_Protein': {
    'Rules':[
    'Proteasome + Protein -> Proteasome'],
    'Tags': [
    1, 'DEG', 'no contingencies']},

'ProtA_[a]_ipi_ProtA_[b]': {
    'Rules':[
    'ProtA(a,b) <-> ProtA(a!1,b!1)'],
    'Tags': [
    1, 'ipi', 'no contingencies']}, 

'Sink_PRODUCE_Protein': {
    'Rules':[
    'Sink -> Sink + Protein'],
    'Tags': [
    1, 'PRODUCE', 'no contingencies']},

'Sink_CONSUME_Protein': {
    'Rules':[
    'Sink + Protein -> Sink'],
    'Tags': [
    1, 'CONSUME', 'no contingencies']},
}



CONTINGENCIES_DATA = {
    # basic reactions with contingencies.
    'A_ppi_C': {
    'Rules':[
    'A(AssocC) + C(AssocA) <-> A(AssocC!1).C(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

    'A_ppi_B; ! A--C': {
    'Rules':[
    'A(AssocB,AssocC!1).C(AssocA!1) + B(AssocA) <-> A(AssocB!2,AssocC!1).B(AssocA!2).C(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'X_p-_A_[Z] \n A_ppi_B; ! A_[Z]-{P}': {
    'Rules':[
    'A(Z~P,AssocB) + B(AssocA) <-> A(Z~P,AssocB!1).B(AssocA!1)',
    'X + A(Z~P,AssocB!1).B(AssocA!1) -> X + A(Z~U,AssocB) + B(AssocA)',
    'X + A(Z~P,AssocB) -> X + A(Z~U,AssocB)'],
    'Tags': [
    1, 'p-', 'contingencies']},

    'Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2 \n Ste20_[KD+CRIB]_ppi_Ste20_[KD+CRIB]; x Cdc42_[ED]--Ste20_[CRIB]': {
    'Rules':[
    'Cdc42(GnP~P,ED) + PIP2(AssocSte20!2).Ste20(BR!2,CRIB,KD+CRIB!1).Ste20(KD+CRIB!1) -> Cdc42(GnP~P,ED!1).PIP2(AssocSte20!2).Ste20(BR!2,CRIB!1,KD+CRIB) + Ste20(KD+CRIB)',
    'Cdc42(GnP~P,ED) + PIP2(AssocSte20!1).Ste20(BR!1,CRIB,KD+CRIB) <-> Cdc42(GnP~P,ED!1).PIP2(AssocSte20!2).Ste20(BR!2,CRIB!1,KD+CRIB)',
    'Cdc42(GnP~P,ED) + Ste20(BR,CRIB,KD+CRIB!1).Ste20(KD+CRIB!1) -> Cdc42(GnP~P,ED!1).Ste20(BR,CRIB!1,KD+CRIB) + Ste20(KD+CRIB)',
    'Cdc42(GnP~P,ED) + Ste20(BR,CRIB,KD+CRIB) <-> Cdc42(GnP~P,ED!1).Ste20(BR,CRIB!1,KD+CRIB)',
    'Ste20(CRIB,KD+CRIB) + Ste20(CRIB,KD+CRIB) <-> Ste20(CRIB,KD+CRIB!1).Ste20(CRIB,KD+CRIB!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Swi4_BIND_SCBG1; x Swi4_[n]--Swi4_[c] \n Swi4_[n]_ppi_Swi4_[c]':{
    'Rules':[
    'SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,n) + SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,c) -> Swi4(AssocSCBG1,n!1).Swi4(AssocSCBG1,c!1) + SCBG1(AssocSwi4) + SCBG1(AssocSwi4)',
    'Swi4(AssocSCBG1,n) + Swi4(AssocSCBG1,c) <-> Swi4(AssocSCBG1,n!1).Swi4(AssocSCBG1,c!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Swi4_BIND_SCBFKS2; x Swi4_[n]--Swi4_[c] \n Swi4_BIND_SCBG1; x Swi4_[n]--Swi4_[c] \n Swi4_[n]_ppi_Swi4_[c]':{
    'Rules':[
    'SCBFKS2(AssocSwi4!1).SCBG1(AssocSwi4!2).Swi4(AssocSCBFKS2!1,AssocSCBG1!2,n) + SCBFKS2(AssocSwi4!1).SCBG1(AssocSwi4!2).Swi4(AssocSCBFKS2!1,AssocSCBG1!2,c) -> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1) + SCBFKS2(AssocSwi4) + SCBFKS2(AssocSwi4) + SCBG1(AssocSwi4) + SCBG1(AssocSwi4)',
    'SCBFKS2(AssocSwi4!1).Swi4(AssocSCBFKS2!1,AssocSCBG1,n) + SCBFKS2(AssocSwi4!1).Swi4(AssocSCBFKS2!1,AssocSCBG1,c) -> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1) + SCBFKS2(AssocSwi4) + SCBFKS2(AssocSwi4)',
    'SCBG1(AssocSwi4!1).Swi4(AssocSCBFKS2,AssocSCBG1!1,n) + SCBG1(AssocSwi4!1).Swi4(AssocSCBFKS2,AssocSCBG1!1,c) -> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1) + SCBG1(AssocSwi4) + SCBG1(AssocSwi4)',
    'Swi4(AssocSCBFKS2,AssocSCBG1,n) + Swi4(AssocSCBFKS2,AssocSCBG1,c) <-> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Sho1_[Cyt]_ppi_Ste11; ! <complex>; k+ Hkr1_[TMD]--Sho1_[TMD]\n <complex>; AND Opy_[BD:Ste50]--Ste50_[RA]; AND Ste11_[SAM]--Ste50_[SAM] \n Ste5_[MEKK]_ppi_Ste11; x Sho1_[Cyt]--Ste11':{
    'Rules':[
    'Hkr1(TMD!1).Sho1(Cyt,TMD!1) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5!3,SAM!2).Ste5(MEKK!3).Ste50(RA!1,SAM!2) -> Hkr1(TMD!4).Opy(BDSte50!1).Sho1(Cyt!3,TMD!4).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) + Ste5(MEKK)',
    'Hkr1(TMD!1).Sho1(Cyt,TMD!1) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) <-> Hkr1(TMD!4).Opy(BDSte50!1).Sho1(Cyt!3,TMD!4).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2)',
    'Sho1(Cyt,TMD) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5!3,SAM!2).Ste5(MEKK!3).Ste50(RA!1,SAM!2) -> Opy(BDSte50!1).Sho1(Cyt!3,TMD).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) + Ste5(MEKK)',
    'Sho1(Cyt,TMD) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) <-> Opy(BDSte50!1).Sho1(Cyt!3,TMD).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'ProtC_ppi_ProtA; ! ProtC_[Gnp]-{P}; ! ProtA_[a]--[b]': {
    'Rules':[
    'ProtC(Gnp~P,AssocProtA) + ProtA(AssocProtC,a!1,b!1) <-> ProtA(AssocProtC!1,a!2,b!2).ProtC(Gnp~P,AssocProtA!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']},

    'ProtC_ppi_ProtA; ! ProtC_[Gnp]-{P}; x ProtA_[a]--[b]': {
    'Rules':[
    'ProtC(Gnp~P,AssocProtA) + ProtA(AssocProtC,a,b) <-> ProtA(AssocProtC!1,a,b).ProtC(Gnp~P,AssocProtA!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']}

}


DATA = [REACTIONS_DATA, CONTINGENCIES_DATA]