# utils.py

import aiohttp
import asyncio
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from config import USER_AGENTS, SEARCH_SOURCES


def get_random_user_agent():
    return random.choice(USER_AGENTS)


async def search_source1(session, title):
    results = []
    try:
        encoded_title = quote(title)
        url = f"https://panhub.fun/s/{encoded_title}.html"
        print(f"Searching Source1 with URL: {url}")

        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            print(f"Source1 Response Status: {response.status}")
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'lxml')

                # 更新选择器，根据实际 HTML 结构调整
                items = soup.select('.listBox .box .item')
                print(f"Source1 Found {len(items)} items with selector '.listBox .box .item'")

                for item in items:
                    try:
                        title_elem = item.select_one('a.title')
                        if title_elem:
                            result_title = title_elem.get_text(strip=True)
                            result_url = title_elem.get('href', '')
                            print(f"Source1 Found Result: {result_title}, URL: {result_url}")

                            if 'pan.quark.cn' in result_url:
                                results.append({
                                    'title': result_title,
                                    'url': result_url,
                                    'source': SEARCH_SOURCES['source1']['name']  # 添加 'source' 键
                                })

                    except Exception as e:
                        print(f"Error parsing item in source1: {e}")
                        continue

    except aiohttp.ClientConnectorError as e:
        print(f"Connection error in search_source1: {e}")
    except asyncio.TimeoutError:
        print("Timeout error in search_source1")
    except Exception as e:
        print(f"Unexpected error in search_source1: {e}")

    print(f"Source1 returning {len(results)} results")
    return results


