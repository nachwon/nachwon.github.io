---
layout: post
title: Git command 정리
author: Che1
category: ETC
---


git init : 현재 폴더를 git repo로 설정

git status: 현재 스테이지 상태 확인

git add <파일이름> : 파일을 커밋 목록에 포함시킴.

git rm --cached <파일이름> : 파일을 커밋 목록에서 제외시킴

git commit -m '코멘트' : 코멘트를 달고 커밋함 한줄 코멘트인 경우
git commit: 텍스트 에디터가 열리고 여러줄의 코멘트 추가 할 수 있음

git log -p: 로그확인 변경사항 확인가능
git log --oneline:  커밋 코멘트만 한줄씩 로그 표시
git log --all: 모든 브랜치 로그 표시
git log -- graph: 브랜치 그래픽 표시 

git diff: 커밋 하지 않고 변경사항 확인
git diff --staged : add 한 파일의 변경사항 확인

git remote add <remote저장소 이름> <주소> : 주소의 저장소를 원격 저장소에 추가
git remote -v: 리모트 저장소 확인
git remote remove <remote저장소이름> : 리모트 저장소 삭제

git push: 현재 브랜치 내용을 저장소에 업데이트

git branch : 현재 커밋에 브랜치 추가
git branch -d : 브랜치 삭제
git branch --merged : merged 된 브랜치 확인
git branch --no-merged : merge 되지 않은 브랜치 확인

git checkout <커밋값 또는 브랜치이름>: 해당 커밋 값 또는 브랜치이름으로 head변경

git merge <브랜치이름> : 현재 위치 커밋과 브랜치의 커밋을 합침

git reset HEAD^ : 바로 전 커밋으로 돌아감

