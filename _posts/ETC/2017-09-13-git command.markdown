---
layout: post
title: Git 명령어 정리
tags:
  - Git
category: ETC
---

## Git 기본 설정

- `config` : git의 기본 설정을 변경

```
git config [옵션]

옵션:
    user.name "유저 이름" : 유저 이름 설정
    user.email [메일주소] : 유저 메일주소 설정
    --global : 전역 설정
    -- list : 설정 목록 확인
```

- `help` : 명령어 도움말 보기

```
git help [명령어]
```
- - -

## Git 저장소 생성하기

- `init` : 현재 디렉토리를 새로운 Git 저장소로 설정

```
git init
```

- `clone` : github 저장소로부터 데이터를 복사 (동시에 origin 리모트 저장소를 생성)

```
git clone [github 저장소 url]
```

- - -

## 스냅샷 관리

- `status` : working directory와 staging area의 상태 확인

```
git status
gst
```

- `diff` : working directory와 staging area의 차이 확인

```
git diff [옵션]

옵션:
    --staged : 마지막 커밋과 staging area의 차이 확인 
``` 

- `add` : 파일을 staging area에 추가

```
git add [파일이름] [옵션]

옵션:
    -A, --all 변경된 모든 파일 추가
```

- `commit` : stage에 추가된 파일 목록을 커밋함.

```
git commit [옵션]

옵션:
    -m [메세지] : 커밋 메세지와 함께 커밋
    -a : 자동으로 add를 진행한 후 커밋
    -v : 커밋 메세지에 diff의 내용 포함
```
- `reset` : 바로 전 커밋으로 돌아감

```
git reset : 직전의 add 이전의 상태로 staging area를 되돌림
git reset --soft HEAD^ : 직전의 커밋을 되돌림
```

- `rm` : 파일을 working directory와 staging area에서 삭제

```
git rm [옵션] [파일이름]

옵션:
    --cached : 파일을 staging area에서 제외(working directory의 파일은 유지됨)
    -f, --force : 삭제하려는 파일의 내용이 브랜치 끝 부분에서의 내용과 다를 경우 강제 삭제 
    --ignore-unmatch : 삭제하려는 파일이 없을 때 발생하는 에러를 무시
```

- `mv` : 파일의 위치 또는 이름을 변경

```
git mv [파일이름] [새 이름] : 파일 이름 변경
git mv [파일이름] [새 경로] : 파일 경로 변경
```



- `log` : 로그확인 변경사항 확인가능

```
git log [옵션]

옵션:
    -p : 변경사항 확인
    --oneline : 커밋 메세지만 한줄씩 표시
    --all : 모든 브랜치 로그 표시
    --graph : 브랜치 트리 그래프 표시
```

- `clean` : working directory의 필요없는 파일을 삭제

```
git clean
```

- - -

## Branch 다루기

- `branch` : 브랜치를 관리

```
git branch [옵션]

옵션:
    [] : 브랜치 목록을 보여줌
    [브랜치 이름] : 현재 커밋에 새 브랜치 생성
    -v : 각 브랜치의 마지막 커밋 메세지를 보여줌
    -merged : merge된 브랜치 목록 확인
    -no-merged : merge하지 않은 브랜치 목록 확인
    -d : 브랜치 삭제
    -D : 브랜치 강제 삭제
```

git remote add `<remote` 저장소 이름> <주소> : 주소의 저장소를 원격 저장소에 추가
git remote -v: 리모트 저장소 확인
git remote remove <remote 저장소이름> : 리모트 저장소 삭제

git push: 현재 브랜치 내용을 저장소에 업데이트

git branch : 현재 커밋에 브랜치 추가
git branch -d : 브랜치 삭제
git branch --merged : merged 된 브랜치 확인
git branch --no-merged : merge 되지 않은 브랜치 확인

git checkout <커밋값 또는 브랜치이름>: 해당 커밋 값 또는 브랜치이름으로 head변경

git merge <브랜치이름> : 현재 위치 커밋과 브랜치의 커밋을 합침



- - - 

##### Reference: 

Git-book : [https://git-scm.com/book/ko/v2](https://git-scm.com/book/ko/v2)
