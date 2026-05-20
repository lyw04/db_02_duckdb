import flet as ft
# import pandas as pd
import duckdb


def main(page: ft.Page):
    page.title = "Asset List"
    page.padding = 16
    page.window.width = 450
    page.window.height = 300
    # page.scroll = ft.ScrollMode.ADAPTIVE

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

    # 너비 비율 계산
    # lengths = {col: int(max(df[col].astype(str).map(len).max(), len(col))) for col in df.columns}
    lengths = {}
    for col in df.columns:
        # 컬럼명 자체의 길이와 데이터들 중 최대 길이
        max_len = max(df[col].astype(str).map(len).max(), len(col))
        lengths[col] = int(max_len)

    # 헤더
    sticky_header = ft.Row(
        controls=[
            ft.Container(ft.Text(col.upper(), weight="bold", size=16), expand=lengths[col]) 
            for col in df.columns
        ],
    )

    # 데이터 리스트
    data_rows = []
    for _, row in df.iterrows():
        data_rows.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(str(row[col]), expand=lengths[col]) for col in df.columns
                ]),
                height=40,
            )
        )

    # 스크롤되는 영역에 data_rows 지정
    scrollable_data = ft.Column(
        controls=data_rows,
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    page.add(
        sticky_header,
        ft.Divider(),
        scrollable_data
    )


if __name__ == "__main__":
    ft.run(main)
