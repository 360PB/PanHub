# config.py

# 搜索源配置
SEARCH_SOURCES = {
    'source1': {
        'name': 'PanHub',
        'url': 'https://panhub.fun/s/',
        'enabled': True,  # 初始设置
        'priority': 1
    },
    'source2': {
        'name': 'KK看吧',
        'url': 'http://s.kkkob.com/v/api',
        'enabled': True,
        'priority': 2
    },
    'source3': {
        'name': '奇乐搜',
        'url': 'https://www.qileso.com/tag/quark',
        'enabled': True,
        'priority': 3
    },
    'source4': {
        'name': 'PanSearch',
        'url': 'https://www.pansearch.me/search',
        'enabled': True,
        'priority': 4
    },
    'source5': {
        'name': '心悦搜',
        'url': 'https://www.xinyueso.com/s/',
        'enabled': True,
        'priority': 5
    }
}

# 用户代理池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
]

# 自定义样式
CUSTOM_CSS = """
<style>
    /* 搜索结果样式 */
    .search-result {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .source-tag {
        font-size: 0.8rem;
        color: #fff;
        background-color: #4285f4;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        margin-right: 0.5rem;
    }
    /* 分页控制样式 */
    .pagination {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    .pagination button {
        margin: 0 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        background-color: #4285f4;
        color: white;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    .pagination button:disabled {
        background-color: #a0c4ff;
        cursor: not-allowed;
    }
</style>
"""
