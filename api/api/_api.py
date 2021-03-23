"""Module to setup fastapi API to expose API to the outside world."""
import logging
import random
from typing import Any, Dict
from starlette.middleware.cors import CORSMiddleware
from collections import Counter



from fastapi import FastAPI
import uvicorn

ERROR_CODES = [error_code for error_code in range(50)]
LOGGER = logging.getLogger("API")
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'])
count_request = 0


def _generate_lists() -> Dict[str, Any]:

    """Generate resolved, unresolved and backlog lists."""
    return {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occured, that is `resolved`'
        } for error_idx in range(50)],
        'unresolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error DEF occured, that is `unresolved`'
        } for error_idx in range(50, 100)],
        'backlog': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error XYZ occured, that is in the `backlog`'
        } for error_idx in range(100, 150)]
    }




@app.get("/get_lists")
def get_lists() -> Dict[str, Any]:

   
    """Return resolved, unresolved and backlog lists."""
    LOGGER.info('Generating resolved, unresolved and backlog lists.')
    return _generate_lists()


@app.get("/error_request")
def error_request() -> Dict[str, int]:

    print(count_request)


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    """Return the error intersection counts between a set of resolved, unresolved and backlog lists.

   

    """
    LOGGER.info('Generating the intersection counts between a set of resolved, unresolved and backlog lists.')

    error_lists = _generate_lists()
    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

    def get_common_error(x,y):
        count  = 0
        for a in x:
            if a in y:
                count = count+1
        return count


    def get_error_list(arg):
        arg_error = []
        for i in arg:
            a = i['code']
            if a not in arg_error:
                arg_error.append(a)

        return arg_error

  
    

    error_from_resolved = get_error_list(resolved)
    error_from_unresolved = get_error_list(unresolved)
    error_from_backlog = get_error_list(backlog)

    return  {
        'resolved_unresolved': get_common_error(error_from_resolved,error_from_unresolved),
        'resolved_backlog': get_common_error(error_from_resolved,error_from_backlog),
        'unresolved_backlog': get_common_error(error_from_unresolved,error_from_backlog)
    }


@app.get("/resolved_error_repeat")
def resolved_error_request() -> Dict[str, int]:

    """Return the error intersection counts between a set of resolved, unresolved and backlog lists."""
    LOGGER.info('Generating resolved repeat error')

    def get_error_list(arg):
        arg_error = []
        for i in arg:
            a = i['code']
            if a not in arg_error:
                arg_error.append(a)

        return arg_error

    error_lists = _generate_lists()
    resolved = error_lists['resolved']


    error_from_resolved = get_error_list(resolved)
    resolved_repeat = dict(Counter(error_from_resolved))

    return resolved_repeat




def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)
