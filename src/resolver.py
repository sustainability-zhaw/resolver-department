import logging

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from settings import settings


logger = logging.getLogger(__name__)

graphql_client = None # Client(transport=RequestsHTTPTransport(url=f"http://{settings.DB_HOST}/graphql"))


def query_info_object_by_link(link):
    return graphql_client.execute(
        gql(
            """
            query getInfoObject($link: String!) {
                getInfoObject(link: $link) {
                    link
                    departments {
                        id
                    }
                    authors {
                        person {
                            department {
                                id
                            }
                        }
                    }
                }
            }
            """
        ),
        variable_values={ "link": link }
    )["getInfoObject"]


def update_info_object(input):
        graphql_client.execute(
            gql(
                """
                mutation updateInfoObject($input: UpdateInfoObjectInput!) {
                    updateInfoObject(input: $input) {
                        infoObject {
                            link     
                        }
                    }
                }
                """
            ),
            variable_values={
                  "input": input
            }
        )


def run(link):
    logger.info(f"Resolving departments for link {link}")

    global graphql_client

    if graphql_client is None:
        logger.info(f"connect to database at '{settings.DB_HOST}'")
        graphql_client = Client(transport=RequestsHTTPTransport(url=f"http://{settings.DB_HOST}/graphql"))

    info_object = query_info_object_by_link(link)

    if not info_object:
        return

    info_object_department_ids = [ 
        department["id"]
        for department in info_object["departments"]
    ]

    person_departments_ids = [
        author['person']['department']["id"]
        for author in info_object['authors'] if author['person']
    ]
    
    new_departments = [
        { "id": department_id }
        for department_id in person_departments_ids if department_id not in info_object_department_ids
    ]

    logger.info(f"Found {len(new_departments)} additional departments")

    if not len(new_departments):
        return

    update_info_object(
        {
            "filter": { "link": { "eq": info_object["link"] } },
            "set": { "departments": new_departments },
        }
    )
