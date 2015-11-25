#!/usr/bin/env python

"""
rule_geometry_data.py contains dictionaries with examples of rules with 
with boolean contingencies that define geometry of a complex.
(e.g. <C1>; 1--2 Ste7--Ste11). 

One dict represents single system, that should run in BioNetGen.
{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

GEOMETRY = {
"""Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Comp>
<Comp>; OR <C1>; OR <C2>
<C1>; 1--2 Ste7--Ste11
<C2>; 1--2 Ste5_[MEKK]--Ste11; 3--4 Ste5_[MEK]--Ste7; 1--3 Ste5_[BDSte5]--Ste5_[BDSte5]""": {
    'Rules':[
    'Ste11(AssocSte7!1).Ste7(ALS359~U,AssocSte11!1) -> Ste11(AssocSte7!1).Ste7(ALS359~P,AssocSte11!1)',
    #'Ste11(AssocSte5!3).Ste5(BDSte5!2,MEKK!3).Ste5(BDSte5!2,MEK!1).Ste7(ALS359~U,AssocSte11,AssocSte5!1) -> Ste11(AssocSte5!3).Ste5(BDSte5!2,MEKK!3).Ste5(BDSte5!2,MEK!1).Ste7(ALS359~P,AssocSte11,AssocSte5!1)'],
                        # the numbering changed a bit through the new indexing during the tree building step and sorting step later
    'Ste11(AssocSte5!2).Ste5(BDSte5!3,MEK!1).Ste5(BDSte5!3,MEKK!2).Ste7(ALS359~U,AssocSte11,AssocSte5!1) -> Ste11(AssocSte5!2).Ste5(BDSte5!3,MEK!1).Ste5(BDSte5!3,MEKK!2).Ste7(ALS359~P,AssocSte11,AssocSte5!1)'],
    'Tags': [
    1, 'P+', 'contingencies', '!', 'bool', 'defined geometry']},

'Ste7_ppi_Ste11': {
    'Rules':[
    'Ste7(AssocSte11) + Ste11(AssocSte7) <-> Ste11(AssocSte7!1).Ste7(AssocSte11!1)'],
    'Tags': [
    1, 'ppi', 'Ste7', 'Ste11', 'no contingencies']},

'Ste5_[MEKK]_ppi_Ste11': {
    'Rules':[
    'Ste5(MEKK) + Ste11(AssocSte5) <-> Ste11(AssocSte5!1).Ste5(MEKK!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste11', 'no contingencies']},

'Ste5_[MEK]_ppi_Ste7': {
    'Rules':[
    'Ste5(MEK) + Ste7(AssocSte5) <-> Ste5(MEK!1).Ste7(AssocSte5!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste7', 'no contingencies']},

'Ste5_[BDSte5]_ppi_Ste5_[BDSte5]': {
    'Rules':[
    'Ste5(BDSte5) + Ste5(BDSte5) <-> Ste5(BDSte5!1).Ste5(BDSte5!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'no contingencies', 'homodimer']},

'''A_ppi_E; ! <comp>
        <comp>; 5--25 A--B
        <comp>; 25--7 B--B
        <comp>; 7--8 B--C
        <comp>; 25--9 B--D
        <comp>; 5--10 A--F
        <comp>; 10--11 F--B
        <comp>; 11--12 B--G''': {
    'Rules':[
    'A(AssocB!7,AssocE,AssocF!3).B(AssocA!7,AssocB!6,AssocD!4).B(AssocB!6,AssocC!5).B(AssocF!2,AssocG!1).C(AssocB!5).D(AssocB!4).F(AssocA!3,AssocB!2).G(AssocB!1) + E(AssocA) <-> A(AssocB!8,AssocE!4,AssocF!3).B(AssocA!8,AssocB!7,AssocD!5).B(AssocB!7,AssocC!6).B(AssocF!2,AssocG!1).C(AssocB!6).D(AssocB!5).E(AssocA!4).F(AssocA!3,AssocB!2).G(AssocB!1)'],
    'Tags': [
    1, 'ppi','contingencies', '!', 'bool', 'defined geometry']},
"""A_ppi_E; ! <comp>
    <comp>; 5--25 A--B
    <comp>; 25--7 B--B
    <comp>; 7--8 B--C
    <comp>; 25--9 B--D
    <comp>; 5--10 A--F
    <comp>; 10--11 F--B
    <comp>; 11--12 B--G
    A_ppi_E; ! <comp2>
    <comp2>; AND A--B
    <comp2>; AND B--C
    <comp2>; AND B--B
    <comp2>; AND B--G""": {
    'Rules':[
    'A(AssocB!9,AssocE,AssocF!4).B(AssocA!9,AssocB!8,AssocC!7,AssocD!5,AssocG!2).B(AssocB!8,AssocC!6).B(AssocF!3,AssocG!1).C(AssocB!7).C(AssocB!6).D(AssocB!5).F(AssocA!4,AssocB!3).G(AssocB!2).G(AssocB!1) + E(AssocA) <-> A(AssocB!10,AssocE!5,AssocF!4).B(AssocA!10,AssocB!9,AssocC!8,AssocD!6,AssocG!2).B(AssocB!9,AssocC!7).B(AssocF!3,AssocG!1).C(AssocB!8).C(AssocB!7).D(AssocB!6).E(AssocA!5).F(AssocA!4,AssocB!3).G(AssocB!2).G(AssocB!1)'],
    'Tags': [
    1, 'ppi','contingencies', '!', 'bool', 'defined geometry']},

    """A_ppi_E; ! <comp>
        <comp>; 5--25 A--B
        <comp>; 25--7 B--B
        <comp>; 7--8 B--C
        <comp>; 25--9 B--D
        <comp>; 5--10 A--F
        <comp>; 10--11 F--B
        <comp>; 11--12 B--G
        <comp>; 11 B_[x]-{P}
        <comp>; 7 B_[y]-{P}
        """: {
    'Rules':[
    'A(AssocB!7,AssocE,AssocF!3).B(AssocA!7,AssocB!6,AssocD!4).B(y~P,AssocB!6,AssocC!5).B(x~P,AssocF!2,AssocG!1).C(AssocB!5).D(AssocB!4).F(AssocA!3,AssocB!2).G(AssocB!1) + E(AssocA) <-> A(AssocB!8,AssocE!4,AssocF!3).B(AssocA!8,AssocB!7,AssocD!5).B(y~P,AssocB!7,AssocC!6).B(x~P,AssocF!2,AssocG!1).C(AssocB!6).D(AssocB!5).E(AssocA!4).F(AssocA!3,AssocB!2).G(AssocB!1)'],
    'Tags': [
    1, 'ppi','contingencies', '!', 'bool', 'defined geometry']},

# the same as befor but the modifications are defined first
    """A_ppi_E; ! <comp>
        <comp>; 11 B_[x]-{P}
        <comp>; 7 B_[y]-{P}
        <comp>; 5--25 A--B
        <comp>; 25--7 B--B
        <comp>; 7--8 B--C
        <comp>; 25--9 B--D
        <comp>; 5--10 A--F
        <comp>; 10--11 F--B
        <comp>; 11--12 B--G

        """: {
    'Rules':[
    'A(AssocB!7,AssocE,AssocF!3).B(AssocA!7,AssocB!6,AssocD!4).B(y~P,AssocB!6,AssocC!5).B(x~P,AssocF!2,AssocG!1).C(AssocB!5).D(AssocB!4).F(AssocA!3,AssocB!2).G(AssocB!1) + E(AssocA) <-> A(AssocB!8,AssocE!4,AssocF!3).B(AssocA!8,AssocB!7,AssocD!5).B(y~P,AssocB!7,AssocC!6).B(x~P,AssocF!2,AssocG!1).C(AssocB!6).D(AssocB!5).E(AssocA!4).F(AssocA!3,AssocB!2).G(AssocB!1)'],
    'Tags': [
    1, 'ppi','contingencies', '!', 'bool', 'defined geometry']},

# simple example for a cis p+
    #Tree:   B <- this B gets p+
    #       / \
    #      B   A
     """A_p+_B; ! <cis>
            <cis>; 1--2 B--B
            <cis>; 1--3 B--A"""
        : {
    'Rules':[
    'A(AssocB!2).B(A~U,AssocA!2,AssocB!1).B(AssocB!1) -> A(AssocB!2).B(A~P,AssocA!2,AssocB!1).B(AssocB!1)'],
    'Tags': [
    1, 'p+','contingencies', '!', 'bool', 'defined geometry']},

#simple exa,ple for a trans p+
    #Tree:  B <- this be gets p+
    #       |
    #       B
    #       |
    #       A
     """A_p+_B; ! <trans>
        <trans>; 1--2 B--B
        <trans>; 2--3 B--A"""
        : {
    'Rules':[
    'A(AssocB!1).B(A~U,AssocB!2).B(AssocA!1,AssocB!2) -> A(AssocB!1).B(A~P,AssocB!2).B(AssocA!1,AssocB!2)'],
    'Tags': [
    1, 'p+','contingencies', '!', 'bool', 'defined geometry']},

# more complex cis p+
    #Tree:  B  <- this gets p+
    #      / \
    #     A   C
    #         | <- at domain b
    #         B
    """A_p+_B; ! <cis>
        <cis>; 1--3 B--A
        <cis>; 1--4 B--C
        <cis>; 4--2 C_[b]--B""": {
    'Rules':[
    'A(AssocB!3).B(A~U,AssocA!3,AssocC!2).B(AssocC!1).C(AssocB!2,b!1) -> A(AssocB!3).B(A~P,AssocA!3,AssocC!2).B(AssocC!1).C(AssocB!2,b!1)'],
    'Tags': [
    1, 'p+','contingencies', '!', 'bool', 'defined geometry']},

    ##Tree:  B  <- this gets p+
    #      / \
    #     A   C
    #     | <- at domain b
    #     B
    """A_p+_B; ! <cis>
        <cis>; 1--3 B--A
        <cis>; 1--4 B--C
        <cis>; 3--2 A_[b]--B""": {
    'Rules':[
    'A(AssocB!3,b!2).B(A~U,AssocA!3,AssocC!1).B(AssocA!2).C(AssocB!1) -> A(AssocB!3,b!2).B(A~P,AssocA!3,AssocC!1).B(AssocA!2).C(AssocB!1)'],
    'Tags': [
    1, 'p+','contingencies', '!', 'bool', 'defined geometry']},
# more complex trans p+
    #Tree: B <- this gets p+
    #      |
    #      C
    #      | <- at domain b
    #      B
    #      |
    #      A
    """A_p+_B; ! <trans>
        <trans>; 2--3 B--A
        <trans>; 1--4 B--C
        <trans>; 4--2 C_[b]--B""": {
    'Rules':[
    'A(AssocB!3).B(A~U,AssocC!2).B(AssocA!3,AssocC!1).C(AssocB!2,b!1) -> A(AssocB!3).B(A~P,AssocC!2).B(AssocA!3,AssocC!1).C(AssocB!2,b!1)'],
    'Tags': [
    1, 'p+','contingencies', '!', 'bool', 'defined geometry']},

    #Tree: B <- this gets p+
    #      |
    #      B
    #     / \
    #    A   C
    """A_p+_B; ! <trans>
        <trans>; 2--3 B--A
        <trans>; 1--2 B--B
        <trans>; 4--2 C--B""": {
    'Rules':[
    'A(AssocB!2).B(A~U,AssocB!3).B(AssocA!2,AssocB!3,AssocC!1).C(AssocB!1) -> A(AssocB!2).B(A~P,AssocB!3).B(AssocA!2,AssocB!3,AssocC!1).C(AssocB!1)'],
    'Tags': [
    1, 'p+','contingencies', '!', 'bool', 'defined geometry']},
}


DATA = [GEOMETRY]
