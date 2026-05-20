import flet as ft
# import pandas as pd
import duckdb


def main(page: ft.Page):
    page.title = "Asset List"
    page.padding = 16
    page.window.width = 450
    page.window.height = 300
    page.scroll = ft.ScrollMode.ADAPTIVE

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

    snack_bar = ft.SnackBar(content=ft.Text("데이터베이스 저장 완료"))
    page.overlay.append(snack_bar)
    snack_bar.open = True

    # DB로부터 Pandas DataFrame으로 읽어오기
    df = con.execute("SELECT * FROM assets").df()

    # DataTable 생성
    data_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col.upper())) for col in df.columns],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(val))) for val in row])
            for row in df.values
        ],
    )

    page.add(data_table)


if __name__ == "__main__":
    ft.run(main)
