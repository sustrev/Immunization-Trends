import pandas as pd
import dash_bootstrap_components as dbc

import os
try:
    os.environ.pop('http_proxy')
    os.environ.pop('https_proxy')
except KeyError:
    pass

import dash
from dash import Dash, html, dcc, Input, Output, State, callback_context

import plotly.graph_objects as go
import plotly.express as px

import filterfx
import visfx

###

# Load in CSV created by datajoin.ipynb
NISPUF_df = pd.read_csv("NISPUF_15_20.csv", low_memory=False)

# For reference, list of all demographic columns in NISPUF_df
demographic_cols = ["AGEGRP", # Age Category of Child (1: 19-23m, 2: 24-29m, 3: 30-35m)
                    "C1R", # Number of People in Household (INT, range 2-8)
                    "CEN_REG", # Census Region (1: NE, 2: MW, 3: S, 4: W)
                    "CHILDNM", # Number of Children Less than 18 Years in Household (1: 1, 2: 2-3, 3: 4+)
                    "CWIC_01", # Child Ever Received WIC Benefits (1: Yes, 2: No, 3: Never Heard Of WIC, 77: Don't Know, 99: Refused)
                    "CWIC_02", # Child Currently Receiving WIC Benefits (1: Yes, 2: No, 77: Don't Know)
                    "EDUC1", # Education of Mother (1: <12 Years, 2: 12 Years, 3: <12 Years, 4: College Grad)
                    "INCPORAR", # Income to Poverty Ratio (FLOAT, MEAN 2.2, MIN 0.5, MAX 3.0)
                    "INCPOV1", # Poverty Status (1: Above Poverty >$75K, 2: Above Poverty <=$75K, 3: Below Poverty, 4: Unknown)
                    "INCQ298A", # Family Income Categories (3: 0-7.5k, 4: 7.5k-10k, 5: 10k-17.5k, 6: 17.5k-20k, 7: 20k-25k, 8: 25k-30k, 9: 30k-35k, 10: 35k-40k, 11: 40k-50k, 12: 50k-60k, 13: 50k-75k, 14: 75k+, 77: Don't Know, 99: Refused)
                    "LANGUAGE", # Language in Which Interview was Conducted (1: English, 2: Spanish, 3: Other)
                    "M_AGEGRP2", # Age of Mother (1: <=29, 2: >=30)
                    "MARITAL2", # Marital Status of Mother (1: Married, 2: All Other)
                    "RACE_K", # Race of Child (1: White, 2: Black, 3: Other/Multiple)
                    "RACEETHK", # Race/Ethnicity of Child (1: Hispanic, 2: Non-Hispanic White, 3: Non-Hispanic Black, 4: Non-Hispanic Other/Multiple)
                    "RENT_OWN", # Home Ownership/Renter (1: Owned, 2: Rented, 3: Other, 77: Don't Know, 99: Refused)
                    "SEX", # Sex of Child (1: Male, 2: Female)
                    "STATE", # True State of Residence (See state_dict, includes states + DC and PR )
                    "INS_STAT", # Combined INS_STAT2_I and INS_STAT_I
                    #"INS_STAT2_I", # Insurance Status (1: Private, 2: Medicaid, 3: Other, 4: Uninsured)
                    #"INS_STAT_I", # Insurance Status (previous code) (1: Private, 2: Medicaid, 3: Other, 4: Uninsured)
                    "INS_BREAK_I", # Continuity of Insurance Coverage Since Birth (1: Currently Insured Sometimes Uninsured, 2: Currently Insured Never Uninsured, 3: Currently Uninsured Sometimes Insured, 4: Never Insured)
                    ]

# For reference, list of all immunization types in NISPUF_df
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

