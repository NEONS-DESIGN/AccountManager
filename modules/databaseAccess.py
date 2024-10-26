from modules.sqlite import sql_execution

# ---------------------------------
# データベースアクセス関数定義
# ---------------------------------
async def get_service_list():
    sql = f"SELECT * FROM serviceList;"
    return await sql_execution(sql)

async def get_search_service_list(serviceName):
    sql = f"SELECT * FROM serviceList WHERE serviceName = '{serviceName}';"
    return await sql_execution(sql)

async def get_like_search_service_list(serviceName):
    sql = f"SELECT * FROM serviceList WHERE serviceName LIKE '%{serviceName}%';"
    return await sql_execution(sql)

async def delete_service(uuid):
    sql = f"DELETE FROM serviceList WHERE uuid = '{uuid}';"
    return await sql_execution(sql)

async def delete_account(serviceUuid):
    sql = f"DELETE FROM accountData WHERE serviceUuid = '{serviceUuid}';"
    return await sql_execution(sql)

async def insert_service(uuid, serviceName, serviceDetail):
    sql = f"INSERT INTO serviceList (uuid, serviceName, serviceDetail) VALUES ('{uuid}', '{serviceName}', '{serviceDetail}')"
    return await sql_execution(sql)

async def update_service(uuid, newServiceName, serviceDetail):
    sql1 = f"UPDATE serviceList SET serviceDetail = '{serviceDetail}' WHERE uuid IS '{uuid}'"
    result1 = await sql_execution(sql1)
    sql2 = f"UPDATE serviceList SET serviceName = '{newServiceName}' WHERE uuid IS '{uuid}'"
    result2 = await sql_execution(sql2)
    sql3 = f"UPDATE accountData SET serviceName = '{newServiceName}' WHERE serviceUuid IS '{uuid}'"
    result3 = await sql_execution(sql3)
    return result1, result2, result3

async def get_account_list(serviceUuid):
    sql = f"SELECT * FROM accountData WHERE serviceUuid = '{serviceUuid}';"
    return await sql_execution(sql)