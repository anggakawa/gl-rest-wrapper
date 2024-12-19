import argparse
import os
import pandas as pd
from datetime import datetime

from gitlab import get_all_projects, combine_all_commits

def main():
    parser = argparse.ArgumentParser(description='API Interation scripts')
    parser.add_argument('--access-token', required=True,
                      help='Your GitLab personal access token. Generate one at gitlab.com/-/profile/personal_access_tokens')
    args = parser.parse_args()
    user_page = 1
    per_page = 5
    while True:
        # list of projects
        projects = get_all_projects(args.access_token, user_page, per_page)
        project_maps = []
        print("Here a list of projects: \n")
        for i, project in enumerate(projects['results'], 1):
            project_maps.append({'id': project['id'], 'name': project['path']})
            print(f"{i}. {project['name_with_namespace']}")
        if projects['info']['next_page'] != '':
            print(f'Page: {user_page} / {projects["info"]["total_pages"]}')
            print("\nOptions:")
            print("1. Change page")
            print("2. Select project")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '1':
                user_page = input("Input your page: ")
            elif choice == '2':
                user_project_choice = input("Choose Project (by order): ")
                user_project_username = input("Search by Username: ")
                user_project_branch = input("Your Branch (development, main, etc.): ")
                combined_commits = combine_all_commits(args.access_token, project_maps[int(user_project_choice) - 1]['id'], user_project_username, user_project_branch)
                df = pd.DataFrame(combined_commits)
                current_date = datetime.now().strftime('%Y-%m-%d')
                filename = f"data/{project_maps[int(user_project_choice) - 1]['name']}_{current_date}.xlsx"
                df.to_excel(filename, engine='openpyxl', index=False)
            elif choice == '3':
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")


if __name__ == '__main__':
    main()
