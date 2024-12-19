import requests
from sqlalchemy import null


def get_all_projects(header, page=1, per_page=20):
    headers = {
        'Authorization': f"Bearer {header}"
    }
    try:
        r = requests.get(f"https://gitlab.com/api/v4/projects?membership=true&per_page={per_page}&page={page}", headers=headers)
        r.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        
        # Check if all required headers exist
        required_headers = ['x-next-page', 'x-prev-page', 'x-total-pages', 'x-total']
        for header in required_headers:
            if header not in r.headers:
                raise KeyError(f"Missing required header: {header}")
        
        info = {
            'next_page': r.headers['x-next-page'],
            'prev_page': r.headers['x-prev-page'],
            'total_pages': r.headers['x-total-pages'],
            'total': r.headers['x-total']
        }
        results = r.json()
        return {'results': results, 'info': info}
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Response missing required data: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response: {str(e)}")

def get_all_commits(token, project_id, username, branch="main", page=1, per_page=20):
    headers = {
        'Authorization': f"Bearer {token}"
    }
    try:
        parameters = f"commits?with_stats=yes&per_page={per_page}&page={page}"
        if username:
            parameters += f"&author={username}"
        if branch:
            parameters += f"&ref_name={branch}"
        r = requests.get(f"https://gitlab.com/api/v4/projects/{project_id}/repository/{parameters}", headers=headers)
        r.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        
        # Check if all required headers exist
        required_headers = ['x-next-page', 'x-prev-page']
        for header in required_headers:
            if header not in r.headers:
                raise KeyError(f"Missing required header: {header}")
        
        info = {
            'next_page': r.headers['x-next-page'],
            'prev_page': r.headers['x-prev-page']
        }

        results = r.json()

        return {'results': results, 'info': info}
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Response missing required data: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response: {str(e)}")


def combine_all_commits(token, project_id, username, branch):
    combined_commits = []
    page = 1
    while True:
        fetch_commits = get_all_commits(token, project_id, username, branch, page)
        result_data = fetch_commits['results']
        for result in result_data:
            combined_commits.append({'id': result['id'], 'created_at': result['created_at'], 
                                     'title': result['title'], 'author_name': result['author_name'],
                                     'committed_date': result['committed_date'], 'additions': result['stats']['additions'],
                                     'deletions': result['stats']['deletions'], 'total': result['stats']['total']})
        if fetch_commits["info"]["next_page"] == '':
            break
        page += 1
    print(f"combined commits: ", len(combined_commits))
    return combined_commits