import requests
from urllib.parse import urlparse, urljoin

def get_root_url(user_url):
    parsed_url = urlparse(user_url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return root_url

def get_robots_txt(root_url):
    robots_url = urljoin(root_url, '/robots.txt')
    response = requests.get(robots_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_robots_txt(robots_txt_content, root_url,user_agent='*'):
    lines = robots_txt_content.split('\n')
    user_agent_section = False
    allowed_urls = []

    for line in lines:
        line = line.strip()

        if line.lower().startswith('user-agent:'):
            current_user_agent = line[len('User-agent:'):].strip()
            user_agent_section = (current_user_agent.lower() == user_agent.lower() or current_user_agent == '*')

        elif user_agent_section and line.startswith('Allow:'):
            allowed_url = line[len('Allow:'):].strip()
            allowed_urls.append(urljoin(root_url, allowed_url))

    return allowed_urls

def is_url_allowed(current_url, allowed_urls):
    for allowed_url in allowed_urls:
        if allowed_url.endswith('*') and current_url.startswith(allowed_url[:-1]):
            return True
        elif current_url == allowed_url:
            return True
    return False

def inspect(user_url):
    print(user_url)
    allowed = None
    root_url = get_root_url(user_url)
    robots_txt_content = get_robots_txt(root_url)
    if robots_txt_content:
        allowed_urls = parse_robots_txt(robots_txt_content, root_url)
        print(f"Allowed URLs for User-agent '*': {allowed_urls}")
        allowed = is_url_allowed(user_url,allowed_urls)
    else:
        print(f"Failed to retrieve robots.txt file for {root_url}.")
        allowed = True

    print(allowed)
    return allowed