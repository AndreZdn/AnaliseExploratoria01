import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================================
# 1. CONFIGURAÇÃO INICIAL E FILTRO DE TEMA (LIGHT / DARK)
# =====================================================================
st.set_page_config(page_title="World Happiness Dashboard", layout="wide", initial_sidebar_state="expanded")

# Captura o estado do modo escuro logo no início da barra lateral
with st.sidebar:
    st.title("⚙️ Filtros Globais")
    modo_escuro = st.toggle("🌙 Modo Escuro", value=False)
    st.divider()

# Definição dinâmica da paleta de cores baseado no toggle
if modo_escuro:
    COR_FUNDO = "#0F172A"          
    COR_CARD = "#1E293B"           
    COR_SIDEBAR = "#1E293B"        
    COR_TEXTO_PRINCIPAL = "#F8FAFC" 
    COR_TEXTO_MUTED = "#94A3B8"     
    COR_GRID = "#334155"           
    # Novas variáveis forçadas para os inputs
    COR_WIDGET_BG = "#334155"
    COR_WIDGET_BORDER = "#475569"
    COR_DROPDOWN_BG = "#1E293B"
else:
    COR_FUNDO = "#FAFAF7"          
    COR_CARD = "#FFFFFF"           
    COR_SIDEBAR = "#FFFFFF"        
    COR_TEXTO_PRINCIPAL = "#1F2937" 
    COR_TEXTO_MUTED = "#6B7280"     
    COR_GRID = "#E5E7EB"           
    # Novas variáveis forçadas para os inputs
    COR_WIDGET_BG = "#FFFFFF"
    COR_WIDGET_BORDER = "#D1D5DB"
    COR_DROPDOWN_BG = "#FFFFFF"

