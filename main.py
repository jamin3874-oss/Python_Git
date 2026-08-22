prompts = [
    {
        "title": "협업 요청 메일 어시스턴트 (케이)",
        "content": "당신은 '케이(Kay)'라는 이름의 팀 협업 요청 메일 작성 어시스턴트입니다. 케이는 사용자가 제공한 정보를 바탕으로 팀원, 다른 부서, 상급자 또는 외부 협력사에게 보내는 협업 요청 메일의 제목과 본문을 작성합니다. 입력에 없는 이름, 날짜, 장소, 업무 내용은 임의로 생성하지 않으며, 핵심 정보가 부족하면 확인 질문을 최대 3개까지 제시합니다. 수신자와의 관계 및 지정한 톤에 맞게 표현을 조절하고, 목적과 요청 사항, 기한, 후속 행동이 명확히 전달되도록 작성합니다.",
        "category": "페르소나",
        "favorite": False
    },
    {
        "title": "배달모아 광고 씬1 - 원룸 고민 장면",
        "content": "During the first 1.5 seconds, he barely moves except for subtle breathing and a natural blink. From 1.5 to 2.5 seconds, he quietly sighs and presses his lips together in hesitation. From 2.5 to 4 seconds, he slowly lowers the smartphone toward his lap while naturally lowering his gaze, unable to make a decision. During the final second, he holds the lowered position with a restrained, disappointed expression.",
        "category": "영상 생성",
        "favorite": False
    },
    {
        "title": "도로 안전 뉴스 자동화 워크플로 설계 요청",
        "content": "Make를 이용해 도로 안전 뉴스 자동 수집 워크플로를 만들고 있다. Make 화면에서 어떤 모듈을 추가하고 각 입력란에 무엇을 넣어야 하는지 단계별로, 한 단계씩 안내해줘. Google 뉴스 RSS에서 포트홀·노면 파손과 싱크홀·지반 침하 관련 기사를 가져와 분류하고 Notion 데이터베이스에 저장하며, Data Store로 중복 등록을 방지한다. RSS Watch RSS Feed Items → Router → 주제별 키워드 Filter(OR 조건) → Data Store 중복 확인 → Exists=false 필터 → Notion 등록 → Data Store에 Key 저장 순서로 구성한다. Notion 등록 실패 시 처리 완료로 잘못 기록되지 않도록, 가능하면 Notion 등록 성공 후 Data Store에 Key를 저장하는 순서로 안내해줘. 현재 Make 크레딧이 소진되어 실행 테스트는 못 했으니, 실행하지 않은 내용을 정상 작동했다고 단정하지 말고 설정 검토와 개선 방법 중심으로 안내해줘.",
        "category": "자동화",
        "favorite": False
    },
]

def add_prompt():
    title = input("제목: ")
    while title =="":
        title = input("제목을 다시 입력해주세요: ")

    content = input("내용: ")
    while content =="":
        content = input("내용을 다시 입력해주세요: ")

    print("카테고리 선택:")
    print("1) 텍스트 생성")
    print("2) 이미지 생성")
    print("3) 영상 생성")
    print("4) 페르소나")
    print("5) 자동화")
    print("6) 기타")
    category_input = input("번호를 선택하거나 직접 입력하세요: ")

    categories ={
        "1": "텍스트 생성",
        "2": "이미지 생성",
        "3": "영상 생성",
        "4": "페르소나",
        "5": "자동화",
        "6": "기타",           
    }

    if category_input in categories:
        category = categories[category_input] 
    else:
        category = category_input

    prompt = {"title": title, "content": content, "category": category, "favorite": False}
    prompts.append(prompt)
    print("프롬프트가 추가되었습니다!")      

def list_prompts():
    print(" === 프롬프트 목록 ===")
    for i, prompt in enumerate(prompts, start=1):
        star = "⭐" if prompt["favorite"] else ""
        print(i, "[" + prompt["category"] + "]",prompt["title"], star)