async def search_source2(session, title):
    results = []
    try:
        url_default = "http://s.kkkob.com"
        async with session.get(f"{url_default}/v/api/getToken", timeout=aiohttp.ClientTimeout(total=30)) as response:
            token_data = await response.json()
            token = token_data.get('token', '')
            print(f"Source2 Retrieved Token: {token}")

        if not token:
            print("Source2 Token not found")
            return results

        headers = {'Content-Type': 'application/json'}
        data = {'name': title, 'token': token}

        async with session.post(f"{url_default}/v/api/getJuzi", json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            juzi_data = await response.json()
            print(f"Source2 Juzi Data: {juzi_data}")
            for item in juzi_data.get('list', []):
                if 'https://pan.quark.cn/' in item['answer']:
                    match = re.search(r'https://pan\.quark\.cn/\S+', item['answer'])
                    if match:
                        results.append({
                            'title': item['question'],
                            'url': match.group(0),
                            'source': SEARCH_SOURCES['source2']['name']  # 添加 'source' 键
                        })
                        print(f"Source2 Found Result: {item['question']}, URL: {match.group(0)}")
                        break

        async with session.post(f"{url_default}/v/api/getXiaoyu", json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            xiaoyu_data = await response.json()
            print(f"Source2 Xiaoyu Data: {xiaoyu_data}")
            for item in xiaoyu_data.get('list', []):
                if 'https://pan.quark.cn/' in item['answer']:
                    match = re.search(r'https://pan\.quark\.cn/\S+', item['answer'])
                    if match:
                        results.append({
                            'title': item['question'],
                            'url': match.group(0),
                            'source': SEARCH_SOURCES['source2']['name']  # 添加 'source' 键
                        })
                        print(f"Source2 Found Result: {item['question']}, URL: {match.group(0)}")
                        break

    except aiohttp.ClientConnectorError as e:
        print(f"Connection error in search_source2: {e}")
    except asyncio.TimeoutError:
        print("Timeout error in search_source2")
    except Exception as e:
        print(f"Unexpected error in search_source2: {e}")
    print(f"Source2 returning {len(results)} results")
    return results


async def search_source3(session, title):
    results = []
    try:
        url = f'https://www.qileso.com/tag/quark?s={title}'
        headers = {'User-Agent': get_random_user_agent()}
        print(f"Searching Source3 with URL: {url}")

        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'lxml')
            nodes = soup.select('.list-group.post-list.mt-3 a')
            print(f"Source3 Found {len(nodes)} nodes with selector '.list-group.post-list.mt-3 a'")

            if nodes:
                href = nodes[0]['href']
                print(f"Source3 Fetching detail page: {href}")
                async with session.get(href, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as node_response:
                    node_content = await node_response.text()
                    node_soup = BeautifulSoup(node_content, 'lxml')
                    nodes = node_soup.select('a[href^="https://pan.quark.cn/s/"]')
                    print(f"Source3 Found {len(nodes)} nodes with selector 'a[href^=\"https://pan.quark.cn/s/\"]'")

                    if nodes:
                        url = nodes[0]['href']
                        title = node_soup.title.string.replace(' - 奇乐搜', '').replace('网盘', '').replace('夸克', '')
                        results.append({
                            'title': title,
                            'url': url,
                            'source': SEARCH_SOURCES['source3']['name']  # 添加 'source' 键
                        })
                        print(f"Source3 Found Result: {title}, URL: {url}")
    except aiohttp.ClientConnectorError as e:
        print(f"Connection error in search_source3: {e}")
    except asyncio.TimeoutError:
        print("Timeout error in search_source3")
    except Exception as e:
        print(f"Unexpected error in search_source3: {e}")
    print(f"Source3 returning {len(results)} results")
    return results


async def search_source4(session, title):
    results = []
    try:
        url = f'https://www.pansearch.me/search?keyword={title}&pan=quark'
        headers = {'User-Agent': get_random_user_agent()}
        print(f"Searching Source4 with URL: {url}")

        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'lxml')
            nodes = soup.select('.whitespace-pre-wrap.break-all')
            print(f"Source4 Found {len(nodes)} nodes with selector '.whitespace-pre-wrap.break-all'")

            for node in nodes:
                content = node.get_text()
                title_match = re.search(r'名称：(.*?)\n\n描述：', content)
                url_match = re.search(r'链接：(https://pan\.quark\.cn/s/[a-zA-Z0-9]+)', content)

                if title_match and url_match:
                    results.append({
                        'title': f"「推荐」{title_match.group(1).strip()}",
                        'url': url_match.group(1),
                        'source': SEARCH_SOURCES['source4']['name']  # 添加 'source' 键
                    })
                    print(f"Source4 Found Result: {'「推荐」' + title_match.group(1).strip()}, URL: {url_match.group(1)}")

                if len(results) >= 14:
                    break  # 根据页面配置动态决定

    except aiohttp.ClientConnectorError as e:
        print(f"Connection error in search_source4: {e}")
    except asyncio.TimeoutError:
        print("Timeout error in search_source4")
    except Exception as e:
        print(f"Unexpected error in search_source4: {e}")
    print(f"Source4 returning {len(results)} results")
    return results


async def search_source5(session, title):
    results = []
    try:
        encoded_title = quote(title)
        url = f"https://www.xinyueso.com/s/{encoded_title}.html"  # 与 search_source1 相同的 URL 模式
        print(f"Searching Source5 with URL: {url}")

        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'lxml')

                # 更新选择器，根据实际 HTML 结构调整
                items = soup.select('.listBox .box .item')
                print(f"Source5 Found {len(items)} items with selector '.listBox .box .item'")

                for item in items:
                    try:
                        title_elem = item.select_one('a.title')
                        if title_elem:
                            result_title = title_elem.get_text(strip=True)
                            result_url = title_elem.get('href', '')
                            print(f"Source5 Found Result: {result_title}, URL: {result_url}")

                            if 'pan.quark.cn' in result_url:
                                results.append({
                                    'title': result_title,
                                    'url': result_url,
                                    'source': SEARCH_SOURCES['source5']['name']  # 添加 'source' 键
                                })

                    except Exception as e:
                        print(f"Error parsing item in source5: {e}")
                        continue

    except aiohttp.ClientConnectorError as e:
        print(f"Connection error in search_source5: {e}")
    except asyncio.TimeoutError:
        print("Timeout error in search_source5")
    except Exception as e:
        print(f"Unexpected error in search_source5: {e}")

    print(f"Source5 returning {len(results)} results")
    return results


async def get_search_results_cached(query, enabled_sources, desired_count=14):
    async with aiohttp.ClientSession() as session:
        all_results = []

        # 根据优先级排序启用的搜索源
        sorted_sources = sorted(
            [item for item in SEARCH_SOURCES.items() if enabled_sources.get(item[0], False)],
            key=lambda item: item[1].get('priority', 100)
        )

        for source_key, source_info in sorted_sources:
            search_func = globals().get(f'search_{source_key}')
            if search_func:
                try:
                    source_results = await search_func(session, query)
                    if source_results:
                        all_results.extend(source_results)
                        # 如果达到所需数量，则停止调用其他源
                        if len(all_results) >= desired_count:
                            print(f"Reached desired count {desired_count}. Stopping search.")
                            break
                except Exception as e:
                    print(f"Error searching {source_info['name']}: {e}")

        # 确保返回的结果不超过所需数量
        return all_results[:desired_count]
