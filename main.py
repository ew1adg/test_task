import logging

import requests

MAX_PAGES = 100
API_ENDPOINT = 'https://reqres.in/api/users'
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"


def get_user_full_name_list(min_id: int, max_id: int) -> list:
    logger = logging.getLogger(__name__)

    # Validate arguments
    if not isinstance(min_id, int):
        logger.error('Minimal id value is not integer')
        return []
    if not isinstance(max_id, int):
        logger.error('Maximal ID value is not integer')
        return []
    if min_id < 0 or max_id < 0:
        logger.error('Argument must be a positive')
        return []
    if min_id > max_id:
        logger.error('Minimal value shall be less or equal to Maximal')
        return []

    exported_users = list()

    # Prepare headers
    ua_header = {'user-agent': USER_AGENT}

    for page_number in range(1, MAX_PAGES + 1):
        # Parametrize url
        parametrized_url = f'{API_ENDPOINT}?page={page_number}'

        # Request data
        logger.info(f'Get data from page {page_number}')
        response = requests.get(parametrized_url, headers=ua_header)
        if response.status_code != 200:
            raise RuntimeError('Request was not successful')

        # Extract data
        resp_data = response.json()
        user_data = resp_data.get('data')
        total_pages = resp_data.get('total_pages', 1)

        if not user_data:
            raise ValueError('There is no user data in response')

        for user_entry in user_data:
            # Extract user details
            _id = user_entry.get('id')
            first_name = user_entry.get('first_name')
            last_name = user_entry.get('last_name')

            # Add user to list if id meets requirements
            if min_id <= _id <= max_id:
                full_name = f'{first_name} {last_name}'
                exported_users.append(full_name)

        # Exit if this is a last page
        if page_number == total_pages:
            break

        logger.info(f"{str(response.json())}")

    exported_users.sort()
    logger.info(f'Exported users is {exported_users}')
    return exported_users


def main():
    logging.basicConfig(level=logging.DEBUG)

    # assert get_user_full_name_list(1, 3) == ['Emma Wong', 'George Bluth', 'Janet Weaver']
    assert get_user_full_name_list(5, 8) == ['Charles Morris', 'Emma Wong', 'Eve Holt', 'Janet Weaver']


if __name__ == "__main__":
    main()