# For reference, dictionary of all valid options for each demographic category
demographic_dict = {"AGEGRP": ["19 - 23 MONTHS", "24 - 29 MONTHS", "30 - 35 MONTHS"],
                        "C1R": ["2", "3", "4", "5", "6", "7", "8+"],
                        "CEN_REG": ["NORTHEAST", "MIDWEST", "SOUTH", "WEST"],
                        "CHILDNM": ["ONE", "TWO OR THREE", "FOUR OR MORE"],
                        "CWIC_01": ["YES", "NO", "NEVER HEARD OF WIC", "DON'T KNOW"],
                        "CWIC_02": ["YES", "NO", "DON'T KNOW"],
                        "EDUC1": ['< 12 YEARS', '12 YEARS', '> 12 YEARS, NON-COLLEGE GRAD', 'COLLEGE GRAD'],
                        "INCPOV1": ['ABOVE POVERTY, > $75K', 'ABOVE POVERTY, <= $75K', 'BELOW POVERTY', 'UNKNOWN'],
                        "INCQ298A": ['$0 - $7500', '$7501 - $10000', '$10001 - $17500', '$17501 - $20000', '$20001 - $25000', '$25001 - $30000', '$30001 - $35000', '$35001 - $40000', '$40001 - $50000', '$50001 - $60000', '$60001 - $75000', '$75001+', "DON'T KNOW", 'REFUSED'],
                        "LANGUAGE": ['ENGLISH', 'SPANISH', 'OTHER'],
                        "M_AGEGRP2": ['<= 29 YEARS', '>= 30 YEARS'],
                        "MARITAL2": ['MARRIED', 'NEVER MARRIED/WIDOWED/DIVORCED/SEPARATED/DECEASED/LIVING WITH PARTNER'],
                        "RACE_K": ['WHITE ONLY', 'BLACK ONLY', 'OTHER + MULTIPLE RACE'],
                        "RACEETHK": ['HISPANIC', 'NON-HISPANIC WHITE ONLY', 'NON-HISPANIC BLACK ONLY', 'NON-HISPANIC OTHER + MULTIPLE RACE'],
                        "RENT_OWN": ['OWNED OR BEING BOUGHT', 'RENTED', 'OTHER ARRANGEMENT', "DON'T KNOW", "REFUSED"],
                        "SEX": ["MALE", "FEMALE"],
                        "INS_STAT": ['PRIVATE INSURANCE', 'ANY MEDICAID', 'OTHER INSURANCE', 'UNINSURED'],
                        "INS_BREAK_I": ['CURRENTLY INSURED BUT UNINSURED AT SOME POINT', 'CURRENTLY INSURED AND NEVER UNINSURED', 'CURRENTLY UNINSURED BUT INSURED AT SOME POINT', 'CURRENTLY UNINSURED AND NEVER INSURED'],
                        "STATE": ["ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", "CONNECTICUT", "DELAWARE", "DISTRICT OF COLUMBIA", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", "SOUTH DAKOTA",  "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING", "PUERTO RICO"]
                        }

# Preload the full dataframe for the immunization-specific comparison graph and initialize comparisons list
full_df = filterfx.full_pct_df(NISPUF_df)
comparisons = [["All Records", full_df]]

# Begin dashboard!
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.title = "Immunization Trends Dashboard"


# Set different aspects of the dashboard to be called within app.layout
def description_card():
    """
    Returns a Div containing dashboard title and descriptions
    """
    return html.Div(
        id="description-card",
        children=[
            html.H3("Immunization Trends"),
            html.Div(
                id="intro",
                children="Explore immunization trends by setting demographic filters, then save filters to add to the comparison graph."
            ),
        ],
    )

def generate_control_card():
    """
    Returns a Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Age Groups"),
            dcc.Dropdown(
                id='agegrp-select',
                options=[{"label": i, "value": i} for i in demographic_dict["AGEGRP"]],
                value=demographic_dict["AGEGRP"][:],
                multi=True,
            ),
            html.P("Select Number of People in Household"),
            dcc.Dropdown(
                id='c1r-select',
                options=[{"label": i, "value": i} for i in demographic_dict["C1R"]],
                value=demographic_dict["C1R"][:],
                multi=True,
            ),
            html.P("Select Census Region"),
            dcc.Dropdown(
                id='cen-reg-select',
                options=[{"label": i, "value": i} for i in demographic_dict["CEN_REG"]],
                value=demographic_dict["CEN_REG"][:],
                multi=True,
            ),
            html.P("Select Number of Minor Children in Household"),
            dcc.Dropdown(
                id='childnm-select',
                options=[{"label": i, "value": i} for i in demographic_dict["CHILDNM"]],
                value=demographic_dict["CHILDNM"][:],
                multi=True,
            ),
            html.P("Select Ever Received WIC Benefits"),
            dcc.Dropdown(
                id='cwic-01-select',
                options=[{"label": i, "value": i} for i in demographic_dict["CWIC_01"]],
                value=demographic_dict["CWIC_01"][:],
                multi=True,
            ),
            html.P("Select Currently Receiving WIC Benefits"),
            dcc.Dropdown(
                id='cwic-02-select',
                options=[{"label": i, "value": i} for i in demographic_dict["CWIC_02"]],
                value=demographic_dict["CWIC_02"][:],
                multi=True,
            ),
            html.P("Select Mother's Education Level"),
            dcc.Dropdown(
                id='educ1-select',
                options=[{"label": i, "value": i} for i in demographic_dict["EDUC1"]],
                value=demographic_dict["EDUC1"][:],
                multi=True,
            ),
            html.P("Select Household Poverty Level"),
            dcc.Dropdown(
                id='incpov1-select',
                options=[{"label": i, "value": i} for i in demographic_dict["INCPOV1"]],
                value=demographic_dict["INCPOV1"][:],
                multi=True,
            ),
            html.P("Select Household Income Level"),
            dcc.Dropdown(
                id='incq298a-select',
                options=[{"label": i, "value": i} for i in demographic_dict["INCQ298A"]],
                value=demographic_dict["INCQ298A"][:],
                multi=True,
            ),
            html.P("Select Language of Interview"),
            dcc.Dropdown(
                id='language-select',
                options=[{"label": i, "value": i} for i in demographic_dict["LANGUAGE"]],
                value=demographic_dict["LANGUAGE"][:],
                multi=True,
            ),
            html.P("Select Mother's Age"),
            dcc.Dropdown(
                id='m-agegrp2-select',
                options=[{"label": i, "value": i} for i in demographic_dict["M_AGEGRP2"]],
                value=demographic_dict["M_AGEGRP2"][:],
                multi=True,
            ),
            html.P("Select Mother's Marital Status"),
            dcc.Dropdown(
                id='marital2-select',
                options=[{"label": i, "value": i} for i in demographic_dict["MARITAL2"]],
                value=demographic_dict["MARITAL2"][:],
                multi=True,
            ),
            html.P("Select Race"),
            dcc.Dropdown(
                id='race-k-select',
                options=[{"label": i, "value": i} for i in demographic_dict["RACE_K"]],
                value=demographic_dict["RACE_K"][:],
                multi=True,
            ),
            html.P("Select Race/Ethnicity"),
            dcc.Dropdown(
                id='raceethk-select',
                options=[{"label": i, "value": i} for i in demographic_dict["RACEETHK"]],
                value=demographic_dict["RACEETHK"][:],
                multi=True,
            ),
            html.P("Select Household Living Situation"),
            dcc.Dropdown(
                id='rent-own-select',
                options=[{"label": i, "value": i} for i in demographic_dict["RENT_OWN"]],
                value=demographic_dict["RENT_OWN"][:],
                multi=True,
            ),
            html.P("Select Sex"),
            dcc.Dropdown(
                id='sex-select',
                options=[{"label": i, "value": i} for i in demographic_dict["SEX"]],
                value=demographic_dict["SEX"][:],
                multi=True,
            ),
            html.P("Select Insurance Status"),
            dcc.Dropdown(
                id='ins-stat-select',
                options=[{"label": i, "value": i} for i in demographic_dict["INS_STAT"]],
                value=demographic_dict["INS_STAT"][:],
                multi=True,
            ),
            html.P("Select Insurance Break Status"),
            dcc.Dropdown(
                id='ins-break-i-select',
                options=[{"label": i, "value": i} for i in demographic_dict["INS_BREAK_I"]],
                value=demographic_dict["INS_BREAK_I"][:],
                multi=True,
            ),
            html.P("Select State"),
            dcc.Dropdown(
                id='state-select',
                options=[{"label": i, "value": i} for i in demographic_dict["STATE"]],
                value=demographic_dict["STATE"][:],
                multi=True,
            ),
        ],
    )

def generate_save_card():
    """
    Returns a Div containing controls for graphs.
    """
    return html.Div(
            id="save_name_card",
            children=[
                html.P('Save Current Demographic Profile'),
                dcc.Textarea(
                    id='text-input',
                    #value="Insert Filter Save Name Here",
                    style={'width': '80%', 'height': '50'},
                ),
                html.Button('Save', id='text-save-button', n_clicks=0),
                html.Div(id='text-save-output', style={'whiteSpace': 'pre-line'})
            ]
    )


def generate_demographic_lines(agegrp_selected, c1r_selected, cen_reg_selected, childnm_selected, cwic_01_selected, cwic_02_selected, educ1_selected, incpov1_selected, incq298a_selected, language_selected, m_agegrp2_selected, marital2_selected, race_k_selected, raceethk_selected, rent_own_selected, sex_selected, ins_stat_selected, ins_break_i_selected, state_selected):
    """
    Takes all demographic filter parameters
    Returns line graph of all immunization types
    """
    filtered_df = filterfx.full_pct_df(filterfx.demog_filter(NISPUF_df, AGEGRP=agegrp_selected, C1R = c1r_selected, CEN_REG = cen_reg_selected, CHILDNM = childnm_selected, CWIC_01 = cwic_01_selected, CWIC_02 = cwic_02_selected, EDUC1 = educ1_selected, INCPOV1 = incpov1_selected, INCQ298A = incq298a_selected, LANGUAGE = language_selected, M_AGEGRP2 = m_agegrp2_selected, MARITAL2 = marital2_selected, RACE_K = race_k_selected, RACEETHK = raceethk_selected, RENT_OWN = rent_own_selected, SEX = sex_selected, INS_STAT = ins_stat_selected, INS_BREAK_I = ins_break_i_selected, STATE = state_selected))
    return visfx.demo_profile(filtered_df, name = "Selected Demographics")

def save_demo_profile(save_name, agegrp_selected, c1r_selected, cen_reg_selected, childnm_selected, cwic_01_selected, cwic_02_selected, educ1_selected, incpov1_selected, incq298a_selected, language_selected, m_agegrp2_selected, marital2_selected, race_k_selected, raceethk_selected, rent_own_selected, sex_selected, ins_stat_selected, ins_break_i_selected, state_selected):
    """
    Takes a snapshot of current demographic profile and saves it to the list
    """
    filtered_df = filterfx.full_pct_df(filterfx.demog_filter(NISPUF_df, AGEGRP=agegrp_selected, C1R = c1r_selected, CEN_REG = cen_reg_selected, CHILDNM = childnm_selected, CWIC_01 = cwic_01_selected, CWIC_02 = cwic_02_selected, EDUC1 = educ1_selected, INCPOV1 = incpov1_selected, INCQ298A = incq298a_selected, LANGUAGE = language_selected, M_AGEGRP2 = m_agegrp2_selected, MARITAL2 = marital2_selected, RACE_K = race_k_selected, RACEETHK = raceethk_selected, RENT_OWN = rent_own_selected, SEX = sex_selected, INS_STAT = ins_stat_selected, INS_BREAK_I = ins_break_i_selected, STATE = state_selected))
    comparisons.append([save_name, filtered_df])
    output = "Current demographics saved as {} for comparison.".format(save_name)
    return output

def generate_comparison_lines(immunization_type):
    """
    Takes saved demographic states
    Returns comparison line graph of one immunization type
    """
    return visfx.compare_lines(comparisons, immunization_type)

def generate_immunization_selector():
    """
    Returns a Div containing immunization selection dropdown
    """
    return html.Div(
        id="immunization-card",
        children=[
            html.P("Select Immunization Type"),
            dcc.Dropdown(
                id='immunization-select',
                options=[{"label": i, "value": i} for i in UTD_cols],
                value=UTD_cols[0],
                multi=False,
            ),
        ],
    )

# Put everything together...
app.layout = html.Div(
    id='app-container',
    children=
    [
        dbc.Row(
            [
                dbc.Col(html.Div(description_card())),
                dbc.Col(html.Div(generate_save_card())),
                dbc.Col(html.Div(generate_immunization_selector())),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(generate_control_card())),
                dbc.Col(html.Div(dcc.Graph(id='demo_graph'))),
                dbc.Col(html.Div(dcc.Graph(id='compare_graph'))),
            ]
        ),
    ]
)

@app.callback(
    Output("demo_graph", "figure"),
    [
        Input("agegrp-select", "value"),
        Input("c1r-select", "value"),
        Input("cen-reg-select", "value"),
        Input("childnm-select", "value"),
        Input("cwic-01-select", "value"),
        Input("cwic-02-select", "value"),
        Input("educ1-select", "value"),
        Input("incpov1-select", "value"),
        Input("incq298a-select", "value"),
        Input("language-select", "value"),
        Input("m-agegrp2-select", "value"),
        Input("marital2-select", "value"),
        Input("race-k-select", "value"),
        Input("raceethk-select", "value"),
        Input("rent-own-select", "value"),
        Input("sex-select", "value"),
        Input("ins-stat-select", "value"),
        Input("ins-break-i-select", "value"),
        Input("state-select", "value"),
    ],
)
def update_demo_lines(agegrp_selected, c1r_selected, cen_reg_selected, childnm_selected, cwic_01_selected, cwic_02_selected, educ1_selected, incpov1_selected, incq298a_selected, language_selected, m_agegrp2_selected, marital2_selected, race_k_selected, raceethk_selected, rent_own_selected, sex_selected, ins_stat_selected, ins_break_i_selected, state_selected):
    filtered_df = filterfx.full_pct_df(filterfx.demog_filter(NISPUF_df, AGEGRP=agegrp_selected, C1R = c1r_selected, CEN_REG = cen_reg_selected, CHILDNM = childnm_selected, CWIC_01 = cwic_01_selected, CWIC_02 = cwic_02_selected, EDUC1 = educ1_selected, INCPOV1 = incpov1_selected, INCQ298A = incq298a_selected, LANGUAGE = language_selected, M_AGEGRP2 = m_agegrp2_selected, MARITAL2 = marital2_selected, RACE_K = race_k_selected, RACEETHK = raceethk_selected, RENT_OWN = rent_own_selected, SEX = sex_selected, INS_STAT = ins_stat_selected, INS_BREAK_I = ins_break_i_selected, STATE = state_selected))
    return visfx.demo_profile(filtered_df, name = "Selected Demographics")

@app.callback(
    Output('text-save-output', 'children'),
    Input('text-save-button', 'n_clicks'),
    State("agegrp-select", "value"),
    State("c1r-select", "value"),
    State("cen-reg-select", "value"),
    State("childnm-select", "value"),
    State("cwic-01-select", "value"),
    State("cwic-02-select", "value"),
    State("educ1-select", "value"),
    State("incpov1-select", "value"),
    State("incq298a-select", "value"),
    State("language-select", "value"),
    State("m-agegrp2-select", "value"),
    State("marital2-select", "value"),
    State("race-k-select", "value"),
    State("raceethk-select", "value"),
    State("rent-own-select", "value"),
    State("sex-select", "value"),
    State("ins-stat-select", "value"),
    State("ins-break-i-select", "value"),
    State("state-select", "value"),
    State('text-input', 'value')
)
def update_save(n_clicks, agegrp_selected, c1r_selected, cen_reg_selected, childnm_selected, cwic_01_selected, cwic_02_selected, educ1_selected, incpov1_selected, incq298a_selected, language_selected, m_agegrp2_selected, marital2_selected, race_k_selected, raceethk_selected, rent_own_selected, sex_selected, ins_stat_selected, ins_break_i_selected, state_selected, value):
    if n_clicks > 0:
        return save_demo_profile(value, agegrp_selected, c1r_selected, cen_reg_selected, childnm_selected, cwic_01_selected, cwic_02_selected, educ1_selected, incpov1_selected, incq298a_selected, language_selected, m_agegrp2_selected, marital2_selected, race_k_selected, raceethk_selected, rent_own_selected, sex_selected, ins_stat_selected, ins_break_i_selected, state_selected)

@app.callback(
    Output('compare_graph', 'figure'),
    Input('immunization-select', 'value')
)
def update_compare_lines(immunization_selected):
    return visfx.compare_lines(comparisons, immunization_selected)

if __name__ == '__main__':
    app.run_server(port=8501)