# Injeção do CSS ULTRA-ESPECÍFICO
st.markdown(f"""
<style>
    /* 1. FUNDO PRINCIPAL E BARRA SUPERIOR BRANCA (HEADER) */
    .stApp {{
        background-color: {COR_FUNDO} !important;
    }}
    header[data-testid="stHeader"] {{
        background-color: {COR_FUNDO} !important; 
    }}
    
    /* Ataca ESPECIFICAMENTE o conteúdo dentro dos botões do cabeçalho */
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] button span,
    header[data-testid="stHeader"] button p {{
        color: {COR_TEXTO_PRINCIPAL} !important;
    }}
    
    /* Garante que os SVGs (ícones do GitHub, Estrela, etc) sejam preenchidos com a cor correta */
    header[data-testid="stHeader"] button svg,
    header[data-testid="stHeader"] button svg path {{
        fill: {COR_TEXTO_PRINCIPAL} !important;
        color: {COR_TEXTO_PRINCIPAL} !important;
    }}
    /* 2. BARRA LATERAL (Fundo, textos e divisória) */
    section[data-testid="stSidebar"] {{
        background-color: {COR_SIDEBAR} !important;
        border-right: 1px solid {COR_GRID} !important;
    }}
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div {{
        color: {COR_TEXTO_PRINCIPAL} !important;
    }}
    section[data-testid="stSidebar"] .stSlider div {{
        color: {COR_TEXTO_MUTED} !important;
    }}

    /* 3. TÍTULOS E TEXTOS NO CORPO PRINCIPAL */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label {{
        color: {COR_TEXTO_PRINCIPAL} !important;
    }}
    .stMarkdown p, caption {{
        color: {COR_TEXTO_MUTED} !important;
    }}

    /* 4. KPIs - CORREÇÃO DE LEITURA (Métricas) */
    div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] * {{
        color: #F97316 !important;
        font-size: 2.2rem !important;
        font-weight: bold !important;
    }}
    div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] * {{
        color: {COR_TEXTO_MUTED} !important;
    }}
    div[data-testid="stMetricDelta"] > div, div[data-testid="stMetricDelta"] svg {{
        color: {COR_TEXTO_MUTED} !important;
        fill: {COR_TEXTO_MUTED} !important;
    }}

    /* 5. CARDS (Bordas arredondadas e sombras) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border: none !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, {0.3 if modo_escuro else 0.04}) !important;
        background-color: {COR_CARD} !important; 
        border-radius: 16px !important;
    }}

    /* 6. ESTILIZANDO AS ABAS (TABS) */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {COR_CARD} !important;
        padding: 5px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        border-bottom: none;
        gap: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {COR_TEXTO_MUTED} !important;
        font-weight: 600;
        border-bottom: 3px solid transparent;
    }}
    .stTabs [aria-selected="true"] {{
        color: #F97316 !important;
        border-bottom-color: #F97316 !important;
    }}

    /* 7. WIDGETS (Inputs, Multiselect e Tags) */
    div[data-baseweb="select"] > div {{
        background-color: {COR_WIDGET_BG} !important;
        border-color: {COR_WIDGET_BORDER} !important;
    }}
    div[role="listbox"] {{
        background-color: {COR_DROPDOWN_BG} !important;
    }}
    /* Corrigindo as "pílulas" dos países selecionados para ficarem laranja com texto branco */
    span[data-baseweb="tag"] {{
        background-color: #F97316 !important;
        color: #FFFFFF !important;
    }}
    span[data-baseweb="tag"] svg {{
        fill: #FFFFFF !important; /* Pinta o ícone do Xzinho de branco */
    }}

    /* 8. BOTÃO DE AÇÃO PRINCIPAL (Aplicar Filtros) */
    div[data-testid="stButton"] button {{
        background-color: #F97316 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease;
    }}
    div[data-testid="stButton"] button:hover {{
        background-color: #EA580C !important;
        color: #FFFFFF !important;
        border: none !important;
    }}

    /* 9. OCULTAR MENUS PADRÕES */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

PALETA_QUENTE = ['#F97316', '#FB923C', '#F59E0B', '#FCD34D', '#E76F51', '#F4A261']

# Função auxiliar para limpar e adaptar os gráficos Plotly ao tema ativo
def clean_chart(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(color=COR_TEXTO_PRINCIPAL)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COR_GRID, title_font=dict(color=COR_TEXTO_PRINCIPAL), tickfont=dict(color=COR_TEXTO_MUTED))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COR_GRID, title_font=dict(color=COR_TEXTO_PRINCIPAL), tickfont=dict(color=COR_TEXTO_MUTED))
    
    if hasattr(fig.layout, 'coloraxis') and fig.layout.coloraxis.colorbar:
        fig.layout.coloraxis.colorbar.title.font.color = COR_TEXTO_PRINCIPAL
        fig.layout.coloraxis.colorbar.tickfont.color = COR_TEXTO_MUTED
        
    return fig

# =====================================================================
# 2. CARREGAMENTO DOS DADOS (CACHE)
# =====================================================================
@st.cache_data
def load_data():
    return pd.read_csv('world_happiness_gold_pt.csv')

df = load_data()

# =====================================================================
# 3. CONTINUAÇÃO DA BARRA LATERAL (FILTROS)
# =====================================================================
with st.sidebar:
    st.markdown("Use os controles abaixo para interagir com as abas do painel.")
    
    st.subheader("Filtro Temporal")
    anos_disponiveis = df['Ano'].dropna().astype(int).unique()
    ano_selecionado = st.slider(
        "Selecione o Ano de Análise:", 
        int(min(anos_disponiveis)), 
        int(max(anos_disponiveis)), 
        int(max(anos_disponiveis))
    )

    st.divider()

    st.subheader("Comparador de Países")
    lista_paises = df['Pais'].dropna().unique().tolist()
    paises_padrao = [p for p in ["Brazil", "United States", "Finland", "Afghanistan"] if p in lista_paises]
    paises_selecionados = st.multiselect(
        "Selecione as nações (Afeta a aba Início):", 
        options=lista_paises, 
        default=paises_padrao
    )
    
    st.divider()
    if st.button("Aplicar Filtros", use_container_width=True):
        st.toast("Filtros atualizados com sucesso!")

# =====================================================================
# 4. ESTRUTURA DE ABAS
# =====================================================================
st.title("🌍 World Happiness Report Dashboard")

tab_inicio, tab_q1, tab_q2, tab_q3, tab_q4 = st.tabs([
    "🏠 Visão Geral", 
    "🚩 Q1: Menores Índices", 
    "🤝 Q2: Generosidade", 
    "📉 Q3: Queda Histórica", 
    "🏰 Q4: Foco Europa"
])

# =====================================================================
# ABA 0: INÍCIO / VISÃO GERAL
# =====================================================================
with tab_inicio:
    st.markdown("Explore as correlações globais e compare o histórico das nações.")
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        with st.container(border=True):
            st.metric("Total de Países", df['Pais'].nunique())
    with col_b:
        with st.container(border=True):
            st.metric("Período Histórico", f"{int(df['Ano'].min())} - {int(df['Ano'].max())}")
    with col_c:
        with st.container(border=True):
            st.metric("Média Global (Escala Vida)", f"{df['Escala_Vida'].mean():.2f}")
    with col_d:
        with st.container(border=True):
            campeoes_anuais = df.loc[df.groupby('Ano')['Escala_Vida'].idxmax()]
            maior_campeao = campeoes_anuais['Pais'].mode()[0] if not campeoes_anuais.empty else "N/A"
            st.metric("Maior Campeão Histórico", maior_campeao)

    st.write("") 

    col_grafico, col_tabelas = st.columns([2.5, 1])

    with col_grafico:
        with st.container(border=True):
            st.markdown("#### Evolução da Felicidade (Países Selecionados)")
            if paises_selecionados:
                df_filtrado = df[df['Pais'].isin(paises_selecionados)]
                fig_linha = px.line(
                    df_filtrado, x='Ano', y='Escala_Vida', color='Pais', markers=True,
                    labels={'Ano': 'Ano', 'Escala_Vida': 'Índice de Felicidade'},
                    color_discrete_sequence=PALETA_QUENTE
                )
                st.plotly_chart(clean_chart(fig_linha), use_container_width=True)
            else:
                st.info("Selecione pelo menos um país no filtro lateral.")

        with st.container(border=True):
            st.markdown("#### Matriz de Correlação (O que impulsiona a felicidade?)")
            cols_correlacao = ['Escala_Vida', 'Log_PIB_Per_Capita', 'Suporte_Social', 
                               'Expectativa_Vida_Saudavel', 'Liberdade_Escolhas', 'Generosidade', 'Percepcao_Corrupcao']
            cols_correlacao = [col for col in cols_correlacao if col in df.columns]
            
            if cols_correlacao:
                df_corr = df[cols_correlacao].corr()
                fig_corr = px.imshow(
                    df_corr, text_auto=".2f", aspect="auto", color_continuous_scale="Oranges", origin='lower'
                )
                st.plotly_chart(clean_chart(fig_corr), use_container_width=True)

    with col_tabelas:
        with st.container(border=True):
            st.markdown("#### 🏆 Top 5 Histórico (Média)")
            top5_geral = df.groupby('Pais')['Escala_Vida'].mean().sort_values(ascending=False).head(5).reset_index()
            fig_top5 = px.bar(top5_geral, x='Escala_Vida', y='Pais', orientation='h', color_discrete_sequence=['#F59E0B'])
            fig_top5.update_yaxes(autorange="reversed")
            st.plotly_chart(clean_chart(fig_top5), use_container_width=True)

        with st.container(border=True):
            st.markdown("#### ⚠️ Bottom 5 Histórico (Média)")
            bottom5_geral = df.groupby('Pais')['Escala_Vida'].mean().sort_values(ascending=True).head(5).reset_index()
            fig_bot5 = px.bar(bottom5_geral, x='Escala_Vida', y='Pais', orientation='h', color_discrete_sequence=['#E76F51'])
            fig_bot5.update_yaxes(autorange="reversed")
            st.plotly_chart(clean_chart(fig_bot5), use_container_width=True)

# =====================================================================
# ABA 1: Q1 (MENORES ÍNDICES)
# =====================================================================
with tab_q1:
    st.markdown(f"Identifique os países na base da pirâmide em **{ano_selecionado}** e acompanhe o histórico do pior país de cada ano.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown(f"#### Top 10 Menores Índices em {ano_selecionado}")
            df_ano = df[df['Ano'] == ano_selecionado].copy()
            
            if not df_ano.empty:
                top_10_ano = df_ano.sort_values('Escala_Vida').head(10)
                fig1 = px.bar(
                    top_10_ano, x='Escala_Vida', y='Pais', orientation='h', text='Escala_Vida'
                )
                cores = ['#E76F51' if i == 0 else '#FCD34D' for i in range(len(top_10_ano))]
                fig1.update_traces(marker_color=cores, texttemplate='%{text:.2f}', textposition='outside')
                fig1.update_yaxes(autorange="reversed")
                st.plotly_chart(clean_chart(fig1), use_container_width=True)
            else:
                st.warning("Sem dados disponíveis para este ano.")

    with col2:
        with st.container(border=True):
            st.markdown("#### Histórico Geral: A Menor Nota de Cada Ano")
            indices_piores = df.groupby('Ano')['Escala_Vida'].idxmin()
            piores_por_ano = df.loc[indices_piores].sort_values('Ano')
            piores_por_ano['Ano_str'] = piores_por_ano['Ano'].astype(int).astype(str)

            fig2 = px.bar(
                piores_por_ano, x='Ano_str', y='Escala_Vida', color='Pais', text='Pais',
                color_discrete_sequence=PALETA_QUENTE, labels={'Ano_str': 'Ano', 'Escala_Vida': 'Índice Escala Vida'}
            )
            fig2.update_traces(textposition='inside', textangle=-90)
            fig2.update_layout(showlegend=False) 
            st.plotly_chart(clean_chart(fig2), use_container_width=True)

# =====================================================================
# ABA 2: Q2 (GENEROSIDADE)
# =====================================================================
with tab_q2:
    st.markdown(f"Analise a generosidade atual do grupo mais feliz e acompanhe a tendência histórica dessa média.")
    
    df_ano_q2 = df[df['Ano'] == ano_selecionado].copy()
    
    if not df_ano_q2.empty:
        top10_felizes_ano = df_ano_q2.sort_values('Escala_Vida', ascending=False).head(10)
        media_generosidade_grupo = top10_felizes_ano['Generosidade'].mean()
        
        col_kpi1, col_kpi2 = st.columns(2)
        with col_kpi1:
            with st.container(border=True):
                mais_generoso = top10_felizes_ano.sort_values('Generosidade', ascending=False).iloc[0]
                st.metric(f"País Mais Generoso do TOP 10 ({ano_selecionado})", mais_generoso['Pais'], f"Nota: {mais_generoso['Generosidade']:.3f}", delta_color="off")
        with col_kpi2:
            with st.container(border=True):
                st.metric(f"Média de Generosidade do Grupo ({ano_selecionado})", f"{media_generosidade_grupo:.3f}", delta_color="off")
                
        col_graf_bar, col_graf_linha = st.columns(2)
        
        with col_graf_bar:
            with st.container(border=True):
                st.markdown(f"#### Composição da Generosidade em {ano_selecionado}")
                fig3 = px.bar(top10_felizes_ano, x='Pais', y='Generosidade', text_auto='.3f')
                cores_generosidade = ['#F97316' if val >= 0 else '#D1D5DB' for val in top10_felizes_ano['Generosidade']]
                fig3.update_traces(marker_color=cores_generosidade)
                fig3.add_hline(y=media_generosidade_grupo, line_dash="dash", line_color="#E76F51", annotation_text=f"Média: {media_generosidade_grupo:.3f}")
                fig3.update_layout(xaxis={'categoryorder': 'total descending'}, coloraxis_showscale=False)
                st.plotly_chart(clean_chart(fig3), use_container_width=True)

        with col_graf_linha:
            with st.container(border=True):
                st.markdown("#### Média Histórica do TOP 10 (Por Ano)")
                def get_top10_mean(group):
                    return group.sort_values('Escala_Vida', ascending=False).head(10)['Generosidade'].mean()
                
                media_historica = df.groupby('Ano').apply(get_top10_mean, include_groups=False).reset_index(name='Media_Generosidade')
                fig_hist = px.line(media_historica, x='Ano', y='Media_Generosidade', markers=True, color_discrete_sequence=['#F97316'])
                
                if ano_selecionado in media_historica['Ano'].values:
                    val_ano = media_historica[media_historica['Ano'] == ano_selecionado]['Media_Generosidade'].values[0]
                    fig_hist.add_scatter(x=[ano_selecionado], y=[val_ano], mode='markers', marker=dict(color='#E76F51', size=12))
                
                fig_hist.update_layout(showlegend=False)
                st.plotly_chart(clean_chart(fig_hist), use_container_width=True)
    else:
        st.warning(f"Não há dados disponíveis para o ano de {ano_selecionado}.")

# =====================================================================
# ABA 3: Q3 (QUEDA DE GENEROSIDADE)
# =====================================================================
with tab_q3:
    st.markdown("Identificação das **maiores quedas históricas** no índice de generosidade (Diferença entre o último e o primeiro ano registrado).")
    
    def calc_queda(grupo):
        grupo = grupo.sort_values('Ano')
        if len(grupo) > 1:
            return grupo['Generosidade'].iloc[-1] - grupo['Generosidade'].iloc[0]
        return 0

    quedas = df.groupby('Pais').apply(calc_queda, include_groups=False).reset_index(name='Queda Absoluta')
    top5_quedas = quedas.sort_values('Queda Absoluta').head(5).copy()
    top5_quedas['Módulo da Queda'] = top5_quedas['Queda Absoluta'].abs()
    
    col_table, col_chart = st.columns([1.2, 2])
    
    with col_table:
        with st.container(border=True):
            st.markdown("#### Ranking: Impacto da Queda Absoluta")
            fig_ranking = px.bar(
                top5_quedas, x='Módulo da Queda', y='Pais', orientation='h',
                text_auto='.3f', labels={'Módulo da Queda': 'Total de Pontos Perdidos'}
            )
            cores_ranking = ['#E76F51' if i == 0 else '#FB923C' for i in range(len(top5_quedas))]
            fig_ranking.update_traces(marker_color=cores_ranking, textposition='outside')
            fig_ranking.update_yaxes(autorange="reversed")
            st.plotly_chart(clean_chart(fig_ranking), use_container_width=True)
    
    with col_chart:
        with st.container(border=True):
            st.markdown("#### Tendência Histórica do TOP 5")
            df_top5 = df[df['Pais'].isin(top5_quedas['Pais'])].copy()
            fig4 = px.line(
                df_top5, x='Ano', y='Generosidade', color='Pais', markers=True,
                color_discrete_sequence=PALETA_QUENTE
            )
            st.plotly_chart(clean_chart(fig4), use_container_width=True)

# =====================================================================
# ABA 4: Q4 (FOCO EUROPA)
# =====================================================================
with tab_q4:
    st.markdown(f"Análise de **{ano_selecionado}**: Avalie a relação entre o desenvolvimento humano, saúde, economia e felicidade na Europa comparada ao resto do mundo.")
    
    europa = ['Albania', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom']
    
    df_base_q4 = df[df['Ano'] == ano_selecionado].copy()
    
    if not df_base_q4.empty and 'IDH' in df_base_q4.columns:
        df_base_q4['Grupo'] = df_base_q4['Pais'].apply(lambda x: 'Europa' if x in europa else 'Outros Países')
        df_base_q4['Tamanho_PIB'] = df_base_q4['Log_PIB_Per_Capita'].apply(lambda x: x if pd.notnull(x) and x > 0 else 5.0)
        
        df_europa_only = df_base_q4[df_base_q4['Grupo'] == 'Europa']
        if not df_europa_only.empty:
            id_mais_feliz = df_europa_only['Escala_Vida'].idxmax()
            pais_mais_feliz = df_europa_only.loc[id_mais_feliz, 'Pais']
            df_base_q4['Label_Destaque'] = df_base_q4['Pais'].apply(lambda x: x if x == pais_mais_feliz else "")
        else:
            df_base_q4['Label_Destaque'] = ""

        with st.container(border=True):
            st.markdown("#### 1. Desenvolvimento Humano e Riqueza: IDH vs Índice de Felicidade")
            fig_idh = px.scatter(
                df_base_q4, x='IDH', y='Escala_Vida', color='Grupo', size='Tamanho_PIB', 
                hover_name='Pais', text='Label_Destaque',
                hover_data={'IDH': ':.3f', 'Escala_Vida': ':.2f', 'Log_PIB_Per_Capita': ':.2f', 'Tamanho_PIB': False},
                color_discrete_map={'Europa': '#F97316', 'Outros Países': '#E5E7EB' if modo_escuro else '#CCCCCC'},
                labels={'IDH': 'Índice de Desenvolvimento Humano (IDH)', 'Escala_Vida': 'Índice de Felicidade', 'Grupo': 'Região'}
            )
            fig_idh.update_traces(textposition='top center')
            st.plotly_chart(clean_chart(fig_idh), use_container_width=True)
                
        with st.container(border=True):
            st.markdown("#### 2. Saúde e Longevidade: Expectativa de Vida vs Suporte Social")
            df_chart2 = df_base_q4.dropna(subset=['Expectativa_Vida_Saudavel', 'Suporte_Social'])
            
            if not df_chart2.empty:
                fig_vida = px.scatter(
                    df_chart2, x='Expectativa_Vida_Saudavel', y='Suporte_Social', color='Grupo', size='Tamanho_PIB',
                    hover_name='Pais', 
                    hover_data={'Expectativa_Vida_Saudavel': ':.1f', 'Suporte_Social': ':.2f', 'Tamanho_PIB': False},
                    color_discrete_map={'Europa': '#F97316', 'Outros Países': '#E5E7EB' if modo_escuro else '#CCCCCC'},
                    labels={'Expectativa_Vida_Saudavel': 'Expectativa de Vida Saudável (Anos)', 'Suporte_Social': 'Suporte Social', 'Grupo': 'Região'}
                )
                st.plotly_chart(clean_chart(fig_vida), use_container_width=True)
    else:
        st.warning(f"Não há dados disponíveis ou coluna IDH ausente para o ano de {ano_selecionado}.")