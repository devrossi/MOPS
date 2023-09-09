import cx_Oracle

def connect_to_db(username, password, host, service_name, port):
    try:
        dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        return connection
    except Exception as e:
        raise e
