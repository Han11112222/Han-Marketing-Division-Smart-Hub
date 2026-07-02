import flet as ft
import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1fu8wYyfCMHBK6rpD3kbl4G_zmwEcse7tKjY08_SucM8/export?format=csv&gid=0"

def get_data():
    backup = [{"구분": "Key Support", "내용": "샘플 데이터", "기능": "엑셀 연결 필요", "활용도": 5, "링크": "#"}]
    try:
        df = pd.read_csv(SHEET_URL, header=None)
        header_idx = -1
        for i, row in df.iterrows():
            if "구분" in " ".join([str(v) for v in row]) and "내용" in " ".join([str(v) for v in row]):
                header_idx = i
                break
        if header_idx == -1:
            return pd.DataFrame(backup)
        df = pd.read_csv(SHEET_URL, header=header_idx).fillna("")
        if '내용' in df.columns:
            trash = ['상세분류', '구분', '내용', '기능', '활용도']
            df = df[~df['내용'].isin(trash)]
            df = df[df['내용'] != ""]
        if '구분' in df.columns:
            df['구분'] = df['구분'].replace("", pd.NA).ffill()
        return df
    except Exception as e:
        print(f"데이터 로드 오류: {e}")
        return pd.DataFrame(backup)

def main(page: ft.Page):
    page.title = "HAN Smart Marketing Hub"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#f8fafc"
    page.window_width = 480      # 모바일 사이즈
    page.window_min_width = 360

    def make_stars(val):
        try:
            if isinstance(val, str) and "★" in val:
                return val
            n = int(float(val)) if val else 0
            return "★" * n + "☆" * (5 - n)
        except:
            return "☆☆☆☆☆"

    # 타이틀
    page.add(
        ft.Container(
            content=ft.Text("🔥 HAN _ Smart Marketing Hub",
                          size=18, weight=ft.FontWeight.BOLD, color="#2c3e50"),
            margin=ft.margin.only(bottom=16)
        )
    )

    df = get_data()

    if df.empty:
        page.add(ft.Text("데이터를 불러올 수 없습니다.", color="red"))
        return

    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

    for category in df['구분'].unique():
        if not category or pd.isna(category):
            continue

        cat_rows = df[df['구분'] == category]

        # 섹션 헤더
        page.add(
            ft.Container(
                content=ft.Row([
                    ft.Text("📂", size=14),
                    ft.Text(str(category), size=14,
                           weight=ft.FontWeight.BOLD, color="#1e40af"),
                ]),
                margin=ft.margin.only(top=20, bottom=4)
            )
        )
        page.add(ft.Divider(height=1, color="#1e40af"))

        # 컬럼 헤더
        page.add(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text("업무 내용", weight=ft.FontWeight.BOLD,
                                      color="#555", size=12),
                        expand=5
                    ),
                    ft.Container(
                        content=ft.Text("활용도", weight=ft.FontWeight.BOLD,
                                      color="#555", size=12,
                                      text_align=ft.TextAlign.CENTER),
                        expand=2
                    ),
                    ft.Container(
                        content=ft.Text("링크", weight=ft.FontWeight.BOLD,
                                      color="#555", size=12,
                                      text_align=ft.TextAlign.CENTER),
                        expand=2
                    ),
                ]),
                bgcolor="#f1f5f9",
                padding=ft.padding.symmetric(horizontal=8, vertical=8),
                border_radius=4,
            )
        )

        # 데이터 행
        for _, row in cat_rows.iterrows():
            title = str(row.get('내용', ''))
            desc  = str(row.get('기능', ''))
            stars = make_stars(row.get('활용도', 0))
            link  = str(row.get('링크', '#'))

            if not title or title in ['상세분류', '구분']:
                continue

            page.add(
                ft.Container(
                    content=ft.Row([
                        # 업무내용
                        ft.Container(
                            content=ft.Column([
                                ft.Text(title, weight=ft.FontWeight.BOLD,
                                       size=12, no_wrap=False),
                                ft.Text(desc, color="#555", size=11,
                                       no_wrap=False),
                            ], spacing=2, tight=True),
                            expand=5,
                        ),
                        # 별점
                        ft.Container(
                            content=ft.Text(stars, color="#f59e0b", size=11,
                                          text_align=ft.TextAlign.CENTER),
                            expand=2,
                            alignment=ft.alignment.center,
                        ),
                        # 링크버튼
                        ft.Container(
                            content=ft.ElevatedButton(
                                "🔗",
                                on_click=lambda e, u=link: page.launch_url(u),
                                style=ft.ButtonStyle(
                                    color="#555",
                                    bgcolor="#ffffff",
                                    padding=ft.padding.symmetric(horizontal=4, vertical=2),
                                    shape=ft.RoundedRectangleBorder(radius=6),
                                    side=ft.BorderSide(1, "#d1d5db"),
                                ),
                                height=32,
                            ),
                            expand=2,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                    ),
                    border=ft.border.only(bottom=ft.BorderSide(1, "#e5e7eb")),
                    padding=ft.padding.symmetric(horizontal=8, vertical=10),
                )
            )

        page.add(ft.Container(height=12))

ft.app(target=main)
