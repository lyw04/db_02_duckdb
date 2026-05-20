import flet as ft
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

    snack_bar = ft.SnackBar(content=ft.Text("데이터베이스 저장 완료"))
    page.overlay.append(snack_bar)
    snack_bar.open = True

    # DB로부터 Pandas DataFrame으로 읽어오기
    df = con.execute("SELECT * FROM assets").df()

    def get_data(filter_query=""):
        if filter_query:
            query = """
                SELECT * FROM assets 
                WHERE name ILIKE ? 
            """
            search_str = f'%{filter_query}%'
            return con.execute(query, [search_str,]).df()
        else:
            return con.execute("SELECT * FROM assets").df()

    df = get_data()

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

    # 필터링을 반영한 row 생성 함수
    def create_rows(current_df):
        rows = []
        for _, row in current_df.iterrows():
            rows.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(str(row[col]), expand=lengths[col]) for col in current_df.columns
                    ]),
                    height=40,
                )
            )
        return rows

    # 스크롤 되는 영역에 create_rows() 함수 결과 지정
    scrollable_data = ft.Column(
        controls=create_rows(df),
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    # 필터링 이벤트 핸들러
    def on_filter_change(e):
        # 입력된 텍스트로 DB 검색
        filtered_df = get_data(e.control.value)
        scrollable_data.controls = create_rows(filtered_df)
        page.update()

    # 필터 입력
    filter_input = ft.Container(
        ft.TextField(
            label="종목 검색",
            prefix_icon=ft.Icons.SEARCH,
            hint_text="종목명을 입력하세요",
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            expand=True,
            on_change=on_filter_change,
        )
    )

    page.add(
        filter_input,
        sticky_header,
        ft.Divider(),
        scrollable_data
    )

if __name__ == "__main__":
    ft.run(main)