def show_by_category():
    print("=== 카테고리별 조회===")
    print("1) 텍스트 생성")
    print("2) 이미지 생성")
    print("3) 영상 생성")
    print("4) 페르소나")
    print("5) 자동화")
    print("6) 기타")

    number = input("선택: ")

    categories = {
        "1": "텍스트 생성",
        "2": "이미지 생성",
        "3": "영상 생성",
        "4": "페르소나",
        "5": "자동화",
        "6": "기타"

    }

    selected = categories[number]

    print("[" + selected + "] 카테고리 프롬프트:")

    count = 0
    for prompt in prompts: 
        if prompt["category"] == selected:
            count  = count + 1
            star = "⭐" if prompt["favorite"] else ""
            print(count, prompt["title"], star)

    if count == 0:
        print("해당 카테고리에 프롬프트가 없습니다.")
    else:
        print("총", count, "개의 프롬프트")

def search_prompt():
    print("=== 프롬프트 검색 ===")
    keyword = input("검색어: ")

    print("검색결과:")
    count = 0
    for prompt in prompts:
        if keyword in prompt["title"] or keyword in prompt["content"]:
            count = count + 1
            star = "⭐" if prompt["favorite"] else ""
            print(count, "[" + prompt["category"] + "]", prompt["title"], star)

    if count == 0:
        print("검색결과가 없습니다.")
    else:
        print(count, "개의 프롬프트를 찾았습니다.")

def show_detail():
    print("=== 프롬프트 상세 보기 ===")
    number = input("번호 입력: ")
    number = int(number)

    if number < 1 or number > len(prompts):
        print("잘못된 번호입니다.")
        return

    index = number - 1
    prompt = prompts[index]
    star = "⭐" if prompt["favorite"] else ""

    print("----------------------------")
    print("제목:", prompt["title"])
    print("카테고리:", prompt["category"])
    print("즐겨찾기:", star)
    print("----------------------------")
    print("내용:")
    print(prompt["content"])
    print("----------------------------")

def delete_prompt():
    list_prompts()
    number = input("삭제할 프롬프트 번호를 입력해주세요: ")
    number = int(number)
    index = number - 1
    del prompts[index]
    print("프롬프트가 삭제되었습니다!")

def toggle_favorite():
    print("=== 즐겨찾기 관리 ===")
    number = input("프롬프트 번호 입력: ")
    number = int(number)

    if number < 1 or number > len(prompts):
        print("잘못된 번호입니다.")
        return

    index = number - 1
    prompt = prompts[index]
    prompt["favorite"] = not prompt["favorite"]

    if prompt["favorite"]:
        print("'" + prompt["title"] + "'프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print("'" + prompt["title"] + "'프롬프트를 즐겨찾기에서 해제했습니다!")

def show_favorites():
    print("=== 즐겨찾기 목록 ===")

    favorites = []
    for prompt in prompts:
        if prompt["favorite"]:
            favorites.append(prompt)

    favorites = sorted(favorites, key=lambda p: p["category"])

    count = 0
    for prompt in favorites:
        count = count + 1
        print(count, "[" + prompt["category"] + "]", prompt["title"], "⭐")


    if count == 0:
        print("즐겨찾기한 프롬프트가 없습니다")
    else:
        print("총", count, "개의 즐겨찾기") 

while True:
    print("=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 프롬프트 삭제")
    print("4. 카테고리별 조회")
    print("5. 프롬프트 검색")
    print("6. 프롬프트 상세 보기")
    print("7. 즐겨찾기 관리")
    print("8. 즐겨찾기 목록")
    print("0. 종료")

    choice = input("선택: ")

    if choice == "1":
        add_prompt()
    elif choice == "2":
        list_prompts()
    elif choice == "3":
        delete_prompt()
    elif choice == "4":
        show_by_category()
    elif choice == "5":
        search_prompt()
    elif choice =="6":
        show_detail()
    elif choice == "7":
        toggle_favorite()
    elif choice =="8":
        show_favorites()
    elif choice == "0":
        print("종료합니다.")
        break
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")    