# 오라클 DB 연동

import cx_Oracle

dbUser = 'ADMIN'
dbPasswd = 'Gammiproject!1'
dsn = 'gammi2_high'
def oracle_init():
    cx_Oracle.init_oracle_client('C:/instantclient_21_6')

def connect():
    try:
        conn = cx_Oracle.connect(dbUser, dbPasswd, dsn)
        conn.autocommit = False
        return conn
    except Exception as msg:
        print('오라클 연결 에러', msg)

def close(conn):
    try:
        if conn:
            conn.close()
    except Exception as msg:
        print('오라클 연결 해제 에러', msg)

def commit(conn):
    try:
        if conn:
            conn.commit()
    except Exception as msg:
        print('트랜잭션 커밋 에러', msg)
        conn.rollback()

def rollback(conn):
    try:
        if conn:
            conn.rollback()
    except Exception as msg:
        print('트랜잭션 롤백 에러', msg)