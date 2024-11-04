import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

def calculate_life_weeks(birth_date, life_expectancy=90):
    today = datetime.now()
    total_weeks = life_expectancy * 52
    lived_weeks = int((today - birth_date).days / 7)
    remaining_weeks = total_weeks - lived_weeks
    return lived_weeks

def create_memento_mori_calendar(birth_date):
    lived_weeks = calculate_life_weeks(birth_date)
    total_weeks = 90 * 52
    
    weeks_matrix = [[0 for _ in range(52)] for _ in range(90)]
    hover_text = [['' for _ in range(52)] for _ in range(90)]
    
    for i in range(total_weeks):
        row = i // 52
        col = i % 52
        year = row + 1
        week = col + 1
        
        if i < lived_weeks:
            weeks_matrix[row][col] = 1
        hover_text[row][col] = f"Year {year}, Week {week}"
            
    fig = go.Figure(data=go.Heatmap(
        z=weeks_matrix,
        text=hover_text,
        hoverinfo='text',
        colorscale=[[0, '#FFFFFF'], [1, '#000000']],
        showscale=False
    ))
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0, pad=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=800,
        height=600,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            fixedrange=True,
            constrain='domain',
            range=[-0.5, 52.5]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            fixedrange=True,
            scaleanchor='x',
            constrain='domain',
            range=[89.5, -0.5]
        ),
        autosize=False
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Life in Weeks",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
        <style>
        .stApp {
            max-width: 1000px;
            margin: 0 auto;
        }
        .st-emotion-cache-16idsys p {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### Your Life in Weeks")
    st.write("Enter your birth date to see your life visualized in weeks")

    # Date input for birth date
    birth_date = st.date_input(
        "Birth Date",
        min_value=datetime(1900, 1, 1).date(),
        max_value=datetime.now().date(),
        value=datetime(1990, 1, 1).date()
    )

    if birth_date:
        # Convert date to datetime for calculations
        birth_datetime = datetime.combine(birth_date, datetime.min.time())
        
        # Create and display the calendar
        fig = create_memento_mori_calendar(birth_datetime)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Calculate and display some statistics
        lived_weeks = calculate_life_weeks(birth_datetime)
        total_weeks = 90 * 52
        remaining_weeks = total_weeks - lived_weeks
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Weeks Lived", f"{lived_weeks:,}")
        with col2:
            st.metric("Weeks Remaining", f"{remaining_weeks:,}")

if __name__ == "__main__":
    main()