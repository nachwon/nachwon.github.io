---
layout: post
title: Git command 정리
author: Che1
category: ETC
---

- 현재 폴더를 git repo로 설정
```
git init
``` 

- 현재 스테이지 상태 확인
```
git status
gst
```
- 파일을 커밋 목록에 추가 (stage)

```
git add [파일이름] [옵션]

옵션:
    -A, --all 모든 파일의 변경사항 추가

```

- 파일을 커밋 목록에서 제외시킴

```
git rm --cached [파일이름]
```

- stage에 추가된 파일 목록을 커밋함.

```
git commit [옵션]

옵션:
    -m [메세지] : 커밋 메세지와 함께 커밋
```
- 로그확인 변경사항 확인가능

```
git log [옵션]

옵션:
    -p : 변경사항 확인
    --oneline : 커밋 메세지만 한줄씩 표시
    --all : 모든 브랜치 로그 표시
    --graph : 브랜치 트리 그래프 표시
```


git diff: 커밋 하지 않고 변경사항 확인
git diff --staged : add 한 파일의 변경사항 확인

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

git reset HEAD^ : 바로 전 커밋으로 돌아감

