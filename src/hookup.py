import re
import db


def run(routing_key, body):
    info_object = db.query_info_object_by_link(body['link'])
    departments = list([author['person']['department'] for author in info_object['authors'] if author['person']]) if info_object else []
    
    if not len(departments):
        return

    db.update_info_object(
        {
            "filter": { "link": { "eq": info_object["link"] } },
            "set": { "departments": departments },
        }
    )
