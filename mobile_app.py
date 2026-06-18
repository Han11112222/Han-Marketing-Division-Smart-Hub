import flet as ft

def main(page: ft.Page):
    # 모바일 화면 UI 설정
    page.title = "마케팅본부 스마트 허브"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 화면에 들어갈 요소들 만들기
    title = ft.Text("📊 마케팅본부 스마트 허브", size=24, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("현재 데이터 대기 중...", size=16, color="grey")

    # 버튼을 눌렀을 때 실행될 동작
    def load_data(e):
        status_text.value = "✔️ marketing_hub.xlsx 연동 준비 완료!"
        status_text.color = "blue"
        page.update()

    # 버튼 만들기
    load_btn = ft.ElevatedButton("모바일 데이터 불러오기", on_click=load_data)

    # 화면에 순서대로 요소 배치하기
    page.add(title, status_text, load_btn)

# 모바일 호환 모드로 앱 실행
ft.app(target=main)