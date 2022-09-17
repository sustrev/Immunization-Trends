import pandas as pd
import numpy as np

UTD_cols = ["P_U12VRC", # Varicella 1+ (0: Not UTD, 1: UTD)
            "P_UTD331", # 3 DT:3 Polio:1 Measles (0: Not UTD, 1: UTD)
            "P_UTD431", # 4 DT:3 Polio:1 Measles (0: Not UTD, 1: UTD)
            "P_UTDHEP", # Hep B (0: Not UTD, 1: UTD)
            "P_UTDHEPA1", # Hep A 1+ (0: Not UTD, 1: UTD)
            "P_UTDHEPA2", # Hep A 2+ (0: Not UTD, 1: UTD)
            "P_UTDHIB", # HIB 3+ (0: Not UTD, 1: UTD)
            "P_UTDHIB_ROUT_S", # HIB 3+, routine/non-shortage (0: Not UTD, 1: UTD)
            "P_UTDHIB_SHORT_S", # HIB 3+, shortage (0: Not UTD, 1: UTD)
            "P_UTDMCV", # Measles 1+ (0: Not UTD, 1: UTD)
            "P_UTDMMX", # Measles-Mumps-Rubella MMR combo 1+ (0: Not UTD, 1: UTD)
            "P_UTDPC3", # Pneumococcal 3+ (0: Not UTD, 1: UTD)
            "P_UTDPCV", # Pneumococcal 4+ (0: Not UTD, 1: UTD)
            "P_UTDPOL", # Polio 3+ (0: Not UTD, 1: UTD)
            "P_UTDROT_S", # Rotavirus 3+ (0: Not UTD, 1: UTD)
            "P_UTDTP3", # DT 3+ (0: Not UTD, 1: UTD)
            "P_UTDTP4", # DT 4+ (0: Not UTD, 1: UTD)
            "PU431331", # 4 DT:3 Polio:1 Measles:3 HIB:3 HepB:1 Var (0: Not UTD, 1: UTD)
            "P_UTD431H31_ROUT_S", # 4:3:1:3:3:1, routine/strict HIB (0: Not UTD, 1: UTD)
            "PU4313313", # 4 DT:3 Polio:1 Measles:3 HIB:3 HepB:1 Var:3 Pneumococcal (0: Not UTD, 1: UTD)
            "P_UTD431H313_ROUT_S", # 4:3:1:3:3:1:3, routine/strict HIB (0: Not UTD, 1: UTD)
            "PU4313314", # 4 DT:3 Polio:1 Measles:3 HIB:3 HepB:1 Var:4 Pneumococcal (0: Not UTD, 1: UTD)
            "P_UTD431H314_ROUT_S", # 4:3:1:3:3:1:4, routine/strict HIB (0: Not UTD, 1: UTD)
            "PUT43133", # 4 DT:3 Polio:1 Measles:3 HIB:3 HepB (0: Not UTD, 1: UTD)
            "P_UTD431H3_ROUT_S", # 4:3:1:3:3, routine/strict HIB (0: Not UTD, 1: UTD)
            "PUTD4313", # 4 DT:3 Polio:1 Measles:3 HIB  (0: Not UTD, 1: UTD)
            "P_UTD431H_ROUT_S", # 4:3:1:3 routine/strict HIB (0: Not UTD, 1: UTD)
            ]

