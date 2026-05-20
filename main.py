import flet as ft
import pandas as pd
import duckdb


def main(page: ft.Page):
    page.title = "Asset List"
    page.padding = 16
    page.window.width = 450
    page.window.height = 500

    # 데이터베이스 접속
    con = duckdb.connect("data/finance.db")

    # 테이블 생성
    con.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            ticker VARCHAR PRIMARY KEY,
            name VARCHAR,
            type VARCHAR
        )
    """)

    # assets.csv 파일을 읽어서 테이블에 추가
    con.execute("""
        INSERT OR IGNORE INTO assets 
        SELECT * FROM read_csv_auto('data/assets.csv')
    """)

    print("데이터베이스 저장 완료")
    
    snack_bar = ft.SnackBar(
        content=ft.Text("데이터베이스 저장 완료")
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
 
    # DB로부터 Pandas DataFrame으로 읽어오기
    df = con.execute("SELECT * FROM assets").df()

    # DataTable 생성
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("티커")),
            ft.DataColumn(ft.Text("종목명")),
            ft.DataColumn(ft.Text("종류")),
        ],
        rows=[]
    )

    # DataRow로 변환하여 추가
    for _, row in df.iterrows():
        data_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row['ticker'])),
                    ft.DataCell(ft.Text(row['name'])),
                    ft.DataCell(ft.Text(row['type'])),
                ]
            )
        )

    page.add(data_table)

if __name__ == "__main__":
    ft.run(main)
