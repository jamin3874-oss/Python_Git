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
        "title": "도로 안전 뉴스 자동화 보고서 작성 요청",
        "content": "Notion의 'Codyssey 3차 과제' 아래 '프로젝트 2｜도로 안전 뉴스 자동화 설계 및 구현' 페이지를 완성해줘. 현재 페이지 내용을 읽고 유용한 기존 내용은 유지하면서 체크리스트와 '확인 필요' 상태를 실제 보고서 형식으로 수정해줘. 자동화할 반복 업무 정의, 자동화 도구 선정 이유, 자동 실행 구조, 워크플로 흐름이 명확히 드러나야 하고, 지정된 캡처 이미지들을 각 설명 아래 삽입하고, 검증하지 못한 내용은 성공했다고 단정하지 않도록 작성해줘.",
        "category": "자동화",
        "favorite": False
    }
]

def add_prompt():
    title = input("제목: ")
    content = input("내용: ")
    category = input("카테고리 선택 (텍스트 생성, 이미지 생성, 영상 생성, 페르소나, 자동화, 기타): ") 

    prompt  ={"title": title, "content": content, "category": category, "favorite": False}
    prompts.append(prompt)
    print("프롬프트가 추가되었습니다")

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

    selected = categories[number   ]

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

def delete_prompt():
    list_prompts()
    number = input("삭제할 프롬프트 번호를 입력해주세요: ")
    number = int(number)
    index = number - 1
    del prompts[index]
    print("프롬프트가 삭제되었습니다!")

while True:
    print("=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 프롬프트 삭제")
    print("4. 카테고리별 조회")
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
    elif choice == "0":
        print("종료합니다.")
        break
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")    