def demog_filter(df, AGEGRP = 'All', C1R = 'All', CEN_REG = 'All', CHILDNM = 'All', CWIC_01 = 'All', CWIC_02 = 'All', EDUC1 = 'All', INCPORAR = 'All', INCPOV1 = 'All', INCQ298A = 'All', LANGUAGE = 'All', M_AGEGRP2 = 'All', MARITAL2 = 'All', RACE_K = 'All', RACEETHK = 'All', RENT_OWN = 'All', SEX = 'All', STATE = 'All', INS_STAT = 'All', INS_BREAK_I = 'All'):
    
    if AGEGRP == 'All':
        df = df
    elif AGEGRP == []:
        df = df
    else:
        to_keep = AGEGRP
        df = df[df.AGEGRP.isin(to_keep)]

    if C1R == 'All':
        df = df
    elif C1R == []:
        df = df
    else:
        to_keep = C1R
        df = df[df.C1R.isin(to_keep)]

    if CEN_REG == 'All':
        df = df
    elif CEN_REG == []:
        df = df
    else:
        to_keep = CEN_REG
        df = df[df.CEN_REG.isin(to_keep)]

    if CHILDNM == 'All':
        df = df
    elif CHILDNM == []:
        df = df
    else:
        to_keep = CHILDNM
        df = df[df.CHILDNM.isin(to_keep)]

    if CWIC_01 == 'All':
        df = df
    elif CWIC_01 == []:
        df = df
    else:
        to_keep = CWIC_01
        df = df[df.CWIC_01.isin(to_keep)]

    if CWIC_02 == 'All':
        df = df
    elif CWIC_02 == []:
        df = df
    else:
        to_keep = CWIC_02
        df = df[df.CWIC_02.isin(to_keep)]

    if EDUC1 == 'All':
        df = df
    elif EDUC1 == []:
        df = df
    else:
        to_keep = EDUC1
        df = df[df.EDUC1.isin(to_keep)]
    
    if INCPORAR == 'All':
        df = df
    elif INCPORAR == []:
        df = df
    else:
        to_keep = INCPORAR
        df = df[df.INCPORAR.isin(to_keep)]

    if INCPOV1 == 'All':
        df = df
    elif INCPOV1 == []:
        df = df
    else:
        to_keep = INCPOV1
        df = df[df.INCPOV1.isin(to_keep)]

    if INCQ298A == 'All':
        df = df
    elif INCQ298A == []:
        df = df
    else:
        to_keep = INCQ298A
        df = df[df.INCQ298A.isin(to_keep)]
    
    if LANGUAGE == 'All':
        df = df
    elif LANGUAGE == []:
        df = df
    else:
        to_keep = LANGUAGE
        df = df[df.LANGUAGE.isin(to_keep)]
    
    if M_AGEGRP2 == 'All':
        df = df
    elif M_AGEGRP2 == []:
        df = df
    else:
        to_keep = M_AGEGRP2
        df = df[df.M_AGEGRP2.isin(to_keep)]

    if MARITAL2 == 'All':
        df = df
    elif MARITAL2 == []:
        df = df
    else:
        to_keep = MARITAL2
        df = df[df.MARITAL2.isin(to_keep)]

    if RACE_K == 'All':
        df = df
    elif RACE_K == []:
        df = df
    else:
        to_keep = RACE_K
        df = df[df.RACE_K.isin(to_keep)]

    if RACEETHK == 'All':
        df = df
    elif RACEETHK == []:
        df = df
    else:
        to_keep = RACEETHK
        df = df[df.RACEETHK.isin(to_keep)]

    if RENT_OWN == 'All':
        df = df
    elif RENT_OWN == []:
        df = df
    else:
        to_keep = RENT_OWN
        df = df[df.RENT_OWN.isin(to_keep)]

    if SEX == 'All':
        df = df
    elif SEX == []:
        df = df
    else:
        to_keep = SEX
        df = df[df.SEX.isin(to_keep)]

    if STATE == 'All':
        df = df
    elif STATE == []:
        df = df
    else:
        to_keep = STATE
        df = df[df.STATE.isin(to_keep)]

    if INS_STAT == 'All':
        df = df
    elif INS_STAT == []:
        df = df
    else:
        to_keep = INS_STAT
        df = df[df.INS_STAT.isin(to_keep)]

    if INS_BREAK_I == 'All':
        df = df
    elif INS_BREAK_I == []:
        df = df
    else:
        to_keep = INS_BREAK_I
        df = df[df.INS_BREAK_I.isin(to_keep)]

    return df

def utd_calc(df, immunization_type, group = ['YEAR']):
    df['COUNTER'] = 1
    pivot_df = df.pivot_table(index=group, columns = immunization_type, values='COUNTER', aggfunc=np.sum)
    pivot_df.reset_index(inplace=True)
    pivot_df[immunization_type] = pivot_df["UTD"] / (pivot_df["NOT UTD"] + pivot_df["UTD"])
    pivot_df.name = immunization_type

    return pivot_df

def utd_df(pivot_df_list):
    for d in pivot_df_list:
        d.drop(columns=["UTD", "NOT UTD"], inplace=True)
    UTD_df = pd.concat(pivot_df_list, axis = 1)
    clean_df = UTD_df.loc[:,~UTD_df.columns.duplicated()].copy()

    return clean_df

def full_pct_df(df, group = ["YEAR"]):
    dfs = []
    for imm in UTD_cols:
        dfs.append(utd_calc(df, imm, group))
    return utd_df(dfs).set_index("YEAR")