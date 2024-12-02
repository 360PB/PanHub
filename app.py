#app.py
import streamlit as st
import asyncio
from utils import get_search_results_cached
from config import CUSTOM_CSS, SEARCH_SOURCES

# 缓存搜索结果，缓存时间为10分钟（600秒）
@st.cache_data(ttl=600)
def get_cached_results(query, enabled_sources, desired_count):
    return asyncio.run(get_search_results_cached(query, enabled_sources, desired_count))


def main():
    # 页面配置
    st.set_page_config(
        page_title="夸克网盘资源搜索",
        page_icon="🔍",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # 应用自定义 CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # 初始化会话状态
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'results_per_page' not in st.session_state:
        st.session_state.results_per_page = 14  # 默认每页显示14个结果

    # 主页面标题
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h1 style="color: #4285f4; font-size: 2.5rem;">🔍 夸克网盘资源搜索</h1>
            <p style="color: #666;">快速搜索，轻松找到您需要的资源</p>
        </div>
    """, unsafe_allow_html=True)

    # 搜索框和按钮并排放置
    search_col1, search_col2 = st.columns([5, 1])  # 调整列宽比例
    with search_col1:
        query = st.text_input(
            label="搜索关键词",
            placeholder="请输入搜索关键词",
            label_visibility="collapsed",
            key="search_input"
        )
    with search_col2:
        # 使用 Streamlit 的按钮，无需自定义 HTML
        search_clicked = st.button("🔍 搜索", key="search_button")

    # 侧边栏：动态启用/禁用搜索源
    st.sidebar.markdown("### 启用搜索源")
    enabled_sources = {}
    for key, source in SEARCH_SOURCES.items():
        enabled = st.sidebar.checkbox(source['name'], value=source['enabled'], key=f'enable_{key}')
        enabled_sources[key] = enabled

    # 侧边栏：选择每页显示数量
    st.sidebar.markdown("### 每页显示数量")
    results_per_page = st.sidebar.selectbox(
        "选择每页显示的搜索结果数量",
        options=[44, 100, 200],
        index=0,  # 默认选择44
        key="results_per_page_select"
    )

    # 更新会话状态中的结果数量
    if st.session_state.results_per_page != results_per_page:
        st.session_state.results_per_page = results_per_page
        st.session_state.current_page = 1  # 重置当前页数

    # 侧边栏：显示搜索历史
    if st.session_state.search_history:
        st.sidebar.markdown("### 搜索历史")
        if st.sidebar.button("清除搜索历史", key="clear_history"):
            st.session_state.search_history = []
        for past_query in st.session_state.search_history[::-1]:  # 逆序显示最新的
            if st.sidebar.button(past_query, key=f'history_{past_query}'):
                st.session_state.search_input = past_query
                st.session_state.search_button = True

    # 高级搜索选项
    st.sidebar.markdown("### 高级搜索选项")
    advanced_search = st.sidebar.checkbox("显示高级搜索选项", key="show_advanced_search")

    advanced_filters = {}
    if advanced_search:
        with st.sidebar.expander("高级过滤器"):
            # 示例高级搜索选项，可以根据实际需求添加更多
            date_from = st.sidebar.date_input("日期从", key="date_from")
            date_to = st.sidebar.date_input("日期到", key="date_to")
            file_type = st.sidebar.selectbox(
                "文件类型",
                options=["全部", "文档", "视频", "音频", "图片"],
                index=0,
                key="file_type_select"
            )
            file_size = st.sidebar.selectbox(
                "文件大小",
                options=["全部", "小于10MB", "10MB-100MB", "大于100MB"],
                index=0,
                key="file_size_select"
            )
            advanced_filters['date_from'] = date_from
            advanced_filters['date_to'] = date_to
            advanced_filters['file_type'] = file_type
            advanced_filters['file_size'] = file_size

    # 搜索逻辑
    if search_clicked and query:
        # 更新搜索历史
        if query not in st.session_state.search_history:
            st.session_state.search_history.append(query)
            if len(st.session_state.search_history) > 10:
                st.session_state.search_history.pop(0)

        with st.spinner('正在搜索中...'):
            try:
                results = get_cached_results(query, enabled_sources, st.session_state.results_per_page)
            except Exception as e:
                st.error(f"搜索过程中出错: {e}")
                results = []
            st.session_state.search_results = results
            st.session_state.current_page = 1  # 重置到第一页

        if results:
            st.success(f"找到 {len(results)} 个相关资源")
            display_results_paginated(results, st.session_state.current_page, st.session_state.results_per_page)
        else:
            st.warning("未找到相关资源，请尝试其他关键词或调整搜索选项")

    elif st.session_state.get('search_results'):
        display_results_paginated(st.session_state.search_results, st.session_state.current_page, st.session_state.results_per_page)

    # 页脚
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 1rem; color: #666;">
            <p>Copyright © 2024 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)


def display_results_paginated(results, current_page, results_per_page):
    total_results = len(results)
    total_pages = (total_results + results_per_page - 1) // results_per_page
    start_idx = (current_page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    page_results = results[start_idx:end_idx]

    for result in page_results:
        st.markdown(f"""
        <div class="search-result">
            <span class="source-tag">{result.get('source', '未知来源')}</span>
            <h4>{result['title']}</h4>
            <a href="{result['url']}" target="_blank">{result['url']}</a>
        </div>
        """, unsafe_allow_html=True)

    # 分页控制
    if total_pages > 1:
        st.markdown('<div class="pagination">', unsafe_allow_html=True)
        col_prev, col_page, col_next = st.columns([1, 2, 1])  # 调整列宽比例
        with col_prev:
            if st.button("⬅️ 上一页", disabled=current_page == 1, key="prev_page"):
                st.session_state.current_page -= 1
        with col_page:
            st.markdown(f"<p>第 {current_page} 页 / 共 {total_pages} 页</p>", unsafe_allow_html=True)
        with col_next:
            if st.button("下一页 ➡️", disabled=current_page == total_pages, key="next_page"):
                st.session_state.current_page += 1
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
