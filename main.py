import flet as ft
import pandas as pd
import duckdb


def main(page: ft.Page):
    page.title = "Asset List"
    page.padding = 16
    page.window.width = 400
    page.window.height = 400

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


if __name__ == "__main__":
    ft.run(main)
