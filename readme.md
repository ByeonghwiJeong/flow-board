# board - encryption, 외부API

</br>

## ⏳ 개발 기간
**2022.09.06 ~ 2022.09.07**

</br>
  
## 🖥️ 프로젝트


### 프로젝트 주체 : *ThingsFlow*

[<img src='https://krafton.com/wp-content/uploads/2022/08/thingsflow_brandmark_Primary_RGB.png' alt='띵스플로우' width="400px"/>](https://krafton.com/studios/thingsflow/)


### ✍🏻프로젝트 주제

> **외부API를 이용한 게시판 구현 & 암호화**

### 🧹 사용된 기술
- **Back-End** : Python, Django, requests, bcrypt, mysql
- **ETC** : Git, Github

### ⭕프로젝트 상세 구현 사항

- **이모지** 활용을 위한 Database Setting
  - **`MySQL`**
    - Character Set - utf8mb4
    - Collate - utf8mb4_unicode_ci
  - **`Django`**
    ```
    'OPTIONS': {'charset': 'utf8mb4', 'use_unicode': True}
    ```
<br/>

- **게시판 등록**  ▶️  `[POST] {url}/board`
  - **requests 패키지**를 활용한 weather API 활용 : 현재 날씨 상황 가져오기
  - **re module**을 활용한 비밀번호 valiator 구현
    - 비밀번호 자릿수 & 비밀번호 숫자 포함에 따른 message 출력
    - `"Enter 6 or more English letters and numbers"`
    - `"Enter 1 or more numbers"`
  - **bcypt 패키지**를 활용해서 암호화해 비밀번호 저장
<br/>

- **게시판 리스트** ▶️ `[GET] {url}/board?page={number}`
  - QueryString key인 page에 따라서 전체출력 or 20개 단위 출력
  - 웹 스크롤링시 QueryString key page값 받기 ~ [1, N]
<br/>

- **게시판 삭제** ▶️ `[POST] {url}/board/<int:post_id>/delete`
  - **bcypt 패키지**를 활용한 post_id에 따른 비밀번호 일치확인
<br/>

- **게시판 리스트** ▶️ `[GET] {url}/board/<int:post_id>/update`
  - **bcypt 패키지**를 활용한 post_id에 따른 비밀번호 일치확인
<br/>

