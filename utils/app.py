import streamlit as st
from streamlit_option_menu import option_menu  # 🆕 Import

from utils.gsheet_utils import load_data_from_gsheet, load_yearly_data
from utils.data_utils import filter_old_records
from utils.ui_utils import show_credit_form, show_debit_form, show_summary
from utils.yearly_overview import show_yearly_overview
from utils.monthly_insights import generate_monthly_insights
from utils.weekly_insights import generate_weekly_insights
from utils.filter_data import filter_data
from utils.ai_insights import show_ai_insights

def run():

    # 📂 Top horizontal menu
    selected = option_menu(
        menu_title=None,
        options=[
            "Credit", "Debit", "Summary", 
            "Weekly Insights", "Monthly Insights", 
            "Yearly Overview", "Filter", "AI Insights"
        ],
        icons=["cash", "credit-card", "bar-chart-line", 
           "calendar-week", "graph-up", "calendar-range", "search", "robot"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        # show_icons=False  # ✅ Only works here
    )

    # Load and prepare data
    df, sheet, spreadsheet = load_data_from_gsheet()
    df = filter_old_records(df)

    # 📦 Route to selected feature
    if selected == "Credit":
        show_credit_form(df, sheet)

    elif selected == "Debit":
        show_debit_form(df, sheet)

    elif selected == "Summary":
        show_summary(load_yearly_data(spreadsheet))

    elif selected == "Weekly Insights":
        generate_weekly_insights(df)

    elif selected == "Monthly Insights":
        generate_monthly_insights(df)

    elif selected == "Yearly Overview":
        show_yearly_overview(load_yearly_data(spreadsheet))

    elif selected == "Filter":
        filter_data(load_yearly_data(spreadsheet))

    elif selected == "AI Insights":
        show_ai_insights(load_yearly_data(spreadsheet))
