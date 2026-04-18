from db import engine

# generic function for getting information the same way the original db did
async def get_resource(json: dict) -> list[dict]:
    con = engine.connect(close_with_result=True)

    for key, value in json.items():
        ...

    result = con.execute('SELECT * FROM TRANSLATIONS;').fetchall()

    result_dict = [dict(row) for row in result]

    return result

async def create_resource(json: dict) -> list[dict]:
    con = engine.connect()

    result = con.execute('INSERT INTO ...')
    result_dict = [dict(row) for row in result]

    return result_dict


async def change_record(json: dict) -> list[dict]:
    con = engine.connect()


